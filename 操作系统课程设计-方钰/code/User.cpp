#define _CRT_SECURE_NO_WARNINGS
#include "OSKernel.h"
#include "User.h"

User::User()
{
	FileSystem* fSys = &OSKernel::Instance().GetFileSystem();
	/* 指向当前目录的Inode指针 */
	u_cdir = (&g_InodeTable)->IGet(0, fSys->ROOTINO);		// 注意这里应当独立的IGet，否则切换文件夹会导致RootInode被IPut
	/* 指向父目录的Inode指针 */
	u_pdir = u_cdir;

	strcpy(u_curdir, "/");

	/* 进程的用户标识 */
	u_uid = 0;		/* 有效用户ID */
	u_gid = 0;		/* 有效组ID */
	u_ruid = 0;		/* 真实用户ID */
	u_rgid = 0;		/* 真实组ID */
}

User::~User()
{

}

void User::Setuid()
{
	short uid = this->u_arg[0];

	if (this->u_ruid == uid || this->SUser())
	{
		this->u_uid = uid;
		this->u_ruid = uid;
	}
	else
	{
		this->u_error = EPERM;
	}
}

void User::Getuid()
{
	unsigned int uid;

	uid = (this->u_uid << 16);
	uid |= (this->u_ruid & 0xFF);
	this->u_ar0[User::EAX] = uid;
}

void User::Setgid()
{
	short gid = this->u_arg[0];

	if (this->u_rgid == gid || this->SUser())
	{
		this->u_gid = gid;
		this->u_rgid = gid;
	}
	else
	{
		this->u_error = EPERM;
	}
}

void User::Getgid()
{
	unsigned int gid;

	gid = (this->u_gid << 16);
	gid |= (this->u_rgid & 0xFF);
	this->u_ar0[User::EAX] = gid;
}

void User::Pwd()
{
	strcpy(this->u_dirp, this->u_curdir);
}

bool User::SUser()
{
	if (0 == this->u_uid)
	{
		return true;
	}
	else
	{
		this->u_error = EPERM;
		return false;
	}
}
