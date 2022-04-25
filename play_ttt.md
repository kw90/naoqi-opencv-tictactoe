# Play TicTacToe

1. Print or Draw a black Tic Tac Toe field with rather thick edges

2. Place Pepper at roughly 40cm distance in front of the field and run
`ssh nao@PEPPER_IP -c "nao stop && naoqi-bin --disable-life"`
ℹ️ wait for all modules to be loaded (all 143 of them)

3. Launch web server to host the game field that is retrieved by Peppers tablet
`cd ~/source/naoqi-opencv-tictactoe/TicTacToe/html/html && python3 -m http.server`

4. Launch VNC and see if field is clearly visible by Peppers camera
`cd ~/source/docker-pepper && ./run.sh`

5. (Launch image server to see debug CV images)
`cd ~/source/naoqi-opencv-tictactoe/TicTacToe/debug_images && python imageme.py 8080`
-> Open browser at localhost:8080 and use auto-refresh extension

5. Launch game
`cd ~/source/naoqi-opencv-tictactoe && ./run.sh`
