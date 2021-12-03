docker run --rm -it --name pepper_tictactoe --network host --env-file .env --volume $PWD/TicTacToe:/naoqi/src/tic-tac-toe naoqi-opencv-tictactoe:latest
