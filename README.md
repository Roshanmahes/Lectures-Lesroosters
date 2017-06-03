# Lectures & Lesroosters
Programmeertheorie/Heuristieken case Lectures & Lesroosters - Roshan Mahes, Philip Roeleveld, Gido Limperg

Ons verslag is [hier](https://github.com/Roshanmahes/Lectures-Lesroosters/blob/master/verslag.pdf) te vinden.


## Algemene informatie
Zie het bestand _requirements.txt_ voor de packages die nodig zijn om de programma's te laten werken.
Alle resultaten die zijn gebruikt in het verslag zijn te vinden in de folder _results_.
Opgeslagen roosters (inclusief het door ons best gevonden rooster en het allereerste rooster) zijn te vinden in de folder _schedules_.
_hill\_climb\_script.py_ en _simulated\_annealing\_script.py_ kunnen worden uitgevoerd om de gelijknamige algoritmes te laten lopen.
Beide scripts duren ongeveer tien minuten maar kunnen worden uitgevoerd met een extra commandline argument om het aantal iteraties te veranderen.
(De standaardwaardes zijn 30 en 100000 respectievelijk.)
Naast deze scripts kunnen in _main.py_ handmatig functies worden aangeroepen zoals de functie die de grootte van de toestandsruimte berekent.

## Bestandsstructuur
__algorithms__

- hill\_climb.py - Het Hill Climbing algoritme en de swap functies die het gebruikt.
- make\_schedule.py - Drie rooster makende functies, alphabetical, random\_sample, en random\_fit.
- simulated\_annealing.py - Het Simulated Annealing algoritme en de swap functies die het gebruikt.
- temperature.py - Alle temperatuurfuncties die gebruikt kunnen worden voor het Simulated Annealing algoritme.

__data__ - Folder met alle case-specifieke bestanden.

__helpers__

- classes.py - Alle class declaraties.
- functions.py - Alle overige hulpfuncties.
- score.py - De functies waarmee de score word berekend.
- state\_space.py - De functie om de toestandsruimte te berekenen.

__results__ - Alle resultaten die zijn gebruikt. Dit is ook waar nieuwe resultaten gegeenereerd door een van de scripts of main.py terechtkomen.

__schedules__ - Hier komen alle pdf bestanden van roosters in te staan.

__hill\_climb\_script.py__ - Een basaal script dat het Hill Climbing algoritme uitvoert.

__main.py__ - Importeert alle andere bestanden en initialiseert de data. Voer vanuit hier algoritmes en andere functies uit.

__requirements.txt__ - Zie boven.

__simulated\_annealing\_script.py__ - Een basaal script dat het Simulated Annealing algoritme uitvoert.
