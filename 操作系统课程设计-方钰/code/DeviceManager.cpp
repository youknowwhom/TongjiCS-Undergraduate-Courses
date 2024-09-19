#include "DeviceManager.h"

using namespace std;

DeviceManager::DeviceManager()
{
	this->nblkdev = 1;
	bdevsw[0] = new VirtualFileDevice("c.img");
	for (int i = 1; i < MAX_DEVICE_NUM; i++) {
		bdevsw[i] = nullptr;
	}
}

DeviceManager::~DeviceManager()
{
	delete bdevsw[0];
}

int DeviceManager::GetNBlkDev()
{
	return this->nblkdev;
}

BlockDevice& DeviceManager::GetBlockDevice(short major)
{
	if (major >= this->nblkdev || major < 0)
	{
		Logger::err() << "Block Device Doesn't Exist!\n";
	}
	return *(this->bdevsw[major]);
}