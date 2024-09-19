#pragma once
#ifndef LOGGER_H
#define LOGGER_H

#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <fstream>
#include <string>

class Logger {
private:
    std::ofstream logfile;

public:
    enum class Level { INFO, WARNING, ERROR };

    Logger();
    ~Logger();

    template<typename T>
    Logger& operator<<(const T& message)
    {
        if (logfile.is_open()) {
            logfile << message;
            logfile.flush();
        }
        else {
            std::cerr << "Log file is not open!" << std::endl;
        }
        return *this;
    }

    static Logger& err();
    static Logger& warning();
    static Logger& info();

private:
    void log(const std::string& message);
    std::string getCurrentTime();
};

#endif // LOGGER_H
