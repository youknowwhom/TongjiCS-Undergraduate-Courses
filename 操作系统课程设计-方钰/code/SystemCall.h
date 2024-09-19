#include "OSKernel.h"

/* 该文件模仿系统调用，对FileManager和User结构操作进行整合 */

/**
 * 打开文件
 * @param path 文件路径
 * @param mode 打开模式
 * @return fd
 */
int Sys_Open(const char* path, int mode);

/**
 * 关闭文件
 * @param fd
 */
void Sys_Close(int fd);

/**
 * 读入文件
 * @param fd
 * @param buffer 读入缓存首地址
 * @param count 读入字节数
 * @return 读入的字节数
 */
int Sys_Read(int fd, unsigned char* buffer, int count);

/**
 * 写入文件
 * @param fd
 * @param buffer 写入缓存首地址
 * @param count 写入字节数
 * @return 写入的字节数
 */
int Sys_Write(int fd, unsigned char* buffer, int count);

/**
 * 新建文件夹
 * @param path 新建路径
 * @param mode
 */
void Sys_MkNod(const char* path, int mode = 040755 /* Unix V6++中mkdir的default mode */ );

/**
 * 改变当前目录
 * @param path改变的路径
 */
void Sys_ChDir(const char* path);

/**
 * 创建文件
 * @param path创建的文件路径
 * @return fd
 */
int Sys_Creat(const char* path, int mode = Inode::IRWXU);

/**
 * 调整文件读写指针
 * @param fd 文件描述符
 * @param offset
 * @param mode seek模式(beg, cur, ate)
 */
void Sys_Seek(int fd, int offset, int mode);

/**
 * 删除文件
 * @param path 文件路径
 */
void Sys_Unlink(const char* path);

/**
 * 读取Inode信息
 * @param path 文件路径
 * @param
 */
void Sys_Stat(const char* path, const DiskInode* inode);



