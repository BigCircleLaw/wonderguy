class wonderbitsError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  #初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


if __name__ == '__main__':
    try:
        raise wonderbitsError('连接异常')
    except wonderbitsError as e:
        print(e)
