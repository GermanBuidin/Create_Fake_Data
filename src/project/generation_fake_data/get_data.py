
def getData():
    n = [{
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
        },
        {
            "order": 4,
            "title": "email",
            "type": "EMAIL",

        }
    ]
    return n


def get_title():
    name = []
    for i in getData():
        name.append(f'{i["order"]} {i["title"]}')
    print(name)

d=get_title()