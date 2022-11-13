# ATP_David_de_Jong

## Tiniest Basic

Interpreter

Reference: https://p112.sourceforge.net/tbp112.html


## Gebruik van het programma

Er kan een file gemaakt worden waarin Tiniest Basic code staat, die wordt vervolgens ingeladen en ge-interpret.
Het programma maakt gebruik van Python versie 3.10 via Windows.

## Turing compleet

- Er kunnen while/for loops worden gemaakt.
- Het slaat variabele op
- Er kunnen condities gemaakt worden door middel van if statements

## Commands

De taal bevat een aantal commands

- IF
- PRINT
- GOTO

Tiniest Basic maakt alleen gebruik van integers.<br />
Variabelen kunnen alleen losse hoofdletters zijn zoals A B C. <br />
PRINT functie kan alleen iets printen als het tussen ' ' staat: `PRINT 'Hello World!'`<br /><br />
Als de IF fout is, wordt de zin niet afgemaakt, als de IF goed is, maakt het programma de regel af.<br />
2 Condities voor een if statement verschillen met de meeste programmeer talen namelijk:
- `IF G <> 10` - Dit is een NOT conditie
- `IF A = 42` - Dit is een equal conditie ipv. ==

## Gebruik van taal

Tiniest Basic maak gebruik van regelnummers die zelf gemaakt moeten worden. Zo wordt dus elke regel assigned naar een nummer:<br />
```
10 A = 10
20 B = 10
30 C = A + B
40 IF C = 20 GOTO 100
50 GOTO 10
100 PRINT 'C is 20!'
```
Regelnummers kunnen ook open gelaten worden voor verduidelijking als er meerdere functies onder elkaar staan.<br />
Door middelvan een `,` kunnen meerdere operaties op 1 regel:<br /><br />
`2300 A = 1, B = 19, C = 20, Z = A + B`<br /><br />
Tiniest Basic kan niet meerdere reken-operaties in 1 regel maken, maximaal 2:<br /><br />
`WRONG: Z = A + B + C`
