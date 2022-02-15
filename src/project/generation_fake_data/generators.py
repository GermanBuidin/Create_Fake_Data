from random import choice, randrange

from generation_fake_data.constants import CITY, \
                                           CODE, \
                                           E_DEMON, \
                                           LAST_NAME, \
                                           NAME, \
                                           NAME_SEPARATOR, \
                                           NAME_STREET, \
                                           TYPE_STREET


class Generator:

    def __init__(self, rows, number_from=0, number_to=0):
        self.rows = rows
        self.number_from = number_from
        self.number_to = number_to

    def generation_fullname(self):
        for i in range(self.rows):
            yield f'{choice(NAME)} {choice(LAST_NAME)}'

    def generation_phone_number(self):
        for i in range(self.rows):
            yield f'+380{choice(CODE)}{randrange(0000000, 9999999)}'

    def generation_email(self):

        for i in range(self.rows):
            name = choice(NAME).lower()
            separator = choice(NAME_SEPARATOR)
            year = randrange(1950, 2010)
            yield f'{name}{separator}{year}@{choice(E_DEMON)}'

    def generation_number(self):
        for i in range(self.rows):
            yield f'{randrange(self.number_from, self.number_to)}'

    def generation_address(self):
        for i in range(self.rows):
            house = f'{randrange(1, 100)} {choice(NAME_STREET)} {choice(TYPE_STREET)} apartment-{randrange(1,200)} '
            country = f'{choice(CITY)} {randrange(00000, 99999)}-code in USA'
            yield f'{house} {country}'


def generator_fake_data(rows, data):
    fake_data = {}
    for i in data['schema']:
        type_func = i["type"]
        number_from = 0
        number_to = 0
        if i['type'] == 'integer':
            number_from = i["min_value"]
            number_to = i["max_value"]
        for n, k in enumerate(FakeData(type_func, number_from, number_to, rows).get_type_data()):
            if n in fake_data:
                fake_data[n] = f'{fake_data[n]},{k}'
            else:
                fake_data[n] = f'{k}'
    return fake_data


class FakeData:
    def __init__(self, type_func, number_from=0, number_to=0, rows=0):
        self.type = type_func
        self.age_from = number_from
        self.age_to = number_to
        self.rows = rows

    def get_type_data(self):
        if self.type == "address":
            type_data = Generator(self.rows).generation_address()
        elif self.type == "integer":
            type_data = Generator(self.rows, self.age_from, self.age_to).generation_number()
        elif self.type == "full_name":
            type_data = Generator(self.rows).generation_fullname()
        elif self.type == "phone_numbers":
            type_data = Generator(self.rows).generation_phone_number()
        else:
            type_data = Generator(self.rows).generation_email()
        return type_data
