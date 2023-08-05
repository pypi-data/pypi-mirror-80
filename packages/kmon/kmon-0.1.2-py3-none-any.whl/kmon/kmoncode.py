class KmonCode:
    code = None
    message = None
    def __init__(self,code,message): self.code = code ; self.message = message

class KmonException(Exception):
    def __init__(self,code , message=None, data=None): 
        self.code = code
        self.data = data
        self.message = message
        super().__init__(self.message)

        