#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <sstream>
#include "Shell.h"
#include "SystemCall.h"
using namespace std;

/* 存储字符串，用于fread/fwrite */
unordered_map<string, string> str_set;

Shell::Shell() : commands{
    new Command_ls(),
    new Command_cd(),
    new Command_cp(),
    new Command_mv(),
    new Command_mkdir(),
    new Command_fformat(),
    new Command_fcreat(),
    new Command_fdelete(),
    new Command_fopen(),
    new Command_fclose(),
    new Command_fread(),
    new Command_fwrite(),
    new Command_flseek(),
    new Command_tree()
}{ }

Shell::~Shell()
{
    for (int i = 0; i < NCOMMAND; i++) {
        if (commands[i])
            delete commands[i];
    }
}

void Shell::interface()
{
	while (true) {
        User& u = OSKernel::Instance().GetUser();   /* 放在循环体内，fformat可能重新加载User */
        cout << u.u_curdir << "$ ";
        string line;
        getline(cin, line);

        istringstream iss(line);
        vector<std::string> words;
        string word;

        /* 分割命令行 */
        while (iss >> word) {
            words.push_back(word);
        }

        if (words.size() == 0)
            continue;

        if (words[0] == string("help")) {
            for (int i = 0; i < NCOMMAND; i++) {
                if (commands[i]) {
                    cout << commands[i]->name << "\t<" << commands[i]->description << ">\n";
                }
            }
            cout << "quit\t<退出系统>\n";
            cout << endl;
            continue;
        }
        else if(words[0] == string("quit")) {
            break;
        }

        /* 匹配命令 */
        int i;
        for (i = 0; i < NCOMMAND; i++) {
            if (commands[i] == nullptr)
                continue;
            else if (commands[i]->name == words[0]) {
                words.erase(words.begin());
                commands[i]->execute(words);
                handleUserError();
                cout << endl;
                break;
            }
        }
        if (i == NCOMMAND)
            cout << "命令不存在!\n" << endl;
	}
}

void Shell::handleUserError()
{
    User& u = OSKernel::Instance().GetUser();
    switch (u.u_error) {
        case EPERM:           cout << "操作不允许" << endl; break;
        case ENOENT:          cout << "文件或目录不存在" << endl; break;
        case ESRCH:           cout << "没有这样的进程" << endl; break;
        case EINTR:           cout << "被中断的系统调用" << endl; break;
        case EIO:             cout << "I/O 错误" << endl; break;
        case ENXIO:           cout << "没有这样的设备或地址" << endl; break;
        case E2BIG:           cout << "参数列表太长" << endl; break;
        case ENOEXEC:         cout << "执行格式错误" << endl; break;
        case EBADF:           cout << "文件描述符不正确" << endl; break;
        case ECHILD:          cout << "没有子进程" << endl; break;
        case EAGAIN:          cout << "资源暂时不可用" << endl; break;
        case ENOMEM:          cout << "内存不足" << endl; break;
        case EACCES:          cout << "权限不够" << endl; break;
        case EFAULT:          cout << "错误的地址" << endl; break;
        case EBUSY:           cout << "设备或资源忙" << endl; break;
        case EEXIST:          cout << "文件已存在" << endl; break;
        case EXDEV:           cout << "跨设备链接" << endl; break;
        case ENODEV:          cout << "没有这样的设备" << endl; break;
        case ENOTDIR:         cout << "非目录路径" << endl; break;
        case EISDIR:          cout << "该路径是目录" << endl; break;
        case ENFILE:          cout << "系统打开的文件过多" << endl; break;
        case EMFILE:          cout << "打开的文件过多" << endl; break;
        case ENOTTY:          cout << "不适当的 I/O 控制操作" << endl; break;
        case EFBIG:           cout << "文件过大" << endl; break;
        case ENOSPC:          cout << "设备上没有空间" << endl; break;
        case ESPIPE:          cout << "非法的 seek 操作" << endl; break;
        case EROFS:           cout << "只读文件系统" << endl; break;
        case EMLINK:          cout << "链接过多" << endl; break;
        case EPIPE:           cout << "破损的管道" << endl; break;
        case EDOM:            cout << "数学参数超出函数定义域" << endl; break;
        case EDEADLK:         cout << "资源死锁避免" << endl; break;
        case ENAMETOOLONG:    cout << "文件名太长" << endl; break;
        case ENOLCK:          cout << "无法获取文件锁" << endl; break;
        case ENOSYS:          cout << "函数未实现" << endl; break;
        case ENOTEMPTY:       cout << "目录非空" << endl; break;
    }
    /* 清除错误标记 */
    u.u_error = 0;
}

