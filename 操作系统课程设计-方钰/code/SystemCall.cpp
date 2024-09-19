#define _CRT_SECURE_NO_WARNINGS
#include "SystemCall.h"

int Sys_Open(const char* path, int mode)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);
	u.u_dirp = path_tmp;
	u.u_arg[1] = mode;

	fileMgr.Open();

	return u.u_ar0[User::EAX];
}

void Sys_Close(int fd){
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	u.u_arg[0] = fd;

	fileMgr.Close();

	return;
}

int Sys_Read(int fd, unsigned char* buffer, int count)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	u.u_arg[0] = fd;
	u.u_arg[1] = (unsigned int) buffer;
	u.u_arg[2] = count;

	fileMgr.Read();

	return u.u_ar0[User::EAX];
}

int Sys_Write(int fd, unsigned char* buffer, int count)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	u.u_arg[0] = fd;
	u.u_arg[1] = (unsigned int)buffer;
	u.u_arg[2] = count;

	fileMgr.Write();

	return u.u_ar0[User::EAX];
}

void Sys_MkNod(const char* path, int mode)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);

	u.u_dirp = path_tmp;
	u.u_arg[1] = mode;

	fileMgr.MkNod();

	return;
}

void Sys_ChDir(const char* path)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);

	u.u_dirp = path_tmp;
	u.u_arg[0] = (unsigned int) path_tmp;

	fileMgr.ChDir();

	return;
}

int Sys_Creat(const char* path, int mode)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);

	u.u_dirp = path_tmp;
	u.u_arg[1] = mode;

	fileMgr.Creat();

	return u.u_ar0[User::EAX];
}

void Sys_Seek(int fd, int offset, int mode)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	u.u_arg[0] = fd;
	u.u_arg[1] = offset;
	u.u_arg[2] = mode;

	fileMgr.Seek();

	return;
}

void Sys_Unlink(const char* path)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);

	u.u_dirp = path_tmp;
	u.u_arg[0] = (unsigned int)path_tmp;

	fileMgr.UnLink();

	return;
}

void Sys_Stat(const char* path, const DiskInode* inode)
{
	User& u = OSKernel::Instance().GetUser();
	FileManager& fileMgr = OSKernel::Instance().GetFileManager();

	char path_tmp[DirectoryEntry::DIRSIZ << 3];
	strcpy(path_tmp, path);

	u.u_dirp = path_tmp;
	u.u_arg[0] = (unsigned int)path_tmp;
	u.u_arg[1] = (unsigned int)inode;

	fileMgr.Stat();

	return;
}