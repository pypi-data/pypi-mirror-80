class CLIError(RuntimeError):
    def __init__(self, message="Unknown error occurred", exit_code=1):
        self.message = message
        self.exit_code = exit_code
