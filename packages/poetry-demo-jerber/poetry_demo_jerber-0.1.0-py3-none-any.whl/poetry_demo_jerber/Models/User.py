from pydantic import BaseModel

from poetry_demo_jerber import main_name


class User(BaseModel):
    name: str = "Jed"


user = User(name=main_name)

print(user)