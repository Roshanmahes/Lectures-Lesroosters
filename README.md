# Lectures & Lesroosters
Programmeertheorie/Heuristieken case Lectures & Lesroosters - Roshan Mahes, Philip Roeleveld, Gido Limperg

De laatste update van ons verslag is [hier](https://www.sharelatex.com/project/59187fabc5474c740b67101b/) te vinden.

## Toestandsruimte
Het is zo eenvoudig nog niet om de grootte van de toestandsruimte te berekenen. Je moet namelijk zowel het aantal manieren waarop colleges in het rooster kunnen worden gezet, als het aantal manieren waarop de studenten kunnen worden ingeroosterd in alle werkcollege-, en practicumgroepen berekenen. Het eerste is relatief simpel. We bepalen het aantal slots M waarin colleges worden geroosterd en berekenen het aantal colleges n dat ingeroosterd moet worden en schrijven
<p align="center">
<img src="https://raw.githubusercontent.com/Roshanmahes/Lectures-Lesroosters/master/README%20resources/latex1.png"/>
</p>
voor het aantal manieren om colleges in te roosteren. De andere kant van het verhaal is lastiger. Voor het aantal manieren om studenten in groepen te zetten berekenen we dan ook niet de exacte waarde, maar een adequate bovengrens. Per vak nemen we de capaciteit van een college en het aantal studenten s dat het vak volgt en berekenen we per college van het aantal groepen g dat nodig om alle studenten in te roosteren. Dan is de waarde
<p align="center">
<br>
<img src="https://raw.githubusercontent.com/Roshanmahes/Lectures-Lesroosters/master/README%20resources/latex2.png"/>
</p>
een bovengrens voor het aantal manieren waarop studenten kunnen worden ingeroosterd. Vermenigvuldigen we de twee bovenstaande getallen nu met elkaar, dan vinden we de bovengrens
<p align="center">
<br>
<img src="https://raw.githubusercontent.com/Roshanmahes/Lectures-Lesroosters/master/README%20resources/latex3.png"/>
</p>
