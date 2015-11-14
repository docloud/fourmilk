# coding=utf8


class Error(Exception):
    " 0 ~ 1000 System Error "
    BOOTSTRAP_ERROR = 0

    " 1000 ~ fin User Error "
    USER_NOT_EXIST = 1000
    PART_NOT_EXIST = 1001

    translate = {
        BOOTSTRAP_ERROR: u'System Internal Error',

        USER_NOT_EXIST: u'用户不存在',
        PART_NOT_EXIST: u'零件不存在',
    }

    def __init__(self, code=0):
        self.error_code = code
        self.message = self.translate.get(self.error_code)

    def __str__(self):
        return self.message.encode('utf8')