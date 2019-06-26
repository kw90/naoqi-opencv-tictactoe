FROM kw90/naoqi-opencv-developer:latest

ADD TicTacToe /naoqi/src/tic-tac-toe/

WORKDIR /naoqi/src/tic-tac-toe

ENV PEPPER_IP="192.168.2.107"
ENV PEPPER_PW="tinaturner"

CMD [ "python" , "./Main.py" ]

