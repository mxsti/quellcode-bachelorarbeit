# Dodge Game Environment

Ziel des Spiels ist es den von oben herab fallenden Barrieren solange wie möglich auszuweichen.

## Observationen:
### Distanz
Typ: Box(1)<br>
| Index 	| Name    	| Min 	| Max 	|
|-------	|---------	|-----	|-----	|
| 0     	| Distanz 	| 0   	| 500 	|
|       	|         	|     	|     	|

### Position
Typ:Box(2)
| Index 	| Name               	| Min 	| Max 	|
|-------	|--------------------	|-----	|-----	|
| 0     	| x-Position Player  	| 60  	| 440 	|
| 1     	| x-Position Barrier 	| 0   	| 400 	|
|       	|                    	|     	|     	|


## Actions:
Type: Discrete(3)
| Index 	| Aktion              	|
|-------	|---------------------	|
| 0     	| nach links bewegen  	|
| 1     	| nach rechts bewegen 	|
| 2     	| nicht bewegen       	|
|       	|                     	|

## Rewards:
+20 für Gewinn des Spiels (Score = 200)<br>
-20 für Niederlage (Kollision mit Barriere)<br>
+1 für das Überleben<br>

## Start Start:
Player in x-Position 250, 1. Barriere in Zufälliger x-Position

## Ende einer Episode:
Erreichen des Maximum Scores von 200 (konfigurierbar) oder Kollision mit einer Barriere