void Command::help()
{
    cout << name << " <" << description << ">" << endl;
    cout << "Usage:";
    for (int i = 0; i < usage.size(); i++) {
        cout << "\t" << usage[i] << "\n";
    }
}

void Command_ls::execute(vector<string> args) {
    string path;
    User& u = OSKernel::Instance().GetUser();
    bool hidden = true;
    int mode = 0;

    /* 解析参数 */
    for (int i = 0; i < args.size(); i++) {
        string arg = args[i];
        if (arg == "-a")
            hidden = false;
        else if (arg[0] == '-') {
            help();
            return;
        }
        else {
            if (path == "")
                path = arg;
            /* 多个参数 意义不明 */
            else {
                help();
                return;
            }
        }
    }

    DiskInode inode;
    Sys_Stat(path.c_str(), &inode);
    if (u.u_error) {
        return;
    }
    else if ((inode.d_mode & Inode::IFMT) != Inode::IFDIR) {
        cout << "给定路径不是文件夹！" << endl;
        return;
    }

    int file = Sys_Open(path.c_str(), File::FREAD);

    unsigned char buffer[sizeof(DirectoryEntry)];

    DirectoryEntry temp;

    while (Sys_Read(file, buffer, sizeof(DirectoryEntry)))
    {
        memcpy(&temp, buffer, sizeof(DirectoryEntry));
        if (temp.m_ino == 0)
            continue;
        else if (hidden && temp.m_name[0] == '.')
            continue;
        cout << temp.m_name << "\t";
    }

    Sys_Close(file);

    if (!u.u_error)
        cout << endl;
}

void Command_cd::execute(vector<string> args)
{
    if (args.size() != 1 || (args.size() == 1 && args[0][0] == '-')) {
        help();
        return;
    }

    Sys_ChDir(args[0].c_str());
}

void Command_cp::execute(vector<string> args)
{
    if (args.size() != 2) {
        help();
        return;
    }

    User& u = OSKernel::Instance().GetUser();
    bool s_out, d_out;
    fstream src, dst;
    int s_fd, d_fd;

    /* 处理src */
    if (args[0][0] == '$') {
        s_out = true;
        src.open(args[0].substr(1), ios::in | ios::binary);
        if (!src) {
            cout << "src: 外部文件不存在" << endl;
            return;
        }
    }
    else {
        s_out = false;
        s_fd = Sys_Open(args[0].c_str(), File::FREAD);
        if (u.u_error) {
            cout << "src: ";    /* 返回后handleUserError会处理 */
            return;
        }
    }

    /* 处理dst */
    if (args[1][0] == '$') {
        d_out = true;
        dst.open(args[1].substr(1), ios::out | ios::trunc | ios::binary);
        if (!dst) {
            cout << "dst: 外部文件创建失败" << endl;
            return;
        }
    }
    else {
        d_out = false;
        d_fd = Sys_Creat(args[1].c_str());
        if (u.u_error) {
            cout << "dst: ";    /* 返回后handleUserError会处理 */
            return;
        }
    }

    /* 一个Buffer为单位进行传输 */
    char* buffer = new char[BUF_SIZE];

    while (true) {
        int count;

        if (s_out) {
            src.read(buffer, BUF_SIZE);
            count = src.gcount();
        }
        else {
            count = Sys_Read(s_fd, (unsigned char*)buffer, BUF_SIZE);
        }

        if (count == 0)
            break;

        if (d_out)
            dst.write(buffer, count);
        else
            Sys_Write(d_fd, (unsigned char*)buffer, count);
    }

    if (s_out)
        src.close();
    else
        Sys_Close(s_fd);

    if (d_out)
        dst.close();
    else
        Sys_Close(d_fd);

    delete[] buffer;
    return;
}


