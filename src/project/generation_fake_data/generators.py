from random import choice, randrange
from generation_fake_data.constants import *


class Generation:

    def __init__(self, number):
        self.number = number

    def generator_fullname(self):
        full_name = [f'{choice(NAME)} {choice(LAST_NAME)}' for i in range(self.number)]
        return full_name

    def generator_phone_number(self):
        phone_number = [f'+380{choice(COD)}{randrange(0000000, 9999999)}' for i in range(self.number)]
        return phone_number

    def generation_email (self):
        email = []
        for i in range(self.number):
            name = choice(NAME).lower()
            separator = choice(NAME_SEPARATOR)
            year = randrange(1950, 2010)
            email.append(f'{name}{separator}{year}@{choice(E_DEMON)}')
        return email


Full = Generation(6)
print(Full.generator_fullname())
print(Full.generator_phone_number())
print(Full.generation_email())
