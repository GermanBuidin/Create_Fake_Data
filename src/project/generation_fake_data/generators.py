from random import choice, randrange
from generation_fake_data.constants import *
from generation_fake_data.get_data import getData, get_type


class Generator:

    def __init__(self, number, age_from=0, age_to=0):
        self.number = number
        self.age_from = age_from
        self.age_to = age_to

    def generation_fullname(self):
        for i in range(self.number):
            yield f'{choice(NAME)} {choice(LAST_NAME)}'

    def generation_phone_number(self):
        phone_number = [f'+380{choice(COD)}{randrange(0000000, 9999999)}' for i in range(self.number)]
        return phone_number

    def generation_email(self):

        for i in range(self.number):
            name = choice(NAME).lower()
            separator = choice(NAME_SEPARATOR)
            year = randrange(1950, 2010)
            yield f'{name}{separator}{year}@{choice(E_DEMON)}'

    def generation_age (self):
        age = [f'{randrange(self.age_from, self.age_to)}' for i in range(self.number)]
        return age

    def generation_adress (self):
        address = []
        for i in range(self.number):
            house = f'{randrange(1, 100)} {choice(NAME_STREET)} {choice(TYPE_STREET)} apartment-{randrange(1,200)} '
            country = f'{choice(CITY)} {randrange(00000, 99999)}-cod in USA'
            address.append(f'{house} {country}')
        return address


class FakeData:

    def generation_fake_data(self):
        name = [i["type"] for i in getData()]
        for number in name:
            print (number)


Full = FakeData()
Full.generation_fake_data()
Full1 = Generator(6, 6, 9)
print (choice(NAME_STREET))
