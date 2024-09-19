#include "Logger.h"

Logger::Logger()
{
    // 打开日志文件
    logfile.open("logfile.txt", std::ios::out | std::ios::app);
    if (!logfile.is_open()) {
        std::cerr << "Failed to open log file!" << std::endl;
    }
    logfile << "============Starting============\n";
}

Logger::~Logger()
{
    logfile << "============Ending============\n";
    if (logfile.is_open()) {
        logfile.close();
    }
}

Logger& Logger::err()
{
    static Logger logger;
    logger.log("[ERROR] ");
    return logger;
}

Logger& Logger::warning()
{
    static Logger logger;
    logger.log("[WARNING] ");
    return logger;
}

Logger& Logger::info()
{
    static Logger logger;
    logger.log("[INFO] ");
    return logger;
}

void Logger::log(const std::string& message)
{
    if (logfile.is_open()) {
        logfile << getCurrentTime() << message;
    }
    else {
        std::cerr << "Log file is not open!";
    }
}

std::string Logger::getCurrentTime()
{
    std::time_t now = std::time(nullptr);
    std::tm* local_time = std::localtime(&now);

    char buffer[80];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", local_time);
    return std::string(buffer);
}