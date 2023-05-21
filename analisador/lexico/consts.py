DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
UPPER_LETTERS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
LOWER_LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'} 
COMMA = {','}
SEMICOLON = {';'}
COLON = {':'}
EXCL_MARK = {'!'}
BACKSLASH = {'\\'}
FORWARD_SLASH = {'/'}
STAR = {'*'}
PLUS_SIGN = {'+'}
MINUS_SIGN = {'-'}
OPEN_PARENTHESIS = {'('}
CLOSE_PARENTHESIS = {')'}
OPEN_BRACE = {'{'}
CLOSE_BRACE = {'}'}
OPEN_BRACKET = {'['}
CLOSE_BRACKET = {']'}
GREATER_THAN = {'>'}
LESS_THAN = {'<'}
EQUAL = {'='}
PERIOD = {'.'}
QUOTE = {'\''}
DOUBLE_QUOTE = {'"'}
UNDERLINE = {'_'}
NL = {'\n'}
TAB = {'\t'}
SPACE = {' '}
POWER = {'E', 'e'}
EOF = {''}
LETTERS = UPPER_LETTERS | LOWER_LETTERS
ARITHMETIC_OPERATORS = PLUS_SIGN | MINUS_SIGN | STAR | FORWARD_SLASH
UNION_ALPHABET = DIGITS | LETTERS | COMMA | SEMICOLON | COLON | EXCL_MARK | BACKSLASH | STAR | PLUS_SIGN | MINUS_SIGN | FORWARD_SLASH | OPEN_PARENTHESIS | CLOSE_PARENTHESIS | OPEN_BRACE | CLOSE_BRACE | OPEN_BRACKET | CLOSE_BRACKET | GREATER_THAN | LESS_THAN | EQUAL | PERIOD | QUOTE | DOUBLE_QUOTE | UNDERLINE | NL | TAB | SPACE | POWER | EOF

alphabet_dictionary = {
    "DIGITS": DIGITS,
    "UPPER_LETTERS": UPPER_LETTERS,
    "LOWER_LETTERS": LOWER_LETTERS,
    "COMMA": COMMA,
    "SEMICOLON": SEMICOLON,
    "COLON": COLON,
    "EXCL_MARK": EXCL_MARK,
    "BACKSLASH": BACKSLASH,
    "FORWARD_SLASH": FORWARD_SLASH,
    "STAR": STAR,
    "PLUS_SIGN": PLUS_SIGN,
    "MINUS_SIGN": MINUS_SIGN,
    "OPEN_PARENTHESIS": OPEN_PARENTHESIS,
    "CLOSE_PARENTHESIS": CLOSE_PARENTHESIS,
    "OPEN_BRACE": OPEN_BRACE,
    "CLOSE_BRACE": CLOSE_BRACE,
    "OPEN_BRACKET": OPEN_BRACKET,
    "CLOSE_BRACKET": CLOSE_BRACKET,
    "GREATER_THAN": GREATER_THAN,
    "LESS_THAN": LESS_THAN,
    "EQUAL": EQUAL,
    "PERIOD": PERIOD,
    "QUOTE": QUOTE,
    "DOUBLE_QUOTE": DOUBLE_QUOTE,
    "UNDERLINE": UNDERLINE,
    "NL": NL,
    "TAB": TAB,
    "SPACE": SPACE,
    "POWER": POWER,
    "EOF": EOF,
    "LETTERS": LETTERS,
    "ARITHMETIC_OPERATORS": ARITHMETIC_OPERATORS,
    "UNION_ALPHABET": UNION_ALPHABET,
    "AB_WITHOUT_DOUBLE_QUOTE": UNION_ALPHABET - DOUBLE_QUOTE - EOF,
    "AB_WITHOUT_CL_BRACE": UNION_ALPHABET - CLOSE_BRACE - EOF
}

state_token_type_map = {
        "ART_OP": ("OPM", "Nulo"),
        "ASSIGN": ("RCB", "Nulo"),
        "CL_PAR": ("FC_P", "Nulo"),
        "COMMA": ("VIR", "Nulo"),
        "COMMENT_2": ("Comentário", "Nulo"),
        "EOF": ("EOF", "Nulo"),
        "ID": ("id", "Nulo"),
        "INT": ("Num", "inteiro"),
        "LIT_2": ("LIT", "literal"),
        "NL": ("Ignorar", "Nulo"),
        "OP_PAR": ("AB_P", "Nulo"),
        "REAL_3": ("Num", "real"),
        "REAL_5": ("Num", "real"),
        "REL_OP_1": ("OPR", "Nulo"),
        "REL_OP_2": ("OPR", "Nulo"),
        "REL_OP_3": ("OPR", "Nulo"),
        "S_COL": ("PT_V", "Nulo"),
        "SPACE": ("Ignorar", "Nulo"),
        "TAB": ("Ignorar", "Nulo"),
    }

reserved_words = {"inicio", "varinicio", "varfim", "escreva", "leia", "se", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"}

