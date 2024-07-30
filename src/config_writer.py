from .lexer import Lexer, Token
from .utils import build_string
import logging

logger = logging.getLogger(__name__)

class ConfigWriter:
    def __init__(self, config: str):
        lexer = Lexer(config)
        self.tokens = lexer.tokenize()
        logger.debug("Tokenization done!!")
        logger.info(f"{self.tokens}")
        self.token = Token.START
        self.position = 0
        self.read_position = 0
        self.output = []

    def write_configs(self) -> str:
        self.read_token()
        stanza_stack_record = []
        stanza_stack = []
        stanza_pointer = 0
        config_line_stack = []
        inside_bracket_array = False
        next_inactive = False
        next_protect = False

        while self.token != Token.EOF:
            logger.debug(f"write_configs: {self.read_position} {self.token}")
            if self.token == Token.LEFT_SQUIRLY:
                logger.debug("LeftSquirly")
                if next_inactive:
                    addition = build_string(stanza_stack_record, config_line_stack).replace("set", "deactivate")
                    self.output.append(addition)
                    next_inactive = False
                elif next_protect:
                    addition = build_string(stanza_stack_record, config_line_stack).replace("set", "protect")
                    self.output.append(addition)
                    next_protect = False
                stanza_pointer += 1
                stanza_stack_record.append(list(stanza_stack))
                stanza_stack.clear()
                config_line_stack.clear()
            elif self.token == Token.LEFT_BRACKET:
                logger.debug("LeftBracket")
                inside_bracket_array = True
            elif self.token == Token.RIGHT_BRACKET:
                logger.debug("RightBracket")
                inside_bracket_array = False
                config_line_stack.clear()
            elif self.token == Token.SEMICOLON:
                logger.debug("Semicolon")
                if self.tokens[self.read_position - 2] == Token.RIGHT_BRACKET:
                    stanza_stack.clear()
                config_line_stack.clear()
            elif self.token == Token.RIGHT_SQUIRLY:
                logger.debug("RightSquirly")
                stanza_pointer -= 1
                stanza_stack.clear()
                stanza_stack_record.pop()
            elif self.token == Token.POUND:
                logger.debug("Pound")
                self.move_past_comment()
            elif isinstance(self.token, Token.Identifier):
                logger.debug("Identifier")
                statement = self.token.value
                if statement.endswith(';'):
                    config_line_stack.append(statement)
                    addition = build_string(stanza_stack_record, config_line_stack)
                    if next_inactive:
                        deactivate = addition.replace("set", "deactivate")
                        next_inactive = False
                        self.output.append(addition)
                        self.output.append(deactivate)
                    elif next_protect:
                        protect = addition.replace("set", "protect")
                        next_protect = False
                        self.output.append(addition)
                        self.output.append(protect)
                    else:
                        self.output.append(addition)
                    config_line_stack.clear()
                    stanza_stack.clear()
                elif inside_bracket_array:
                    config_line_stack.append(statement)
                    addition = build_string(stanza_stack_record, config_line_stack)
                    self.output.append(addition)
                    config_line_stack.pop()
                elif statement == "inactive:":
                    next_inactive = True
                elif statement == "protect:":
                    next_protect = True
                elif statement == "replace:":
                    pass
                else:
                    logger.debug(f"non terminating statement {statement}")
                    stanza_stack.append(statement)
                    config_line_stack.append(statement)
            else:
                logger.debug(f"hit default case for {self.token}")

            self.read_token()
            logger.debug(f"stanza_stack {stanza_stack}")
            logger.debug(f"stanza_pointer {stanza_pointer}")
            logger.debug(f"stanza_stack_record {stanza_stack_record}")
            logger.debug(f"config_line_stack {config_line_stack}")

        return "\n".join(self.output)

    def read_token(self):
        if self.read_position >= len(self.tokens):
            self.token = Token.EOF
        else:
            self.token = self.tokens[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def move_past_comment(self):
        logger.info("move_past_comment")
        while True:
            next_token = self.tokens[self.read_position]
            if next_token == Token.NEW_LINE or next_token == Token.RIGHT_SQUIRLY:
                break

            if isinstance(next_token, Token.Identifier):
                statement = next_token.value
                if statement.endswith(';'):
                    break

            self.token = self.tokens[self.read_position]
            logger.info(f"skip {self.token}")
            self.position = self.read_position
            self.read_position += 1
