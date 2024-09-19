#include "File.h"
#include "OSKernel.h"

/*==============================class File===================================*/
File::File()
{
	this->f_count = 0;
	this->f_flag = 0;
	this->f_offset = 0;
	this->f_inode = nullptr;
}

File::~File()
{
}

/*==============================class OpenFiles===================================*/
OpenFiles::OpenFiles()
{
}

OpenFiles::~OpenFiles()
{
}

int OpenFiles::AllocFreeSlot()
{
	int i;
	User& u = OSKernel::Instance().GetUser();

	for (i = 0; i < OpenFiles::NOFILES; i++)
	{
		/* 进程打开文件描述符表中找到空闲项，则返回之 */
		if (this->ProcessOpenFileTable[i] == nullptr)
		{
			/* 设置核心栈现场保护区中的EAX寄存器的值，即系统调用返回值 */
			u.u_ar0[User::EAX] = i;
			return i;
		}
	}

	u.u_ar0[User::EAX] = -1;   /* Open1，需要一个标志。当打开文件结构创建失败时，可以回收系统资源*/
	u.u_error = EMFILE;
	return -1;
}


File* OpenFiles::GetF(int fd)
{
	File* pFile;
	User& u = OSKernel::Instance().GetUser();

	/* 如果打开文件描述符的值超出了范围 */
	if (fd < 0 || fd >= OpenFiles::NOFILES)
	{
		u.u_error = EBADF;
		return nullptr;
	}

	pFile = this->ProcessOpenFileTable[fd];
	if (pFile == nullptr)
	{
		u.u_error = EBADF;
	}

	return pFile;	/* 即使pFile==nullptr也返回它，由调用GetF的函数来判断返回值 */
}

void OpenFiles::SetF(int fd, File* pFile)
{
	if (fd < 0 || fd >= OpenFiles::NOFILES)
	{
		return;
	}
	/* 进程打开文件描述符指向系统打开文件表中相应的File结构 */
	this->ProcessOpenFileTable[fd] = pFile;
}

/*==============================class IOParameter===================================*/
IOParameter::IOParameter()
{
	this->m_Base = 0;
	this->m_Count = 0;
	this->m_Offset = 0;
}

IOParameter::~IOParameter()
{
}

