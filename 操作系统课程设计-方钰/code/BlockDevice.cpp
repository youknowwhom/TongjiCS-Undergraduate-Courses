#include "BlockDevice.h"

VirtualFileDevice::VirtualFileDevice(string filename)
{
    this->filename = filename;

    ifstream check_file(filename);
    if (check_file) {
        Logger::info() << "Virtual disk file exists. Opening...\n";
        // 文件存在，以二进制模式打开进行读写
        check_file.close();
        file.open(filename, ios::binary | ios::in | ios::out);
    }
    else {
        Logger::info() << "Virtual disk file does not exist. Creating...\n";
        // 文件不存在，创建并填充为全 0
        file.open(filename, ios::binary | ios::out);
        if (file) {
            char* buffer = new char[DEVICE_MEMORY];
            memset(buffer, 0, DEVICE_MEMORY);
            file.write(buffer, DEVICE_MEMORY);
            delete[] buffer;
            Logger::info() << "Virtual Disk file created and filled with zeros.\n";
            file.close();
            file.open(filename, ios::binary | ios::in | ios::out);
        }
        else {
            Logger::err() << "Failed to create virtual disk file.\n";
            return;
        }
    }
}

VirtualFileDevice::~VirtualFileDevice()
{
    // TODO: 延迟写
    file.close();
}

int VirtualFileDevice::Strategy(Buf* bp)
{
	if (bp->b_blkno < 0 || bp->b_blkno >= NSECTOR) {
		bp->b_flags |= Buf::B_ERROR;
		Logger::err() << "Invalid block number to read / write.\n";
	}
	else {
		if (bp->b_flags & Buf::B_WRITE)
			Write(bp);
		else if (bp->b_flags & Buf::B_READ)
			Read(bp);
	}

	return 0;
}

int VirtualFileDevice::Bno2Addr(int blkno)
{
	return blkno * SECTOR_SIZE;
}

int VirtualFileDevice::Read(Buf* bp)
{
    int addr = Bno2Addr(bp->b_blkno);

    file.seekg(addr, ios::beg);
    file.read((char*)bp->b_addr, SECTOR_SIZE);

    Logger::info() << "Read Virtual Disk, blkno:" << bp->b_blkno << " addr:0x" << hex << addr << dec << " count:" << file.gcount() << "\n";

	return 0;
}

int VirtualFileDevice::Write(Buf* bp)
{
    int addr = Bno2Addr(bp->b_blkno);

    file.seekp(addr, ios::beg);
    file.write((char*)bp->b_addr, SECTOR_SIZE);
    file.flush();

    Logger::info() << "Write Virtual Disk, blkno:" << bp->b_blkno << " addr:0x" << hex << addr << dec << "\n";

	return 0;
}