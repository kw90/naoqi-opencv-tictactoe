# Tic Tac Toe running on Pepper

Application for playing Tic Tac Toe against Pepper with simple game logic, computer vision and human-robot interaction components. The included Dockerfile allows to run everything in a pre-built container without the need to install Python2.7, NaoQi 2.5 and OpenCV 3.4. The environment variables `PEPPER_IP` and `PEPPER_PW` should be changed. This repository has been created for a workshop at the 37th Bundeswettbewerb Informatik BWINF.


## Requirements

The following software must be installed beforehand:

+ Docker Engine >= v16 (current version v18.09 recommended)
	+ An installation guide for any operating system can be found on the [Docker
		Docs](https://docs.docker.com/install/)


## Prepare Pepper

```bash
$ ssh nao@[PEPPER_IP]
# nao stop
# naoqi-bin --disable-life
```


## Development Guide

So that we can start programming, we first need the version control software `Git`. An installation guide can be found [here](https://git-scm.com/book/de/v1/Los-geht%E2%80%99s-Git-installieren).

Clone the repository naoqi-opencv-tictactoe with

```bash
git clone https://github.com/kw90/naoqi-opencv-tictactoe.git
```
and navigate into the folder

```bash
cd naoqi-opencv-tictactoe-dev
```

Inside this folder the container can be built using

```bash
docker build -t naoqi-opencv-tictactoe-dev:latest .
```

This will pull the Docker image from the Docker Hub, copy the
TicTacToe folder and sets the command `python Main.py` as the
Launch order.

Then the container can be started by running,

```bash
docker run -it --network host naoqi-opencv-tictactoe-dev:latest
```

which runs  the Python `Main.py` program on the specified Pepper in the `Dockerfile`.

To run a different program inside the container, it can be specified after the container image description

```bash
docker run -it --network host naoqi-opencv-tictactoe-dev:latest python DetectBoard.py
```

If something has been modified in the TicTacToe application, you can simply use the two commands

```bash
docker build -t naoqi-opencv-tictactoe-dev:latest .
docker run -it --network host naoqi-opencv-tictactoe-dev:latest
```

to rebuild and rerun the container.

### More convenient way

For more convenient development, the source directory `TicTacToe` can be mounted inside the container and started with a simple shell as entrypoint

```bash
docker run -it -v `pwd`/TicTacToe:/naoqi/src/tic-tac-toe --entrypoint /bin/sh --network host naoqi-opencv-tictactoe-dev:latest
```
This method allows to modify files on the Host machine using a preferred text editor and run them inside the container by running the Python program on the Docker shell, e.g. simply

```bash
python Main.py
```
