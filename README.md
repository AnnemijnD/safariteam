# UvA Lesroosters

Probleem: hoe kan een lesrooster zo efficiënt mogelijk ingedeeld worden?

## Link naar het rooster

https://annemijnd.github.io/safariteam/results/schedule.html

### Vereisten

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/).
Alle benodigde pakketten staan in requirements.txt.

### Structuur

In het mapje 'code' staan alle scripts. In het mapje 'data' staan alle csv bestanden.
en in het mapje resultaten staat het bestand 'schedule.html'. Hierin wordt uiteindelijk het rooster weergegeven.
In het bestand 'exploratie' wordt ingegaan op o.a. de state space en lower- en upper bound.

### Test

De code kan gerund worden met de onderstaande code.
```
python plan.py
```
Vervolgens wordt verschijnt er een pop-up met mogelijke input. Alle velden moeten ingevuld worden. Als er wordt gevraagd om aantal iteraties of runs, moet de input altijd een positief getal zijn. In de terminal wordt aangegeven wanneer er een functie geladen wordt.

### Resultaat
Het uiteindelijke resultaat staat in de folder 'results' onder de naam 'schedule.html'.

## Structuur van het rooster
Het rooster bestaat uit totaal 140 slots:
  - 5 dagen;
  - 4 tijdslots per dag;
  - 7 zalen per tijdslot;

## Auteurs

Annemijn, Sanne en Rebecca

## Dankwoord

Met dank aan tech-assistent Quinten van der Post!



![alt text](http://heuristieken.nl/wiki/images/f/f5/Roostering2.jpg)
