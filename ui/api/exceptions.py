class APIException(Exception):

   def __init__(self, *args, **kwargs) -> None:
       self.code = kwargs.get('code', 500)
       super().__init__(*args)
