from random import choice, randrange
from generation_fake_data.constants import *
from generation_fake_data.get_data import getData


class Generator:

    def __init__(self, rows, age_from=0, age_to=0):
        self.rows = rows
        self.age_from = age_from
        self.age_to = age_to

    def generation_fullname(self):
        for i in range(self.rows):
            yield f'{choice(NAME)} {choice(LAST_NAME)}'

    def generation_phone_number(self):
        for i in range(self.rows):
            yield f'+380{choice(COD)}{randrange(0000000, 9999999)}'

    def generation_email(self):

        for i in range(self.rows):
            name = choice(NAME).lower()
            separator = choice(NAME_SEPARATOR)
            year = randrange(1950, 2010)
            yield f'{name}{separator}{year}@{choice(E_DEMON)}'

    def generation_age(self):
        for i in range(self.rows):
            yield f'{randrange(self.age_from, self.age_to)}'

    def generation_address(self):
        for i in range(self.rows):
            house = f'{randrange(1, 100)} {choice(NAME_STREET)} {choice(TYPE_STREET)} apartment-{randrange(1,200)} '
            country = f'{choice(CITY)} {randrange(00000, 99999)}-cod in USA'
            yield f'{house} {country}'


def generation_fake_data(rows):
    list_data = {}
    for i in getData():
        type_func = i["type"]
        age_from = 0
        age_to = 0
        if "AGE" in i.values():
            age_from = i["from"]
            age_to = i["to"]
        for n, k in enumerate(FakeData(type_func, age_from, age_to, rows).get_type()):
            if n in list_data:
                list_data[n] = f'{list_data[n]},{k}'
            else:
                list_data[n] = f'{k}'
    return list_data


class FakeData:
    def __init__(self, type_func, age_from=0, age_to=0, rows=0):
        self.type = type_func
        self.age_from = age_from
        self.age_to = age_to
        self.rows = rows

    def get_type(self):
        data_type = {"ADDRESS": Generator(self.rows).generation_address(),
                     "AGE": Generator(self.rows, self.age_from, self.age_to).generation_age(),
                     "FULL_NAME": Generator(self.rows).generation_fullname(),
                     "NUMBER_PHONE": Generator(self.rows).generation_phone_number(),
                     "EMAIL": Generator(self.rows).generation_email()}
        return data_type[self.type]
