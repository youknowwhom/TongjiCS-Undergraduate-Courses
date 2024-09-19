import time
import sys
import os
import multiprocessing
from time import sleep
import json
import copy
import mimetypes

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, QThread, Qt
from PyQt5.QtWebChannel import QWebChannel

from aiohttp import web

from myParser import Parser
from myLexer import Lexer
from myBlockDivider import BlockDivider
from myCodeGenerator import CodeGenerator
from tokenType import tokenType

mimetypes.add_type("application/javascript", ".js", True)
serverPort = 9099
serverDirectory = "dist/frontend"


os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"


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
    def setParser(self, parser: Parser):
        self.parser = parser
        delta = time.time() - self.parser_init_begin
        print(f"self.parser is set to {self.parser}")
        print(f"Parser took {delta} seconds to initialize")
        self.goto_table = self.parser.getGotoTable()
        self.action_table = self.parser.getActionTable()
        self.parent().page().runJavaScript("window.cpf.flush();")

    @pyqtSlot(str, result=str)
    def process(self, code_str):
        self.lexer.lines = code_str.splitlines()
        # 此处用于显示高亮，还是沿用原先对源代码扫描一遍
        # 语法分析器独立地调用lexer得token
        token_list, lexer_success = self.getLex()
        if lexer_success:
            parse_result = self.getParse(code_str.splitlines())     # 独立调用，一遍扫描源代码
            return json.dumps(
                {
                    "lexer": self.dumpTokenList(token_list),
                    "lexer_success": lexer_success,
                    **parse_result,
                }
            )
        else:
            msg = "词法分析出现错误，后续步骤已取消"
            errors = []
            for t in token_list:
                if t["prop"] == tokenType.UNKNOWN:
                    print(t)
                    errors.append(
                        "Error at ({},{}): 无法识别的字符/字符串".format(
                            t["loc"]["row"], t["loc"]["col"]
                        )
                    )
            return json.dumps(
                {
                    "lexer": self.dumpTokenList(token_list),
                    "lexer_success": lexer_success,
                    "ast": {
                        "root": msg,
                        "err": "lexer_error",
                    },
                    "goto": [[msg]],
                    "action": [[msg]],
                    "process": [[msg]],
                    "semantic_quaternation": [[msg]],
                    "semantic_error_occur": True,
                    "semantic_error_message": errors,
                }
            )

    def dumpTokenList(self, token_list):
        def dumpToken(r):
            r["prop"] = r["prop"].value
            return r

        return list(map(dumpToken, token_list))

    def getParse(self, codes):
        if self.parser is not None:
            parsed_result = self.parser.getParse(codes)
            print(self.parser.semantic.quaternion_table)
            if not self.parser.semantic_error_occur:
                blockDivider = BlockDivider(self.parser.semantic.quaternion_table)
                blockDivider.computeBlocks(self.parser.semantic.getFuncTable())
                codeGenerator = CodeGenerator(blockDivider.func_blocks, self.parser.semantic.process_table, self.parser.semantic.words_table)
                codes = codeGenerator.getObjectCode()
                with open("./code.asm", "w") as f:
                    f.write("\n".join(codes))
                code_error_occur = codeGenerator.error_occur
                code_error_msg = codeGenerator.error_msg
            else:
                code_error_occur = False
                code_error_msg = []
                codes = []
            return {
                "ast": parsed_result,
                "goto": self.goto_table,
                "action": self.action_table,
                "process": self.parser.parse_process_display,
                "semantic_quaternation": self.parser.semantic_quaternation,
                "semantic_error_occur": self.parser.semantic_error_occur or code_error_occur,
                "semantic_error_message": self.parser.semantic_error_message + code_error_msg,
                "code": [[code] for code in codes]
            }
        else:
            launching = "Parser正在启动，请稍等。"
            return {
                "ast": {
                    "token": launching,
                    "err": "parser_not_ready",
                },
                "goto": [[launching]],
                "action": [[launching]],
                "process": [[launching]],
                "semantic_quaternation": [[launching]],
                "semantic_error_occur": False,
                "semantic_error_message": [],
            }

    def getLex(self):
        return self.lexer.getLex()


class MainWindow(QWebEngineView):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load(QUrl(f"http://localhost:{serverPort}/index.html"))
        self.setWindowTitle("类C文法编译器")
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
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = MainWindow()
    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    multiprocessing.freeze_support()
    serverProcess = multiprocessing.Process(
        None, ServerProcess, args=(application_path,), name="server"
    )
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
