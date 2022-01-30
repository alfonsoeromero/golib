class ParseError(Exception):
    """Exception thrown when a parsing error occurred"""

    def __init__(self, msg, lineno=1):
        Exception.__init__(f"{msg} near line {lineno}")
        self.lineno = lineno
