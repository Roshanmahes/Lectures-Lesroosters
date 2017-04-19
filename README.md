# Lectures & Lesroosters
Programmeertheorie/Heuristieken case Lectures & Lesroosters - Roshan Mahes, Philip Roeleveld, Gido Limperg

## Inleiding
Roosters zijn van uiterst belang in het hedendaags leven. Zonder roosters zouden zaken in het leven geen structuur hebben, de kleinste planning die je in je hoofd hebt, is al een rooster. Al is het het feit dat je om 5 uur boodschappen gaat doen, vervolgens koken en vanaf 9 uur televisie kijken. Natuurlijk is dit eenvoudig te onthouden, maar het onthouden van een trein-/busreis van Science Park naar Berkhout, een track die je niet dagelijks afreist, is al een stuk lastiger. Vooral als je niet even het rooster met vertrektijden op station Amsterdam Centraal, of de 9292-app, niet kan gebruiken.

Omdat roosters zo een belangrijke rol spelen in ons leven, is het evident dat er uitgebreid onderzoek wordt gedaan naar het bepalen van een optimaal rooster. Helaas is dit een onoplosbaar probleem, roosters zijn namelijk lastiger in te richten dan je denkt. Er is namelijk geen algemene oplossing om voor elke toestand een optimaal rooster te maken. Regelmatig worden er nieuwe algoritmes bedacht binnen onder andere de Grafentheorie om een zo goed mogelijk rooster te maken. Helaas kost zo een algoritme al gauw dagen, maanden, of zelfs jaren rekentijd. Vaak zijn de roosters waar wij in het dagelijks leven mee te maken hebben erg lastig te maken met zo een algoritme. Zo willen we bijvoorbeeld niet elke dag op hetzelfde moment een gebeurtenis inplannen, duurt deze niet altijd even lang, of moet er rekening gehouden worden met feestdagen. We kunnen wellicht aanvaarden dat het maken van een rooster enige tijd kan duren. Maar jaren? Zo lang willen we nou ook weer niet wachten voor een reisje Berkhout.

## Case Lectures & Lesroosters
In onze case hebben we te maken met 609 studenten (zie [vakkenenstudenten.csv](https://github.com/Roshanmahes/Lectures-Lesroosters/blob/master/studentenenvakken.csv)). Elk van de studenten volgt tussen de één en vijf vakken in periode 4. Er zijn 29 vakken (zie [vakken.csv](https://github.com/Roshanmahes/Lectures-Lesroosters/blob/master/vakken.csv)). Verder zijn er zeven zalen (zie [zalen.csv](https://github.com/Roshanmahes/Lectures-Lesroosters/blob/master/zalen.csv)), waarin de studenten les hebben. Het is aan ons om de studenten in te delen in groepen, en een weekrooster te maken, opdat elk van de studenten tevreden naar elk van zijn/haar lessen kan.

### Vereisten
Natuurlijk zou een opdracht als deze eenvoudig uit te werken zijn als er geen verdere vereisten waren. Net als in de praktijk ontbreken deze noodzakelijkheden niet. De volgende zaken zijn bij deze case van toepassing:

  0. Alle 29 vakken dienen ingeroosterd te worden.
  1. Vakken bestaan uit hoorcolleges en/of werkcolleges en/of practica.
  2. Alle zalen zijn voor alle drie collegetypes geschikt.
  3. Bij hoorcolleges moeten alle ingeschreven studenten ineens bedeeld worden.
  4. Bij werkgroepen en practica moeten de studenten, afhankelijk van de capaciteit, worden opgedeeld in zo min mogelijk groepen.
  5. Een college duurt van 9:00-11:00, 11:00-13:00, 13:00-15:00 of 15:00-17:00 op een werkdag. Eén zo'n periode van twee uur wordt een tijdsslot genoemd.
  6. Een geldig weekrooster is een weekrooster waarvoor aan alle roosterbare activiteiten van ieder vak een tijdsslot met een zaal hebben. We noemen het paar tijdsslot-zaal een zaalslot.

Er zijn nog steeds meerdere roosters te maken die aan bovenstaande vereisten voldoen. Een student wil niet alleen een rooster hebben, maar ook dat hij/zij zo veel mogelijk opsteekt bij de vakken. Daarom zijn er enkele bonus- en maluspunten te verdienen, wat een indicatie geeft van hoe goed het door ons gemaakte rooster is:

  * Een geldig weekrooster levert 1000 punten op.
  
  Bonuspunten:
  * Studenten leren het meest als de activiteiten zoveel mogelijk verdeeld zijn over de week. Een vak van twee tot vier activiteiten die maximaal verdeeld zijn over de week levert 20 bonuspunten op. Voor twee activiteiten is dat ma-do of di-vr, voor drie activiteiten is dat ma-wo-vr en voor vier activiteiten is dat ma,di,do,vr.
  
  Maluspunten:
  * Voor ieder vak van x activiteiten geldt dat ze 10 maluspunten opleveren als ze op x-1 dagen geroosterd zijn, 20 voor x-2 en 30 voor x-3.
  * Voor ieder zaalslot geldt dat er één maluspunt valt voor iedere ingeschreven student die er volgens de opgegeven zaalgroote niet meer in past.
  * Voor iedere student die meer dan één activiteit in een tijdsslot heeft (een roosterconflict) geldt 1 maluspunt per conflict.

Tot slot is er nog één escape optie, indien het maken van het rooster ons maar niet wil lukken:

  Escape:
  * De grootste zaal heeft ook een avondslot van 17:00-19:00, maar gebruik van het avondslot kost 50 maluspunten.

## Toestandsruimte
(5)*(5)*(7)*(609/29)??
?? 609 nCr 29
