## constraint.py

In constraint.py staan functies die checken voor bepaalde "constraints" en per functie een aantal punten teruggeven.

### Hard constraints
Dit zijn de constraints waar het rooster sowieso aan moet voldoen zijn:
- Alle hoorcolleges moeten eerder in de week ingepland worden dan de werkcolleges en de practica.
- Lessen mogen niet met zichzelf overlappen.
- Sommige vakken moeten tegelijkertijd volgbaar zijn.

### Soft constraints
- Hou rekening met studentenaantallen; een groep van ingeroosterde studenten moet ook in de ingeroosterde zaal passen.
- Een vak moet goed verspreid zijn over de week.

## swutch.py

Switch is een module die ervoor zorgt dat twee of meer random lessen worden geruild binnen 1 rooster. 

## hillclimber.py

In hillclimber.py wordt gebruik gemaakt van het hill climber algoritme. Deze krijgt een valide rooster mee (= een rooster die aan de hard constraints voldoet) en zoekt hierna een rooster dat aan zoveel mogelijk soft constraints voldoet. Er wordt steeds een nieuw rooster gemaakt en gekeken of dit nieuwe rooster meer punten heeft dan het vorige rooster; als dit wel zo is dan wordt er verder gewerkt met het nieuwe rooster met meer punten, waardoor de punten steeds verder oplopen.

## genetic.py

Een genetisch algoritme dat geïnspireerd is door onderdelen uit de evolutie. Er worden goede roosters geselecteerd en hiervan worden 'kinderen' gemaakt. Dit wordt een aantal generaties herhaald zodat er een nieuwe populatie van goede kinderen (roosters) is.
