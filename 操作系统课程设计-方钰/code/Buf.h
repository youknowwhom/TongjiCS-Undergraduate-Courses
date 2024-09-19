#ifndef BUF_H
#define BUF_H

#define BUF_SIZE 512

/*
 * 缓存控制块buf定义
 * 记录了相应缓存的使用情况等信息；
 * 同时兼任I/O请求块，记录该缓存
 * 相关的I/O请求和执行结果。
 */
class Buf
{
public:
	enum BufFlag	/* b_flags中标志位 */
	{
		B_CLEAR		= 0x0,		/* b_flags所有标记清空 */
		B_WRITE		= 0x1,		/* 写操作。将缓存中的信息写到硬盘上去 */
		B_READ		= 0x2,		/* 读操作。从盘读取信息到缓存中 */
		B_DONE		= 0x4,		/* I/O操作结束 */
		B_ERROR		= 0x8,		/* I/O因出错而终止 */
		B_DELWRI	= 0x10		/* 延迟写，在相应缓存要移做他用时，再将其内容写到相应块设备上 */
	};

public:
	unsigned int b_flags;	/* 缓存控制块标志位 */

	Buf* b_forw;
	Buf* b_back;

	short	b_dev;			/* 主、次设备号，其中高8位是主设备号，低8位是次设备号 */
	int		b_wcount;		/* 需传送的字节数 */
	unsigned char* b_addr;	/* 指向该缓存控制块所管理的缓冲区的首地址 */
	int		b_bufno;		/* 缓存块在缓存块队列中的下标 */
	int		b_blkno;		/* 磁盘逻辑块号 */
	int		b_error;		/* I/O出错时信息 */
	int		b_resid;		/* I/O出错时尚未传送的剩余字节数 */
};

#endif
