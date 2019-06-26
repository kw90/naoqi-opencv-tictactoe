## Requirements

Folgende Software muss vorher installiert werden:

+ Docker Engine >= v16 (aktuelle Version v18.09 empfohlen)
	+ Eine Installations-Anleitung für jegliche Betriebssysteme kann auf [Docker
		Docs](https://docs.docker.com/install/) gefunden werden

Verbindung mit dem WLAN:

__SSID__: `PRAF`

__KEY__: `poposoft`

## Pepper vorbereiten

```bash
nao stop
naoqi-bin --disable-life
```


## Entwicklungsanleitung

Damit wir losprogrammieren können, brauchen wir zuerst die Versionsverwaltungs Software `Git`. Eine Installationsanleitung findet ihr unter https://git-scm.com/book/de/v1/Los-geht%E2%80%99s-Git-installieren.

Repo naoqi-opencv-tictactoe-dev von (https://gitlab.enterpriselab.ch/RoboCup/naoqi-opencv-tictactoe-dev) clonen  mittels

```bash
git clone https://gitlab.enterpriselab.ch/RoboCup/naoqi-opencv-tictactoe-dev
```
und in den Ordner hinein navigieren

```bash
cd naoqi-opencv-tictactoe-dev
```

In diesem Folder dann

```bash
docker build -t naoqi-opencv-tictactoe:latest .
```

aufrufen. Dies zieht das Docker Image vom Docker Hub, kopiert den
TicTacToe Folder hinein und setzt die Command `python Main.py` als
Startbefehl.

Daraufhin, kann mit

```bash
docker run -it --network host naoqi-opencv-tictactoe:latest
```

das Python Programm auf Pepper ausgeführt werden.

Wenn in der TicTacToe Anwendung etwas geändert wurde, kann dann einfach mittels den beiden commands

```bash
docker build -t naoqi-opencv-tictactoe:latest .
docker run -it --network host naoqi-opencv-tictactoe:latest
```

der container neu gebaut und ausgeführt werden.