void Command_mv::execute(vector<string> args)
{
    if (args.size() != 2) {
        help();
        return;
    }

    if (args[0] == args[1])
        return;

    // 先执行cp
    Command_cp cp;
    cp.execute(args);

    // 若cp错误则不再删除
    User& u = OSKernel::Instance().GetUser();
    if (u.u_error)
        return;

    // cp成功则删除原文件
    Command_fdelete fdelete;
    fdelete.execute({ vector<string>(1, args[0]) });
}



void Command_mkdir::execute(vector<string> args)
{
    if (args.size() != 1 || (args.size() == 1 && args[0][0] == '-')) {
        help();
        return;
    }

    Sys_MkNod(args[0].c_str());
}

void Command_fformat::execute(vector<string> args)
{
    OSKernel& o = OSKernel::Instance();

    o.GetFileSystem().FormatDisk();
    o.Restart();        /* 重启整个Kernel，这样能关闭打开的Openfile结构，重置curdir等*/
}

void Command_fcreat::execute(vector<string> args)
{
    if (args.size() != 1 || (args.size() == 1 && args[0][0] == '-')) {
        help();
        return;
    }

    int fd = Sys_Creat(args[0].c_str());

    User& u = OSKernel::Instance().GetUser();
    if (!u.u_error)
        cout << "fd: " << fd << endl;
}


void Command_fdelete::execute(vector<string> args)
{
    if (args.size() != 1 || (args.size() == 1 && args[0][0] == '-')) {
        help();
        return;
    }

    Sys_Unlink(args[0].c_str());

    return;
}

void Command_fopen::execute(vector<string> args)
{
    string path;
    int mode = 0;

    /* 解析参数 */
    for (int i = 0; i < args.size(); i++) {
        string arg = args[i];

        if (arg == "-r") 
            mode |= File::FREAD;
        else if (arg == "-w") 
            mode |= File::FWRITE;
        else if(arg[0] == '-') {
            help();
            return;
        }
        else {
            if (path == "")
                path = arg;
            /* 多个参数 意义不明 */
            else {
                help();
                return;
            }
        }
    }

    if (path == "") {
        help();
        return;
    }

    if (mode == 0) {
        cout << "必须指定至少一种打开方式" << endl;
        return;
    }

    int fd = Sys_Open(path.c_str(), mode);

    User& u = OSKernel::Instance().GetUser();
    if (!u.u_error)
        cout << "fd: " << fd << endl;
}

void Command_fclose::execute(vector<string> args)
{
    if (args.size() != 1 || (args.size() == 1 && args[0][0] == '-')) {
        help();
        return;
    }

    int fd;
    istringstream ss1 = istringstream(args[0]);
    ss1 >> fd;
    if (ss1.fail()) {
        cout << "文件描述符fd非法" << endl;
        return;
    }

    Sys_Close(fd);
}

void Command_fread::execute(vector<string> args)
{
    if (!(args.size() == 2 || (args.size() == 4 && args[2] == ">>"))) {
        help();
        return;
    }

    int fd, count;

    istringstream ss1 = istringstream(args[0]);
    ss1 >> fd;
    if (ss1.fail()) {
        cout << "文件描述符fd非法" << endl;
        return;
    }
    istringstream ss2 = istringstream(args[1]);
    ss2 >> count;
    if (ss2.fail()) {
        cout << "读入字节数非法" << endl;
        return;
    }
    
    unsigned char* buffer = new unsigned char[count + 1];
    count = Sys_Read(fd, buffer, count);

    User& u = OSKernel::Instance().GetUser();
    if (!u.u_error) {
        buffer[count] = 0;

        if (!count) {
            delete[] buffer;
            return;
        }

        if (args.size() == 2)
            cout << buffer << endl;
        else {
            str_set[args[3]] = string((char *)buffer);
        }
    }

    delete[] buffer;
}


