FROM kw90/naoqi-opencv-developer:latest

ADD TicTacToe /naoqi/src/tic-tac-toe/

WORKDIR /naoqi/src/tic-tac-toe

ENV PEPPER_IP="192.168.1.100"
ENV PEPPER_TABLET_IP="198.18.0.1"
ENV PEPPER_PW="tinaturner"

CMD [ "python" , "./Main.py" ]

