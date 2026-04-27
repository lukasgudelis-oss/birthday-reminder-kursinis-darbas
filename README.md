# Birthday Reminder

Tai Python kalba parašyta gimtadienių priminimo programa. Programa leidžia vartotojams pridėti, peržiūrėti ir ištrinti gimtadienius, gauti priminimus, bei išsaugoti duomenis faile.

---

## 1. Įvadas (Introduction)

### Projekto tikslas

Sukurti veikiančią gimtadienių valdymo sistemą, kuri pademonstruotų keturis pagrindinius OOP pilierius, projektavimo šablonų naudojimą bei duomenų valdymą išoriniuose failuose.

### Kaip paleisti programą?

1. Įsitikinkite, kad kompiuteryje įdiegtas Python 3.8+.
2. Atsisiųskite projekto failus į vieną aplanką.
3. Atidarykite terminalą tame aplanke ir paleiskite:

```bash
python birthday_reminder.py
```

### Kaip naudotis programa?

- **Paleidimas:** Įveskite vartotojo vardą ir pasirinkite rolę (`user` arba `admin`).
- **Pridėjimas:** Pasirinkite `1`, įveskite vardą ir datą formatu `YYYY-MM-DD`.
- **Trynimas:** Pasirinkite `2`, matysite sąrašą ir galėsite ištrinti pagal vardą.
- **Peržiūra:** Pasirinkite `3` — programa parodys artimiausius gimtadienius.
- **Šiandien:** Pasirinkite `4` — patikrinama ar šiandien kas nors švenčia.
- **Išsaugojimas:** Pasirinkite `5` arba `0` — duomenys išsaugomi į `birthdays.csv`.

### Kaip kūriau programą (kūrimo eiga)

Programą kūriau palaipsniui — kiekvienas žingsnis buvo atskiras Git commit'as.

1. **Validacija** (`validators.py`) — pradėjau nuo paprasčiausio: funkcija kuri tikrina ar varde nėra skaičių ar simbolių.
2. **Abstrakti klasė** (`notifiable.py`) — sukūriau bazinę „sutartį" kuri sako kad kiekvienas vartotojas privalo turėti `send_notification()` metodą.
3. **Birthday klasė** (`birthday.py`) — klasė kuri saugo vieno žmogaus vardą ir datą, ir moka suskaičiuoti kiek dienų liko iki gimtadienio.
4. **User ir AdminUser klasės** (`user.py`) — vartotojas kuris turi gimtadienių sąrašą. AdminUser paveldi viską iš User, bet pranešimus rodo kitaip.
5. **BirthdayManager** (`manager.py`) — pagrindinis valdytojas su Singleton šablonu ir failų logika.
6. **Meniu** (`main.py`) — paskutinis žingsnis kuris sujungia viską į vieną veikiančią programą.
7. **Testai** (`test_birthday_reminder.py`) — unit testai kurie patikrina ar viskas veikia kaip turi.

---

## 2. Analizė ir Įgyvendinimas (Body/Analysis)

### 1. Enkapsuliacija (Encapsulation)

Reikšmė: Duomenų slėpimas klasės viduje, apsaugant juos nuo tiesioginio pasiekiamumo iš išorės.

```python
class Birthday:
    def __init__(self, name: str, birth_date: date) -> None:
        self._name = name
        self._birth_date = birth_date
```

### 2. Paveldėjimas (Inheritance)

Reikšmė: Galimybė kurti naujas klases esamų klasių pagrindu, perimant jų savybes ir metodus.

```python
class User(Notifiable):
    ...

class AdminUser(User):
    ...
```

### 3. Abstrakcija (Abstraction)

Reikšmė: Sudėtingos detalės paslepiamos apibrėžiant tik bendrą metodų struktūrą per abstrakčias klases.

```python
class Notifiable:
    def send_notification(self, message: str) -> None:
        raise NotImplementedError("send_notification() turi buti realizuotas!")
```

### 4. Polimorfizmas (Polymorphism)

Reikšmė: Skirtingos klasės gali turėti tą patį metodą, tačiau jį įgyvendinti skirtingai.

Šiame projekte metodas `send_notification()` realizuojamas skirtingai:

- `User` klasėje rodomas paprastas pranešimas
- `AdminUser` klasėje tas pats pranešimas rodomas su `ADMIN` žyme ir žvaigždutėmis

Tai leidžia naudoti tą patį metodą skirtingiems objektams, nekeičiant programos logikos.