void Command_fwrite::execute(vector<string> args)
{
    if (!(args.size() == 2 || (args.size() == 3 && args[1] == "<<"))) {
        help();
        return;
    }

    int fd, count;
    istringstream ss1 = istringstream(args[0]);
    ss1 >> fd;
    if (ss1.fail()) {
        cout << "文件描述符fd非法" << endl;
        return;
    }

    char* buffer;
    if (args.size() == 2) {
        count = args[1].size();
        buffer = new char[count + 1]; // 这里算上尾零 但是不写入文件
        strcpy(buffer, args[1].c_str());
    }
    else{
        if (str_set.count(args[2]) == 0) {
            cout << "输入的字符串不存在，请先通过fread定义" << endl;
            return;
        }
        string str = str_set[args[2]];
        count = str.size();
        buffer = new char[count + 1]; // 这里算上尾零 但是不写入文件
        strcpy(buffer, str.c_str());
    }

    Sys_Write(fd, (unsigned char *)buffer, count);

    delete[] buffer;
}


void Command_flseek::execute(vector<string> args)
{
    /* 三部分 fd offset 和 模式 */
    if (args.size() != 3) {
        help();
        return;
    }

    int fd, offset;
    istringstream ss1 = istringstream(args[0]);
    ss1 >> fd;
    if (ss1.fail()) {
        cout << "文件描述符fd非法" << endl;
        return;
    }
    istringstream ss2 = istringstream(args[1]);
    ss2 >> offset;
    if (ss2.fail()) {
        cout << "读入字节数非法" << endl;
        return;
    }

    int mode;
    if (args[2] == "-b")
        mode = 0;
    else if (args[2] == "-c")
        mode = 1;
    else if (args[2] == "-e")
        mode = 2;
    else {
        help();
        return;
    }

    Sys_Seek(fd, offset, mode);
}


void _traverse_tree(vector<bool> pre_print, string path)
{
    int file = Sys_Open(path.c_str(), File::FREAD);

    unsigned char buffer[sizeof(DirectoryEntry)];
    DirectoryEntry temp;

    vector<string> files;

    while (Sys_Read(file, buffer, sizeof(DirectoryEntry)))
    {
        memcpy(&temp, buffer, sizeof(DirectoryEntry));
        if (temp.m_ino == 0)
            continue;
        else if (temp.m_name[0] == '.')
            continue;
        files.push_back(temp.m_name);
    }

    for (int i = 0; i < files.size(); i++) {
        string file = files[i];
        DiskInode inode;
        for (auto pre : pre_print) {
            cout << (pre ? "│" : " ") << "  ";
        }
        cout << ((i == files.size()-1) ? "└─" : "├─") << file << endl;
        Sys_Stat((path + "/" + file).c_str(), &inode);
        if ((inode.d_mode & Inode::IFMT) == Inode::IFDIR) {
            vector<bool> p = pre_print;
            p.push_back(i != files.size() - 1);
            _traverse_tree(p, path + "/" + file);
        }
    }

    Sys_Close(file);
}

void Command_tree::execute(vector<string> args)
{
    string path = ".";
    User& u = OSKernel::Instance().GetUser();
    
    if (args.size() > 1) {
        help();
        return;
    }
    else if (args.size() == 1) {
        path = args[0];
    }

    DiskInode inode;
    Sys_Stat(path.c_str(), &inode);
    if (u.u_error) {
        return;
    }
    else if ((inode.d_mode & Inode::IFMT) != Inode::IFDIR) {
        cout << "给定路径不是文件夹！" << endl;
        return;
    }

    cout << path << endl;
    _traverse_tree({}, path);

    if (!u.u_error)
        cout << endl;
}
