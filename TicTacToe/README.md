# TicTacToe

Works only on Amber.

nao:i1-p2e3p

## Init Commands

```console
$ export NAO_IP=<pepper IP>

$ ssh nao@NAO_IP

$ nao stop

$ naoqi-bin --disable-life
```

In another shell session

```console
$ ssh nao@NAO_IP

$ qicli call ALMotion.wakeUp
```

## Calibrate color ranges for stones

Edit the ``__red_range_lower``, ``__red_range_upper`` and blue equivalent arrays in the DetectBoard.py class.

## Debug image processing
The image processing can be tested by running DetectBoard.py. It will create multiple debug files:
* gray, binary, canny images
* detected board, fields
* detected red and blue stones