from poker.utils.constants import INCREMENT_LIMIT, Cash


class IncrementException(BaseException):

    def __init__(self):
        self.message = f"Value should be less than {INCREMENT_LIMIT}."
        super().__init__(self.message)


class CashException(BaseException):

    def __init__(self):
        self.message = f"Invalid value. Acceptable values are {', '.join([f'{str(item.value)}' for item in Cash])}."
        super().__init__(self.message)


class NegativeException(BaseException):

    def __init__(self):
        self.message = "Value should be greater than 0."
        super().__init__(self.message)


class RangeException(BaseException):
    
    def __init__(self):
        self.message = "Value falls outside range."
        super().__init__(self.message)


class InvalidActionException(BaseException):
    
    def __init__(self, valid_actions: list[str]):
        self.message = f"Invalid action. Acceptable values are {', '.join(action for action in valid_actions)}."
        super().__init__(self.message)


class InsufficientChipException(BaseException):
    
    def __init__(self, chip_count: int):
        self.message = f"You only have {chip_count}. Please select a different amount."
        super().__init__(self.message)