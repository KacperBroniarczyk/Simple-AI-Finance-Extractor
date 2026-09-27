from dotenv import load_dotenv
from openai import OpenAI
import json
import streamlit as st
import pandas as pd

load_dotenv()
client = OpenAI()


def finanse_ai(polecenie):
    try:
        odpowiedz = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system","content": "jestes ekstaktorem danych finansowym. Zwracaj wyslane ci dane w formacie json: {'zakupy': [{'kategoria': 'nazwa', 'kwota': liczba}]}. "
                                                   "Kategoria ma się zawierać w tej liście: Dom i opłaty, Jedzenie, Transport, Zdrowie i uroda, Styl życia, Rozwój, Finanse, Rodzina i inne."},
                      {"role": "user", "content": polecenie}],
            temperature=0.0,
            response_format={"type": "json_object"})
        return odpowiedz.choices[0].message.content
    except Exception as e:
        print(f"Błąd komunikacji z API: {e}")
        return None

def main():
    st.title("Simple-AI-Finance-Extractor")
    if 'historia_wydatkow' not in st.session_state:
        st.session_state.historia_wydatkow=[]
    dane=st.text_input("Twoje wydatki: ")
    if dane:
        wynik=finanse_ai(dane)
        if wynik:
            with open("wynik.json","w",encoding='utf-8') as plik_wyjsciowy:
                plik_wyjsciowy.write(wynik)
            try:
                dane_json=json.loads(wynik)
                for element in dane_json['zakupy']:
                    st.session_state.historia_wydatkow.append(element)
                st.success("Dodano nowe wydatki.")
            except KeyError:
                st.error("Błąd struktury danych od AI.")
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")
    if len(st.session_state.historia_wydatkow) > 0:
        nowy_slownik = {}
        for element in st.session_state.historia_wydatkow:
            kategoria = element['kategoria'].capitalize()
            kwota = int(element['kwota'])
            if kategoria not in nowy_slownik:
                nowy_slownik[kategoria] = kwota
            else:
                nowy_slownik[kategoria] += kwota
        st.write("Podsumowanie wydatków:")
        for k, v in nowy_slownik.items():
            st.write(f"- {k}: {v}zł")
        suma_calkowita = sum(nowy_slownik.values())
        st.write(f"Całkowita suma wydatków: {suma_calkowita}zł")
        st.subheader("Wykres wydatków")
        tabela_wykresu = pd.DataFrame.from_dict(nowy_slownik, orient='index', columns=['Kwota'])
        st.bar_chart(tabela_wykresu)

if __name__ == "__main__":
    main()