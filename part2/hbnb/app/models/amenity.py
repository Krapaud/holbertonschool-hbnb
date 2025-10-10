from . import BaseModel


class AmenityModel(BaseModel):
    def __init__(self, name):
        super().__init__()
        if len(name) < 50:
            self.name = name
        else:
            print("Required, maximum length of 50 characters.")
