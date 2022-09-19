from os import environ
from typing import Final
from dotenv import load_dotenv
load_dotenv()


class TgKeys:
    TOKEN: Final = environ.get('TOKEN')