```python
class User(Notifiable):
    def send_notification(self, message: str) -> None:
        print(f"[{self._username}] Pranesimas: {message}")

class AdminUser(User):
    def send_notification(self, message: str) -> None:
        print(f"[ADMIN - {self._username}] *** {message} ***")
```

### Projektavimo šablonas (Design Pattern)

Projekte panaudotas **Singleton** šablonas klasėje `BirthdayManager`.

- **Kodėl šis šablonas?** Sistemoje turi egzistuoti tik vienas centralizuotas objektas, atsakingas už vartotojų ir gimtadienių valdymą. Singleton užtikrina, kad visoje programoje veiktų tas pats duomenų srautas.
- **Veikimas:** Perrašius `__new__` metodą, užtikrinama, kad sukūrus naują `BirthdayManager()` objektą, bus grąžinta ta pati jau egzistuojanti egzemplioriaus nuoroda.

```python
class BirthdayManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._users = {}
        return cls._instance
```

### Kompozicija ir Agregacija

- **Kompozicija:** `User` objektas turi `Birthday` objektų sąrašą. Gimtadieniai tiesiogiai priklauso nuo vartotojo — be vartotojo jie neegzistuoja.
- **Agregacija:** `BirthdayManager` klasė turi `User` objektų žodyną. Tai agregacija, nes vartotojai sukuriami atskirai ir tik tada perduodami valdytojui.

### Darbas su failais (File Handling)

Programa naudoja Python funkcijas darbui su failais.

- Duomenys rašomi į `birthdays.csv`.
- Išsaugoma: vartotojo vardas, gimtadienio vardas ir data.
- Failas automatiškai yra įkeliamas kiekvieną kartą paleidus programą.

### Testavimas (Testing)

Programoje naudojamas testavimas su Python standartine biblioteka `unittest`. Iš viso parašyti **25 testai**, visi praeina.

Testavimo metu buvo tikrinamos svarbiausios sistemos dalys:

**Validacija** — tikrinama ar `is_valid_name()` teisingai atmeta skaičius ir simbolius.

**Gimtadienio logika** — testuojama ar `days_until()` grąžina teigiamą skaičių ir ar `is_today()` teisingai atpažįsta šiandienos datą.

**Vartotojų valdymas** — tikrinama gimtadienių pridėjimas, trynimas ir paieška neatsižvelgiant į didžiąsias/mažąsias raides.

**Singleton šablono veikimas** — patikrinama ar sukūrus kelis `BirthdayManager` objektus, jie visi nurodo į tą patį egzempliorių.

**Failų operacijos** — tikrinama ar išsaugojus ir vėl nuskaičius duomenys nesidingsta.

Testai vykdomi su šią komandą:

```bash
python -m unittest test_birthday_reminder.py -v
```

---

## 3. Rezultatai ir Išvados (Results and Summary)

### Rezultatai

- Programa sėkmingai įgyvendina gimtadienių valdymo funkcionalumą: vartotojai gali pridėti, peržiūrėti ir ištrinti gimtadienius.
- Įgyvendintas Singleton projektavimo šablonas, kuris užtikrina vieną sistemos instanciją.
- Testavimo metu teko atidžiai rašyti `setUp` metodus, nes Singleton išlaiko būseną tarp testų.
- Sukurti ir paleisti 25 vienetiniai testai, kurie patvirtina pagrindinių funkcijų teisingą veikimą.
- Duomenų išsaugojimas į CSV failą veikia gerai — duomenys išlieka tarp programos paleidimų.

### Išvados

Šio darbo metu buvo sukurta veikianti gimtadienių priminimo sistema, pritaikant objektinio programavimo principus.

Buvo sėkmingai įgyvendinti keturi OOP principai: enkapsuliacija, paveldėjimas, abstrakcija ir polimorfizmas. Taip pat pritaikytas Singleton projektavimo šablonas ir parodyti kompozicijos bei agregacijos principai.

Ateityje manau, jog šią sistemą būtų galima tobulinti:

- naudojant duomenų bazę vietoje CSV failo
- pridedant el. laiškų siuntimą kai artėja gimtadienis

---

## 4. Šaltiniai (References)

- Python dokumentacija: https://docs.python.org/3/
- unittest dokumentacija: https://docs.python.org/3/library/unittest.html
- Dizaino šablonai: https://refactoring.guru/design-patterns/singleton/python/example
- PEP8: https://pep8.org/

## Autorius : Lukas Gudelis (EIF-25)
