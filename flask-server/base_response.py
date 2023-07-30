class BaseResponse:
    isSuccess: bool
    data: str
    message:str
    ErrorMessage=str


    def __init__(self):
       self.data=""
       self.message=""
       self.ErrorMessage=""
       self.isSuccess=True