#ifndef OPEN_FILE_MANAGER_H
#define OPEN_FILE_MANAGER_H

#include "INode.h"
#include "File.h"
#include "FileSystem.h"

/* Forward Declaration */
class OpenFileTable;
class InodeTable;

/* 以下2个对象实例定义在OpenFileManager.cpp文件中 */
extern InodeTable g_InodeTable;
extern OpenFileTable g_OpenFileTable;

/*
 * 打开文件管理类(OpenFileManager)负责
 * 内核中对打开文件机构的管理，为进程
 * 打开文件建立内核数据结构之间的勾连关系。
 * 
 * 勾连关系指进程u区中打开文件描述符指向
 * 打开文件表中的File打开文件控制结构，
 * 以及从File结构指向文件对应的内存Inode。
 */
class OpenFileTable
{
public:
	/* static consts */
	static const int NFILE = 100;	/* 打开文件控制块File结构的数量 */

	/* Functions */
public:
	/* Constructors */
	OpenFileTable();
	/* Destructors */
	~OpenFileTable();


	/*
	 * @comment 在系统打开文件表中分配一个空闲的File结构
	 */
	File* FAlloc();
	/*
	 * @comment 对打开文件控制块File结构的引用计数f_count减1，
	 * 若引用计数f_count为0，则释放File结构。
	 */
	void CloseF(File* pFile);

	/* Members */
public:
	File m_File[NFILE];			/* 系统打开文件表，为所有进程共享，进程打开文件描述符表
								中包含指向打开文件表中对应File结构的指针。*/
};

/*
 * 内存Inode表(class InodeTable)
 * 负责内存Inode的分配和释放。
 */
class InodeTable
{
	/* static consts */
public:
	static const int NINODE = 100;	/* 内存Inode的数量 */

	/* Functions */
public:
	/* Constructors */
	InodeTable();
	/* Destructors */
	~InodeTable();

	/*
	 * @comment 根据指定设备号dev，外存Inode编号获取对应
	 * Inode。如果该Inode已经在内存中，对其上锁并返回该内存Inode，
	 * 如果不在内存中，则将其读入内存后上锁并返回该内存Inode
	 */
	Inode* IGet(short dev, int inumber);
	/*
	 * @comment 减少该内存Inode的引用计数，如果此Inode已经没有目录项指向它，
	 * 且无进程引用该Inode，则释放此文件占用的磁盘块。
	 */
	void IPut(Inode* pNode);

	/*
	 * @comment 将所有被修改过的内存Inode更新到对应外存Inode中
	 */
	void UpdateInodeTable();

	/*
	 * @comment 检查设备dev上编号为inumber的外存inode是否有内存拷贝，
	 * 如果有则返回该内存Inode在内存Inode表中的索引
	 */
	int IsLoaded(short dev, int inumber);
	/*
	 * @comment 在内存Inode表中寻找一个空闲的内存Inode
	 */
	Inode* GetFreeInode();

	/* Members */
public:
	Inode m_Inode[NINODE];		/* 内存Inode数组，每个打开文件都会占用一个内存Inode */

	FileSystem* m_FileSystem;	/* 对全局对象g_FileSystem的引用 */
};

#endif
