#ifndef USER_H
#define USER_H

#include "Process.h"
#include "File.h"
#include "INode.h"
#include "FileManager.h"

typedef int ErrorCode;

/*
 * @comment 该类与Unixv6中 struct user结构对应，因此只改变
 * 类名，不修改成员结构名字，关于数据类型的对应关系如下:
 */
class User
{
public:
	static const int EAX = 0;	/* u.u_ar0[EAX]；访问现场保护区中EAX寄存器的偏移量 */

	/* 系统调用相关成员 */
	unsigned int u_ar0[1];		/* 指向核心栈现场保护区中EAX寄存器
								存放的栈单元，本字段存放该栈单元的地址。
								在V6中r0存放系统调用的返回值给用户程序，
								x86平台上使用EAX存放返回值，替代u.u_ar0[R0] */

	int u_arg[5];				/* 存放当前系统调用参数 */
	char* u_dirp;				/* 系统调用参数(一般用于Pathname)的指针 */

	/* 文件系统相关成员 */
	Inode* u_cdir;		/* 指向当前目录的Inode指针 */
	Inode* u_pdir;		/* 指向父目录的Inode指针 */

	DirectoryEntry u_dent;					/* 当前目录的目录项 */
	char u_dbuf[DirectoryEntry::DIRSIZ];	/* 当前路径分量 */
	char u_curdir[128];						/* 当前工作目录完整路径 */

	ErrorCode u_error;			/* 存放错误码 */
	int u_segflg;				/* 表明I/O针对用户或系统空间 */

	/* 进程的用户标识 */
	short u_uid;		/* 有效用户ID */
	short u_gid;		/* 有效组ID */
	short u_ruid;		/* 真实用户ID */
	short u_rgid;		/* 真实组ID */

	/* 文件系统相关成员 */
	OpenFiles u_ofiles;		/* 进程打开文件描述符表对象 */

	/* 文件I/O操作 */
	IOParameter u_IOParam;	/* 记录当前读、写文件的偏移量，用户目标区域和剩余字节数参数 */

	/* Member Functions */
public:
	User();
	~User();

	/* 根据系统调用参数uid设置有效用户ID，真实用户ID，进程用户ID(p_uid) */
	void Setuid();

	/* 获取用户ID，低16比特为真实用户ID(u_ruid)，高16比特为有效用户ID(u_uid) */
	void Getuid();

	/* 根据系统调用参数gid设置有效组ID，真实组ID */
	void Setgid();

	/* 获取组ID, 低16比特为真实组ID(u_rgid)，高16比特为有效组ID(u_gid) */
	void Getgid();

	/* 获取当前用户工作目录 */
	void Pwd();

	/* 检查当前用户是否是超级用户 */
	bool SUser();
};

#endif

