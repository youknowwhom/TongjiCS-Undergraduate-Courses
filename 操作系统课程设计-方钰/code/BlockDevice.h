#ifndef BLOCK_DEVICE_H
#define BLOCK_DEVICE_H

#include <iostream>
#include <fstream>
#include <string>

#include "Buf.h"
#include "Logger.h"

using namespace std;


/*
 * 块设备基类，各类块设备都从此基类继承。
 */
class BlockDevice
{
public:
	virtual ~BlockDevice() {};
	/*
	 * 定义为虚函数，由派生类进行override实现设备
	 * 特定操作。正常情况下，基类中函数不应被调用到。
	 */
	virtual int Strategy(Buf* bp) = 0;
};


/* 一级文件虚拟设备派生类。从块设备基类BlockDevice继承而来。 */
class VirtualFileDevice : public BlockDevice
{
public:
	static const int SECTOR_SIZE = BUF_SIZE;
	static const int DEVICE_MEMORY = 40 << 20;
	static const int NSECTOR = DEVICE_MEMORY / SECTOR_SIZE;

	VirtualFileDevice(string filename);
	~VirtualFileDevice();
	/*
	 * Override基类BlockDevice中的虚函数，实现
	 * 派生类VirtualFileDevice特定的设备操作逻辑。
	 */
	int Strategy(Buf* bp);

private:
	string filename;
	fstream file;

	int Bno2Addr(int bno);
	int Read(Buf* bp);
	int Write(Buf* bp);
};

#endif
