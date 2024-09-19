#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include "OSKernel.h"


class Command {
public:
	string name;
	string description;
	vector<string> usage;

	Command(string n, string d, vector<string> u) :name(n), description(d), usage(u) {};
	virtual ~Command() {};
	virtual void execute(vector<string>) = 0;
	void help();
};


class Shell {
	static const int NCOMMAND = 100;
	Command* commands[NCOMMAND] = {};	/* 存放所有command */
public:
	Shell();
	~Shell();
	void interface();
private:
	void handleUserError();
};


/* 具体Command */

class Command_ls: public Command {
public:
	Command_ls() :Command("ls", "列出路径下所有文件", { "ls (current path)", "ls <path>", "-a 全部展示"}) {};
	void execute(vector<string>);
};

class Command_cd : public Command {
public:
	Command_cd() :Command("cd", "切换当前目录", { "cd <path>" }) {};
	void execute(vector<string>);
};

class Command_cp : public Command {
public:
	Command_cp() :Command("cp", "复制文件(支持文件系统内外复制)", { "cp <src> <dst>", "为表区分，请在外部路径前加'$'"}) {};
	void execute(vector<string>);
};

class Command_mv : public Command {
public:
	Command_mv() :Command("mv", "移动文件", { "mv <old_path <new_path>" }) {};
	void execute(vector<string>);
};

class Command_mkdir : public Command {
public:
	Command_mkdir() :Command("mkdir", "新建目录项", { "mkdir <path>" }) {};
	void execute(vector<string>);
};

class Command_fformat : public Command{
public:
	Command_fformat() :Command("fformat", "格式化磁盘", { "fformat" }) {};
	void execute(vector<string>);
};

class Command_fcreat : public Command {
public:
	Command_fcreat() :Command("fcreat", "新建文件", { "fcreat <path>", "返回文件描述符"}) {};
	void execute(vector<string>);
};

class Command_fdelete : public Command {
public:
	Command_fdelete() :Command("fdelete", "删除文件", { "fdelete <path>" }) {};
	void execute(vector<string>);
};

class Command_fopen : public Command {
public:
	Command_fopen() :Command("fopen", "打开文件", { "fopen <path> -<mode>", "-r 读模式", "-w 写模式", "返回文件描述符"}) {};
	void execute(vector<string>);
};

class Command_fclose : public Command {
public:
	Command_fclose() :Command("fclose", "关闭文件", { "fclose <fd>"}) {};
	void execute(vector<string>);
};

class Command_fread : public Command {
public:
	Command_fread() :Command("fread", "读文件", {"fread <fd> <count> [>> <str> (写入到字符串中)]"}) {};
	void execute(vector<string>);
};

class Command_fwrite : public Command {
public:
	Command_fwrite() :Command("fwrite", "写文件", { "fwrite <fd> <str>\t从标准输入流写入", "fwrite <fd> << <str>\t从字符串中写入"}) {};
	void execute(vector<string>);
};

class Command_flseek : public Command {
public:
	Command_flseek() :Command("flseek", "调整文件读写指针", { "flseek <fd> <offset> -<mode>", "-b 相对文件头", "-c 相对当前位置", "-e 相对文件尾"}) {};
	void execute(vector<string>);
};

class Command_tree : public Command {
public:
	Command_tree() :Command("tree", "展示目录树", { "tree <path>" }) {};
	void execute(vector<string>);
};

