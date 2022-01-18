from .generators import Generator

def getData():
    N=[{
        "order": 0,
        "title": "name",
        "type": "FULL_NAME"
    },
        {
            "order": 1,
            "title": "number phone",
            "type": "NUMBER_PHONE"
        },
        {
            "order": 2,
            "title": "age",
            "type": "AGE",
            "from": 14,
            "to": 60
        },
        {
            "order": 3,
            "title": "Address",
            "type": "ADDRESS"
        }]
    return N


def get_type():
    TYPE = {"ADDRESS": Generator(6).generation_adress(),
            "AGE": Generator(6, 6, 60).generation_age(),
            "FULL_NAME": Generator(6).generation_fullname(),
            "NUMBER_PHONE": Generator(6).generation_phone_number()}
    return TYPE