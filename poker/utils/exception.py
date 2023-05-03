from poker.utils.constants import INCREMENT_LIMIT, Cash


class IncrementException(BaseException):

    def __init__(self):
        self.message = f"value should be less than {INCREMENT_LIMIT}"
        super().__init__(self.message)


class CashException(BaseException):

    def __init__(self):
        self.message = f"invalid value. Acceptable values are {', '.join([f'${str(item.value)}' for item in Cash])}"
        super().__init__(self.message)


class NegativeException(BaseException):

    def __init__(self):
        self.message = "value should be greater than 0"
        super().__init__(self.message)


class RangeException(BaseException):
    
    def __init__(self):
        self.message = "value falls outside range"
        super().__init__(self.message)


class GamePlayException(BaseException):

    def __init__(self):
        self.message = f"Please enter 'Yes' or 'No'"
        super().__init__(self.message)


class NotReadyException(BaseException):
    pass


class InvalidActionException(BaseException):
    pass


class InsufficientChipException(BaseException):
    pass