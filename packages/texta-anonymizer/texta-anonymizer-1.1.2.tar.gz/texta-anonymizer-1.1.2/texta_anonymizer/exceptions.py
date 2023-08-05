
class InvalidInputError(Exception):
    def __init__(self, exit_code, msg):
        super().__init__()
        self.exit_code = exit_code
        self.msg = msg
