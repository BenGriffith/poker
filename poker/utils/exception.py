from poker.utils.constants import INCREMENT_LIMIT, Cash


class IncrementException(BaseException):

    def __init__(self):
        self.message = f"value should be less than {INCREMENT_LIMIT}"
        super().__init__(self.message)


class CashException(BaseException):

    def __init__(self):
        self.message = f"invalid value. Acceptable values are {', '.join([f'${str(item.value)}' for item in Cash])}"
        super().__init__(self.message)