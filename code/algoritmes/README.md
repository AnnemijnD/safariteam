## constraint.py

In constraint.py staan functies die checken voor bepaalde "constraints" en per functie een aantal punten teruggeven.

### Punten
De punten van de roosters zijn berekend aan de hand van de bonus- en maluspunten. Hierbij worden de minpunten van de hard constraints ook meegenomen, maar zijn zo goed als verwaarloosbaar naarmate het rooster beter wordt.
Het aantal punten van een rooster wordt berekend met de berekening:

Points = spread_bonuspoints  - hard_constraints * 100  - student_fit_maluspoints / (max(student_fit_maluspoints / max(session_bonuspoints)))

- Hierbij bestaan de spread_bonus_points uit het verschil tussen de bonus en maluspunten die een session kan hebben.
- De hard constraints bestaan uit minpunten van de hard constraints (hoorcolleges eers en rekening houdend met overlappende vakken). Deze worden 100 keer meer meegeteld dan de soft constraints, zodat een rooster veel makkelijker aan de hard constraints kan voldoen.
- Om ervoor te zorgen dat de bonus- en maluspunten evenveel meetellen in de puntenberekeneing wordt er een berekening gemaakt voor het aantal maluspunten. De malus punten van capaciteit (student_fit_maluspoints) worden gedeeld door (het max aantal maluspunten voor deze soft constraint gedeeld door het max aantal bonuspunten). 


### Hard constraints
Dit zijn de constraints waar het rooster sowieso aan moet voldoen zijn:
- Alle hoorcolleges moeten eerder in de week ingepland worden dan de werkcolleges en de practica.
- Lessen mogen niet met zichzelf overlappen.
- Sommige vakken moeten tegelijkertijd volgbaar zijn.

Het max aantal minpunten dat deze hard constraint kan hebben is 39.

### Soft constraints
- Hou rekening met studentenaantallen; een groep van ingeroosterde studenten moet ook in de ingeroosterde zaal passen.
- Een vak moet goed verspreid zijn over de week.

## hillclimber.py

In hillclimber.py wordt gebruik gemaakt van het hill climber algoritme. Deze krijgt een valide rooster mee (= een rooster die aan de hard constraints voldoet) en zoekt hierna een rooster dat aan zoveel mogelijk soft constraints voldoet. Er wordt steeds een nieuw rooster gemaakt en gekeken of dit nieuwe rooster meer punten heeft dan het vorige rooster; als dit wel zo is dan wordt er verder gewerkt met het nieuwe rooster met meer punten, waardoor de punten steeds verder oplopen.

## annealing.py

In annealing.py wordt een simulated annealing algoritme toegepast. In dit rooster kunnen er, in tegenstelling tot de hillclimber, ook roosters worden geaccepteerd met minder punten. Het accepteren van slechtere roosters gebeurt op basis van een kansberekening. Naarmate het aantal iteraties hoger wordt, wordt de kans minder dat een slechter rooster geaccepteerd wordt. Er zijn verschillende cooling schemes gebruikt (= een manier waarop de acceptatiekans bepaald wordt), waaruit bleek dat de 'exponential cooling scheme' op beste resultaten uit kwam.

## genetic.py

Een genetisch algoritme dat geïnspireerd is door onderdelen uit de evolutie. Er worden goede roosters geselecteerd en hiervan worden 'kinderen' gemaakt. Dit wordt een aantal generaties herhaald zodat er een nieuwe populatie van goede kinderen (roosters) is.
