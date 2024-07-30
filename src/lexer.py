import logging
from typing import List, Union

logger = logging.getLogger(__name__)

class Token:
    class Identifier:
        def __init__(self, value: str):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, Token.Identifier) and self.value == other.value

        def __repr__(self):
            return f'Identifier("{self.value}")'

    EOF = 'EOF'
    LEFT_SQUIRLY = '{'
    RIGHT_SQUIRLY = '}'
    SEMICOLON = ';'
    UNKNOWN = 'UNKNOWN'
    START = 'START'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    POUND = '#'
    NEW_LINE = '\n'

class Lexer:
    def __init__(self, source: str):
        self.source = list(source)
        self.position = 0
        self.read_position = 0
        self.character = self.source[0] if self.source else ''
        self.end = len(self.source)

    def read_char(self):
        if self.read_position >= len(self.source):
            self.character = ''
        else:
            self.character = self.source[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek(self) -> str:
        return self.source[self.read_position] if self.read_position < len(self.source) else ''

    def tokenize(self) -> List[Union[Token.Identifier, str]]:
        tokens = []
        while True:
            token = self.next_token()
            if token == Token.EOF:
                break
            tokens.append(token)
        return tokens

    def next_token(self):
        self.skip_whitespace()
        if self.position == self.end:
            return Token.EOF
        if self.character.isalnum() or self.character in '"-^<*./\\':
            return Token.Identifier(self.read_identifier())
        if self.character == '{':
            self.read_char()  # Move past the '{'
            return Token.LEFT_SQUIRLY
        if self.character == '}':
            self.read_char()  # Move past the '}'
            return Token.RIGHT_SQUIRLY
        if self.character == ';':
            self.read_char()  # Move past the ';'
            return Token.SEMICOLON
        if self.character == '[':
            self.read_char()  # Move past the '['
            return Token.LEFT_BRACKET
        if self.character == ']':
            self.read_char()  # Move past the ']'
            return Token.RIGHT_BRACKET
        if self.character == '#':
            self.read_char()  # Move past the '#'
            return Token.POUND
        if self.character == '\n':
            self.read_char()  # Move past the '\n'
            return Token.NEW_LINE
        self.read_char()  # Move past the unknown character
        return Token.UNKNOWN

    def skip_whitespace(self):
        while self.character.isspace() and self.character != '\n':
            self.read_char()

    def read_identifier(self) -> str:
        start = self.position
        if self.character == '"':
            self.read_char()
            while self.character != '"':
                self.read_char()
            self.read_char()  # Move past the closing '"'
        else:
            while not self.character.isspace() and self.character not in {'{', '}', ';', '[', ']', '#', '\n'}:
                self.read_char()
        word = ''.join(self.source[start:self.read_position])
        return word.strip()