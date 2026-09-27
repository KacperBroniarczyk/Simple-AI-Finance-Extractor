from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()
client=OpenAI()

def finanse_ai(polecenie):
    try:
        odpowiedz=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"jestes ekstaktorem danych finansowym. Zwracaj wyslane ci dane w formacie json: {'zakupy': [{'kategoria': 'nazwa', 'kwota': liczba}]}"},
                      {"role":"user","content":polecenie}],
            temperature=0.0,
            response_format={"type":"json_object"})
        return (odpowiedz.choices[0].message.content)
    except Exception as e:
        print(f"Błąd komunikacji z API: {e}")
        return None

def main():
    with open("wydatki.txt","r",encoding='utf-8') as plik:
        dane=plik.read()

    wynik=(finanse_ai(dane))
    if wynik:
        with open("wynik.json","w",encoding='utf-8') as plik_wyjsciowy:
            plik_wyjsciowy.write(wynik)
        print("Dane poprawnie wyekstrahowane i zapisane do wynik.json.")

    try:
        dane_json = json.loads(wynik)
    except Exception as e:
        print(f"{e}")
    nowy_slownik={}
    try:
        for element in dane_json['zakupy']:
            if element['kategoria'] not in nowy_slownik:
                nowy_slownik[element['kategoria']] = int(element['kwota'])
            else:
                nowy_slownik[element['kategoria']] = nowy_slownik[element['kategoria']] + int((element['kwota']))
        print("Podsumowanie wydatków:")
        for k,v in nowy_slownik.items():
            print(f"- {k.capitalize()}: {v}zł")
        suma_calkowita=sum(nowy_slownik.values())
        print(f"Całkowita suma wydatków: {suma_calkowita}zł")
    except KeyError:
        print("Błąd struktury danych od AI")

if __name__ == "__main__":
    main()