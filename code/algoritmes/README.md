## constraint.py

In constraint.py staan functies die checken voor bepaalde "constraints" en per functie een aantal punten teruggeven.

### Punten
De punten van de roosters zijn berekend aan de hand van de bonus- en maluspunten. Hierbij worden de minpunten van de hard constraints ook meegenomen, maar zijn zo goed als verwaarloosbaar naarmate het rooster beter wordt.
Het aantal punten van een rooster wordt berekend met de berekening:

Points = spread_bonuspoints  - hard_constraints * 100  - student_fit_maluspoints / (max(student_fit_maluspoints / max(session_bonuspoints)))

- Hierbij bestaan de spread_bonus_points uit het verschil tussen de bonus en maluspunten voor spreiding die een session kan hebben.
- De hard constraints bestaan uit minpunten van de hard constraints (hoorcolleges voor andere colleges en rekening houdend met overlappende vakken). Deze worden zwaarder meegeteld dan de soft constraints, zodat een rooster makkelijker aan de hard constraints kan voldoen.
- Om ervoor te zorgen dat de bonus- en maluspunten evenveel meetellen in de puntenberekeneing wordt er een berekening gemaakt voor het aantal maluspunten. De malus punten van capaciteit (student_fit_maluspoints) wordt gedeeld door (het max aantal maluspunten voor deze soft constraint gedeeld door het max aantal bonuspunten). 


### Hard constraints
De constraints waar het rooster sowieso aan moet voldoen zijn:
- Alle hoorcolleges moeten eerder in de week ingepland worden dan de werkcolleges en de practica.
- Colleges van een vak mogen niet met andere colleges van datzelfde vak overlappen.
- Sommige vakken moeten tegelijkertijd volgbaar zijn.

### Soft constraints
- Hou rekening met studentenaantallen; een groep van ingeroosterde studenten moet ook in de ingeroosterde zaal passen. De functie die de maluspunten voor studentenaantallen berekent is de 'student_fit' functie. Deze functie kan minimaal -1332 en max 0 punten geven. 
- Een vak moet goed verspreid zijn over de week. De functie die de bonus en maluspunten voor verspreiding berekent is 'spread_chceck'. Deze functie kan minmaal -430 en maximaal 440 punten geven. 

## hillclimber.py

In hillclimber.py wordt gebruik gemaakt van het hill climber algoritme. Deze krijgt een valide rooster mee (= een rooster die aan de hard constraints voldoet) en zoekt hierna een rooster dat aan zoveel mogelijk soft constraints voldoet. Er wordt steeds een nieuw rooster gemaakt en gekeken of dit nieuwe rooster meer punten heeft dan het vorige rooster; als dit wel zo is dan wordt er verder gewerkt met het nieuwe rooster met meer punten, waardoor de punten steeds verder oplopen. Het aanmaken van een 'nieuw' rooster gebeurt door telkens 1 random sessie van het rooster te ruilen met een andere random sessie. Dit ruilen gebeurt in Constraint.py in de functie 'switch_sessions'. 
Na een aantal pogingen om meerdere random onderdelen per keer te switchen is gebleken dat de kans dat er een goed rooster wordt gevonden hoger is wanneer er telkens maar 1 onderdeel per keer geswitched wordt. Dit komt waarschijnlijk doordat de kans om een slecht rooster te genereren toeneemt wanneer er meer dan 1 onderdeel per keer geswitched wordt. 

## hillclimberextended.py

Deze hillclimber werkt voor een groot deel hetzelfde als de originele hill climber, maar in deze versie wordt er rekening gehouden met het 'vastlopen' van een rooster. Als er een x aantal keren alleen naar slechtere roosters zijn gemaakt, dan wordt er een nieuwe switch geforceerd, waarbij er dus geforceerd een random onderdeel wordt geruild, zonder te checken of dit rooster meer punten heeft. x is in deze functie bepaald door de hillclimber een aantal keer te runnen en uit te zoeken wat het hoogste resultaat gaf. Hieruit bleek dat het algoritme met een x tussen de 40 en 60 de hoogste resultaten genereerde. 

## annealing.py

In annealing.py wordt een simulated annealing algoritme toegepast. In dit rooster kunnen er, in tegenstelling tot de hillclimber, ook roosters worden geaccepteerd met minder punten. Het accepteren van slechtere roosters gebeurt op basis van een kansberekening. Naarmate het aantal iteraties hoger wordt, wordt de kans minder dat een slechter rooster geaccepteerd wordt. Er zijn verschillende cooling schemes gebruikt (= een manier waarop de acceptatiekans bepaald wordt), waaruit bleek dat de 'exponential cooling scheme' op beste resultaten uit kwam.

## genetic.py

In genetic.py wordt een genetisch algoritme toegepast. In dit algoritme wordt vanuit een begin populatie (een lijst met roosters) telkens een nieuwe populatie gemaakt. Uit de beginpopulatie worden ouders (roosters) gekozen die m.b.v. cyclische crossovers kinderen (roosters) maken.

Voor het kiezen van de ouders zijn verschillende methoden geimplementeerd. Er kan gekozen worden op basis van een "K-way tournament". Hierbij worden er telkens willekeurig K individueen gekozen en wordt het beste van deze K ouder. Uit een aantal keren testen is gebleken dat K=5 het beste resultaat geeft.
Een andere methode is de "ranking" methode. Hierbij krijgt ieder individu een cijfer tussen 1 en populatiegrootte, waarbij 1 het rooster is met het minst aantal punten representterd en populatiegrootte het rooster met de meeste punten. De roosters worden vervolgens met kans cijfer/populatiegrootte gekozen om ouder te zijn. Betere roosters hebben dus een grotere kans om ouder te worden.
Als laatste methode is er nog de random methode. Hierbij wordt er telkens willekeurig uit de populatie een rooster gekozen dat ouder wordt.

De kinderen worden gemaakt m.b.v cyclische crossovers, hierbij krijgen beide kinderen 30% van de ene ouder en 70% van de andere ouder. Deze percentages zijn ook gekozen op basis van testen. Om diversiteit in de populatie te brengen wordt bij maximaal 20% van de kinderen een mutatie aangebracht. Deze mutatie bestaat uit het doen van minimaal 1 en maximaal 3 switches van sessies.

Als laatste wordt deze nieuwe populatie gehalveerd zodat de populatiegrootte gelijk blijft. Dit halveren wordt altijd gedaan op basis van K-way tournament

Dit proces wordt een x aantal generaties uitgevoerd.
