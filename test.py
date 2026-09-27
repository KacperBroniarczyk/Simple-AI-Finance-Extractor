dane={'zakupy': [{'kategoria': 'jedzenie', 'kwota': 25}, {'kategoria': 'jedzenie', 'kwota': 5}, {'kategoria': 'usługi', 'kwota': 150}]}

nowy_slownik={}

for element in dane['zakupy']:
    if element['kategoria'] not in nowy_slownik:
        nowy_slownik[element['kategoria']] = int(element['kwota'])
    else:
        nowy_slownik[element['kategoria']] = nowy_slownik[element['kategoria']]+int((element['kwota']))

print(nowy_slownik)