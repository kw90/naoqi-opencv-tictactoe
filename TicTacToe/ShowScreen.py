import os


class ShowScreen(object):
    def __init__(self, session):
        self.__ip = os.environ.get("BOARD_SERVICE_IP")
        self.__port = os.environ.get("BOARD_SERVICE_PORT")
        try:
            self.__tablet = session.service("ALTabletService")
            self.__tablet.enableWifi()
            print("Tablet connection status: " + self.__tablet.getWifiStatus())
        except Exception as e:
            print(e)

    def show_screen(self, params):
        url_flipped = (
            "http://" + self.__ip + ":" + self.__port + "/index-flipped.html"
        )
        self.__tablet.showWebview(url_flipped + params)

    def hide_screen(self):
        self.__tablet.hideWebview()
