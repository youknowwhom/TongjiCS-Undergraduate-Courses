#include "BufferManager.h"
#include "OSKernel.h"

BufferManager::BufferManager()
{
	this->m_DeviceManager = &OSKernel::Instance().GetDeviceManager();
	bFreeList.b_back = &bFreeList;
	bFreeList.b_forw = &bFreeList;

	for (int i = 0; i < NBUF; i++) {
		Buf* bp = &(m_Buf[i]);
		bp->b_addr = Buffer[i];
		bp->b_bufno = i;
		bp->b_dev = -1;
		bp->b_forw = bFreeList.b_forw;
		bp->b_back = &bFreeList;
		bFreeList.b_forw->b_back = bp;
		bFreeList.b_forw = bp;
	}
}

BufferManager::~BufferManager()
{
	this->Bflush(0);
}

/* Debug用 查看BFreeList各个Buffer和数量 */
void BufferManager::ShowBFreeList()
{
	Buf* bp;
	int cnt = 0;
	for (bp = this->bFreeList.b_forw; bp != &(this->bFreeList); bp = bp->b_forw)
	{
		cout << bp->b_bufno << "(" << bFreeList.b_back->b_bufno << ") ";
		cnt++;
	}
	cout << cnt << endl;
}

Buf* BufferManager::GetBlk(short dev, int blkno)
{
	/* 在所有的Blk中寻找，看是否能够复用 */
	for (int i = 0; i < NBUF; i++) {
		Buf* bp = &(m_Buf[i]);
		if (bp->b_blkno == blkno && bp->b_dev == dev) {
			Logger::info() << "Found block " << blkno << " at buffer " << i <<". Reusing...\n";
			NotAvail(bp);
			return bp;
		}
	}

	/* 没有可以复用的Blk，找新的自由缓存 */
	Buf* bp = this->bFreeList.b_forw;
	if (bp != &this->bFreeList) {
		Logger::info() << "Use free buffer " << bp->b_bufno << ".\n";
		NotAvail(bp);
		if (bp->b_flags & Buf::B_DELWRI) {
			Logger::info() << "Encounter dirty buffer " << bp->b_bufno << ". Writing back...\n";
			Bwrite(bp);
			bp->b_blkno = dev;    
			bp->b_blkno = blkno;
			/* 需要注意此处，Bwrite通过Brelse释放了Buffer。
			 * 如果不重新NotAvail可能导致反复Brelse，
			 * 若Buffer在BFreelist末尾会导致BFreelist成环。*/
			NotAvail(bp);
			/* 注意: 这里清除了所有其他位 */
			bp->b_flags = Buf::B_CLEAR;
			return bp;
		}
		bp->b_dev = dev;
		bp->b_blkno = blkno;

		/* 注意: 这里清除了所有其他位 */
		bp->b_flags = Buf::B_CLEAR;
		return bp;
	}
	else {
		/* 自由缓存是空的？同步读/写不可能出现（Bread用完及时释放），报个错 */
		Logger::err() << "bFreeList is empty.\n";
		return GetBlk(dev, blkno);
	}
}

void BufferManager::NotAvail(Buf* bp)
{
	Logger::info() << "Get buffer " << bp->b_bufno << " from BFreeList\n";

	/* 从自由队列中取出 */
	bp->b_back->b_forw = bp->b_forw;
	bp->b_forw->b_back = bp->b_back;

	return;
}

Buf* BufferManager::Bread(short dev, int blkno)
{
	Buf* bp;
	Logger::info() << "Executing Bread, dev: " << dev << ", blkno: " << blkno << "\n";
	/* 根据设备号，字符块号申请缓存 */
	bp = this->GetBlk(dev, blkno);
	/* 如果在设备队列中找到所需缓存，即B_DONE已设置，就不需进行I/O操作 */
	if (bp->b_flags & Buf::B_DONE)
	{
		return bp;
	}
	/* 没有找到相应缓存，构成I/O读请求块 */
	bp->b_flags |= Buf::B_READ;
	bp->b_wcount = BufferManager::BUFFER_SIZE;

	this->m_DeviceManager->GetBlockDevice(dev<<8).Strategy(bp);
	bp->b_flags |= Buf::B_DONE;

	return bp;
}


void BufferManager::Bwrite(Buf* bp)
{
	bp->b_flags &= ~(Buf::B_READ | Buf::B_DONE | Buf::B_ERROR | Buf::B_DELWRI);
	bp->b_flags |= Buf::B_WRITE;
	bp->b_wcount = BufferManager::BUFFER_SIZE;		/* 512字节 */

	this->m_DeviceManager->GetBlockDevice(bp->b_dev>>8).Strategy(bp);
	this->Brelse(bp);
	
	bp->b_flags |= Buf::B_DONE;

	return;
}


void BufferManager::Bdwrite(Buf* bp)
{
	Logger::info() << "Executing delayed write at buffer " << bp->b_bufno << "\n";
	/* 置上B_DONE允许其它进程使用该磁盘块内容 */
	bp->b_flags |= (Buf::B_DELWRI | Buf::B_DONE);
	this->Brelse(bp);
	return;
}

void BufferManager::Bawrite(Buf* bp)
{
	/* 本次文件系统不涉及异步写 都同步迅速写 */
	this->Bwrite(bp);
	return;
}

void BufferManager::Brelse(Buf* bp)
{
	Logger::info() << "Brelse buffer " << bp->b_bufno << ", blkno:" << bp->b_blkno << "\n";

	(this->bFreeList.b_back)->b_forw = bp;
	bp->b_back = this->bFreeList.b_back;
	bp->b_forw = &(this->bFreeList);
	this->bFreeList.b_back = bp;
}

void BufferManager::Bflush(short dev)
{
	Buf* bp, * next;

	for (bp = this->bFreeList.b_forw; bp != &(this->bFreeList); bp = next)
	{
		next = bp->b_forw;
		/* 找出自由队列中所有延迟写的块 */
		if ((bp->b_flags & Buf::B_DELWRI) && dev == bp->b_dev)
		{
			this->NotAvail(bp);
			this->Bwrite(bp);
		}
	}

	return;
}

void BufferManager::ClrBuf(Buf* bp)
{
	int* pInt = (int*)bp->b_addr;

	/* 将缓冲区中数据清零 */
	for (unsigned int i = 0; i < BufferManager::BUFFER_SIZE / sizeof(int); i++)
	{
		pInt[i] = 0;
	}
	return;
}

Buf& BufferManager::GetBFreeList()
{
	return this->bFreeList;
}