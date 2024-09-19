#include "OSKernel.h"

OSKernel OSKernel::instance;

OSKernel::OSKernel()
{
	this->m_DeviceManager = new DeviceManager();
	this->m_BufferManager = new BufferManager();
	this->m_FileSystem = new FileSystem();
	this->m_FileManager = new FileManager();
	this->m_User = new User();
}

OSKernel::~OSKernel()
{
	delete this->m_User;
	delete this->m_FileManager;
	delete this->m_FileSystem;
	delete this->m_BufferManager;
	delete this->m_DeviceManager;
}

void OSKernel::Restart()
{
	/* 用于格式化时的重新加载 */
	delete this->m_User;
	delete this->m_FileManager;
	delete this->m_FileSystem;
	delete this->m_BufferManager;
	delete this->m_DeviceManager;
	this->m_DeviceManager = new DeviceManager();
	this->m_BufferManager = new BufferManager();
	this->m_FileSystem = new FileSystem();
	this->m_FileManager = new FileManager();
	this->m_User = new User();
}

OSKernel& OSKernel::Instance()
{
	return OSKernel::instance;
}

BufferManager& OSKernel::GetBufferManager()
{
	return *(this->m_BufferManager);
}

DeviceManager& OSKernel::GetDeviceManager()
{
	return *(this->m_DeviceManager);
}

FileSystem& OSKernel::GetFileSystem()
{
	return *(this->m_FileSystem);
}

FileManager& OSKernel::GetFileManager()
{
	return *(this->m_FileManager);
}

User& OSKernel::GetUser()
{
	return *(this->m_User);
}