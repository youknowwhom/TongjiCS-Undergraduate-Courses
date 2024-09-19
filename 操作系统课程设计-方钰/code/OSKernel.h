#ifndef OSKernel_H
#define OSKernel_H

#include "User.h"
#include "BufferManager.h"
#include "DeviceManager.h"
#include "FileManager.h"
#include "FileSystem.h"


/*
 * OSKernel类用于封装所有内核相关的全局类实例对象。
 *
 * OSKernel类在内存中为单体模式，保证内核中封装各内核
 * 模块的对象都只有一个副本。
 */
class OSKernel
{
public:
	OSKernel();
	~OSKernel();
	void Restart();
	static OSKernel& Instance();

	BufferManager& GetBufferManager();
	DeviceManager& GetDeviceManager();
	FileSystem& GetFileSystem();
	FileManager& GetFileManager();
	User& GetUser();


private:
	static OSKernel instance;		/* OSKernel单体类实例 */

	BufferManager* m_BufferManager;
	DeviceManager* m_DeviceManager;
	FileSystem* m_FileSystem;
	FileManager* m_FileManager;
	User* m_User;
};

#endif
