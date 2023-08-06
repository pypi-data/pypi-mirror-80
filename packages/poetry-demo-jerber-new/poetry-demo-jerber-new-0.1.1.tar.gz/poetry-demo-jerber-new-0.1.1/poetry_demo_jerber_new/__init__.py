__version__ = "0.1.0"

print("HIIII")


main_name = "harriet"

from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str = "hi"


from poetry_demo_jerber.Models.User import user

print("here is a user", user)

if __name__ == "__main__":
    print("YAASS")
