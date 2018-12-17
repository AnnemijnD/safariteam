## course.py
De class "Course" maakt een object aan voor elk vak. Er zijn 29 courses, dus uit de class komen 29 objecten. Een course object bevat informatie over;
- Naam en course_id;
- Hoeveel hoorcolleges, werkcolleges en practica het vak heeft;
- Het maximum aantal leerlingen per hoorcollege, werkcollege of practicum;
- Het verwachtte aantal leerlingen per vak

Verder worden er in course.py sessies aangemaakt aan de hand van de class Session. Sessies zijn specifieke onderdelen van het vak (hoorcolleges, werkcolleges of practica). In totaal zijn er 129 sessions, waarvan 39 hoorcolleges.
De hoeveelheid sessies per onderdeel van een vak wordt bepaald door het aantal verachte studenten en het max aantal studenten per type. Een voorbeeld:

Het vak Advanced Heuristics verwacht 22 studenten. Het max aantal studenten per practicum van dit vak is 10. Er worden dus 3 (22/10 = 2,2) sessies aangemaakt voor het type practicum van het vak Advanced Heuristics.

Ook wordt er in course.py de 'mutual courses' ingeladen. Dit zijn de vakken die tegelijkertijd gevolgd moeten kunnen worden.

## loaddata.py
In loaddata.py wordt alle data ingeladen vanuit csv bestanden, zoals de vakken en zalen.

## schedulemaker.py
In schedulemaker.py wordt een random valide rooster gemaakt. Het rooster begint als een lege lijst en wordt vervolgens opgevuld met sessies, die aangemaakt worden in course.py. In de functie "fill_schedule" wordt meteen al rekening gehouden met de hard constraints, zoals dat de hoorcolleges geplaatst moeten worden voor de werkcolleges en practica (zie het mapje algoritmes of exploratie.pdf voor uitleg over de hard constraints).

## session.py
session.py wordt gebruikt door de Course class (in course.py). In Course worden objecten van sessies aangemaakt aan de hand van de Session class. Er zijn in totaal 140 sessies, inclusief 'lege' sessies (dagen * zalen * tijslots = 140). De lege sessies bestaan uit sessies die geen type sessie bevatten maar wel een id hebben. In totaal zijn er 11 'lege' sessies. Een sessie bevat informatie over:
- De naam en id van de sessie
- Het type van de sessie (dit kan hoorcollege, werkcollege of practicum zijn)
- Het max aantal studenten voor deze sessie
- De id van de groep van deze sessie (zie kopje "Groepen")
- course_object: deze begint leeg en wordt later aangevuld door het object van het vak waar de sessie vandaan komt (bijvoorbeeld als de sessie een Bioinformatica werkcollege is, dan bestaat het course_object uit een object van het van Bioinformatica).

## Groepen
Omdat het maximaal aantal studenten soms niet overeenkomt met het aantal verwachte studenten voor een vak, worden er meerdere groepen aangemaakt. Een groep bestaat uit een aantal studenten en een type van een vak (werkcollege of practica). Voor hoorcolleges worden geen groepen aangemaakt, aangezien alle studenten bij elk hoorcollege aanwezig zijn. Elke groep heeft een eigen id.
