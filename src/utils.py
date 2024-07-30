import logging

logger = logging.getLogger(__name__)

def build_string(stanza_stack_record, config_line_stack) -> str:
    new_string = "set"

    for vec in stanza_stack_record:
        for string in vec:
            new_string += f" {string}"
    for string in config_line_stack:
        new_string += f" {string}"

    if new_string.endswith(";"):
        new_string = new_string[:-1]
    logger.info(f"config_line:\n{new_string}")
    return new_string
