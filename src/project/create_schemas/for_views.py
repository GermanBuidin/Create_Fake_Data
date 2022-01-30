from datetime import datetime

def datajson(form: 'form', formset: "formset"):
    parent = form.clean()
    child = []
    for f in formset:
        child.append(f.clean())
    parent['schema'] = child
    parent['date'] = f'{datetime.now()}'
    return parent
