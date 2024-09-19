from enum import Enum

class tokenType(Enum):
    UNKNOWN = "unknown"
    S_COMMENT = "s_comment"
    LM_COMMENT = "lm_comment"
    RM_COMMENT = "rm_comment"
    IDENTIFIER = "identifier"
    INTEGER_CONSTANT = "integer_constant"
    FLOATING_POINT_CONSTANT = "floating_point_constant"
    EOF = "eof"
    L_PAREN = "l_paren"
    R_PAREN = "r_paren"
    L_BRACE = "l_brace"
    R_BRACE = "r_brace"
    STAR = "star"
    STAR_EQUAL = "starequal"
    PLUS = "plus"
    PLUS_EQUAL = "plusequal"
    MINUS = "minus"
    MINUS_EQUAL = "minusequal"
    PERCENT = "percent"
    PERCENT_EQUAL = "percentequal"
    EXCLAMATION_EQUAL = "exclaimequal"
    SLASH = "lash"
    SLASH_EQUAL = "slashequal"
    LESS = "less"
    LESS_EQUAL = "lessequal"
    LESS_LESS = "lessless"
    LESS_LESS_EQUAL = "lesslessequal"
    GREATER = "greater"
    GREATER_GREATER = "greatergreater"
    GREATER_EQUAL = "greaterequal"
    SEMI = "semi"
    EQUAL = "equal"
    EQUAL_EQUAL = "equalequal"
    COMMA = "comma"
    KW_ELSE = "kw_else"
    KW_IF = "kw_if"
    KW_INT = "kw_int"
    KW_FLOAT = "kw_float"
    KW_RETURN = "kw_return"
    KW_VOID = "kw_void"
    KW_WHILE = "kw_while"

tokenSymbols = {
    "=": tokenType.EQUAL,
    "+": tokenType.PLUS,
    "+=": tokenType.PLUS_EQUAL,
    "-": tokenType.MINUS,
    "-=": tokenType.MINUS_EQUAL,
    "*": tokenType.STAR,
    "*=": tokenType.STAR_EQUAL,
    "/": tokenType.SLASH,
    "/=": tokenType.SLASH_EQUAL,
    "%": tokenType.PERCENT,
    "%=": tokenType.PERCENT_EQUAL,
    "==": tokenType.EQUAL_EQUAL,
    ">": tokenType.GREATER,
    ">>": tokenType.GREATER_GREATER,
    ">>=": tokenType.GREATER_EQUAL,
    ">=": tokenType.GREATER_EQUAL,
    "<": tokenType.LESS,
    "<<": tokenType.LESS_LESS,
    "<<=": tokenType.LESS_LESS_EQUAL,
    "<=": tokenType.LESS_EQUAL,
    "!=": tokenType.EXCLAMATION_EQUAL,
    ";": tokenType.SEMI,
    ",": tokenType.COMMA,
    "#": tokenType.EOF,
    "(": tokenType.L_PAREN,
    ")": tokenType.R_PAREN,
    "{": tokenType.L_BRACE,
    "}": tokenType.R_BRACE,
    "//": tokenType.S_COMMENT,
    "/*": tokenType.LM_COMMENT,
    "*/": tokenType.RM_COMMENT,
}

tokenKeywords = {
    "int": tokenType.KW_INT,
    "float": tokenType.KW_FLOAT,
    "void": tokenType.KW_VOID,
    "if": tokenType.KW_IF,
    "else": tokenType.KW_ELSE,
    "return": tokenType.KW_RETURN,
    "while": tokenType.KW_WHILE,
}

tokenOthers = {
    "identifier": tokenType.IDENTIFIER,
    "integer_constant": tokenType.INTEGER_CONSTANT,
    "floating_point_constant": tokenType.FLOATING_POINT_CONSTANT
}


def tokenType_to_terminal(tokenType: tokenType) -> str:
    for key, value in tokenKeywords.items():
        if value == tokenType:
            return key
    for key, value in tokenSymbols.items():
        if value == tokenType:
            return key
    # 如identifier、numeric_constant并非固定的terminal，直接返回对应的字符串名
    return tokenType.value
