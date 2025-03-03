class Model:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, value)
            else:
                raise AttributeError(f"{key} is not a valid attribute for {self.__class__.__name__}")
