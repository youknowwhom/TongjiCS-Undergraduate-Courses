import time
import sys
import os
import multiprocessing
import threading
from time import sleep
import logging
import json

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWebChannel import QWebChannel

from aiohttp import web

from myParser import Parser
from myLexer import Lexer

serverPort = 9099
serverDirectory = "dist/frontend"


class ParserLauncher(QObject):
    returnParser = pyqtSignal(Parser)
    finished = pyqtSignal()

    def run(self):
        self.returnParser.emit(Parser())
        self.finished.emit()


class Compiler(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = Lexer()
        self.parser = None
        self.parser_init_begin = time.time()
        self.getParserNonBlock()

    def getParserNonBlock(self):
        self.pl_thread = QThread()
        self.pl_worker = ParserLauncher()
        self.pl_worker.moveToThread(self.pl_thread)
        self.pl_thread.started.connect(self.pl_worker.run)
        self.pl_worker.returnParser.connect(self.setParser)
        self.pl_worker.finished.connect(self.pl_thread.quit)
        self.pl_thread.finished.connect(self.pl_thread.deleteLater)
        self.pl_thread.start()

    @pyqtSlot(Parser)
    def setParser(self, parser):
        self.parser = parser
        delta = time.time() - self.parser_init_begin
        print(f"self.parser is set to {self.parser}")
        print(f"Parser took {delta} seconds to initialize")
        self.goto_table = self.parser.get_goto_table()
        self.action_table = self.parser.get_action_table()
        self.parent().page().runJavaScript("window.cpf.flush();")

    @pyqtSlot(str, result=str)
    def process(self, code_str):
        token_list, lexer_success = self.getLex(code_str)
        parse_result = self.getParse(token_list)
        return json.dumps(
            {
                "lexer": self.dumpTokenList(token_list),
                "lexer_success": lexer_success,
                **parse_result,
            }
        )

    def dumpTokenList(self, token_list):
        def dumpToken(r):
            r["prop"] = r["prop"].value
            return r

        return list(map(dumpToken, token_list))

    def getParse(self, token_list):
        if self.parser is not None:
            parsed_result = self.parser.getParse(token_list)
            return {
                "ast": parsed_result,
                "goto": self.goto_table,
                "action": self.action_table,
                "process": self.parser.parse_process_display,
            }
        else:
            launching = "Parser 正在启动，请稍等。"
            return {
                "ast": {
                    "root": launching,
                    "err": "parser_not_ready",
                },
                "goto": [[launching]],
                "action": [[launching]],
                "process": [[launching]],
            }

    def getLex(self, code_str: str):
        return self.lexer.getLex(code_str.splitlines())


class MainWindow(QWebEngineView):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load(QUrl(f"http://localhost:{serverPort}/index.html"))
        self.setWindowTitle("类C词法&文法分析器") 
        self.webChannel = QWebChannel(self.page())
        self.webChannel.registerObject("compiler", Compiler(self))
        self.page().setWebChannel(self.webChannel)


def ServerProcess(application_path):
    # serving local files
    app = web.Application()
    app.add_routes(
        [
            web.static(
                "/",
                os.path.join(application_path, serverDirectory),
                show_index=True,
                follow_symlinks=False,
                append_version=True,
            )
        ]
    )
    web.run_app(app, host="localhost", port=serverPort)


def QtProcess():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    multiprocessing.freeze_support()
    serverProcess = multiprocessing.Process(None, ServerProcess, args=(application_path,), name="server")
    windowProcess = multiprocessing.Process(None, QtProcess, name="window")
    serverProcess.start()
    print("started serverProcess")
    windowProcess.start()
    print("started windowProcess")
    while windowProcess.is_alive() and serverProcess.is_alive():
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
    serverProcess.terminate()
    print("killed serverProcess")
    windowProcess.terminate()
    print("killed windowProcess")
