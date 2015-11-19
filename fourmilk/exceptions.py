# coding=utf8


class Error(Exception):
    " 0 ~ 1000 System Error "
    BOOTSTRAP_ERROR = 0
    ARGUMENT_ERROR = 1

    " 1000 ~ fin User Error "
    USER_NOT_EXIST = 1000
    USER_EXISTED = 1001

    PART_NOT_EXIST = 1002
    PART_AMOUNT_ERROR = 1003

    translate = {
        BOOTSTRAP_ERROR: u'System Internal Error',
        ARGUMENT_ERROR: u'Argument Error',

        USER_NOT_EXIST: u'用户不存在',
        USER_EXISTED: u'用户已存在',
        PART_NOT_EXIST: u'零件不存在',
        PART_AMOUNT_ERROR: u'零件数量有误',
    }

    def __init__(self, code=0, message=""):
        self.error_code = code
        self.message = message or self.translate.get(self.error_code)

    def __str__(self):
        return self.message.encode('utf8')