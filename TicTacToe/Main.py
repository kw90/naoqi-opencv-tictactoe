import qi
import os

from GameHandler import GameHandler

if __name__ == "__main__":

    # Amber
    # Pepper DFKI
    #ip = "pepper-1.sb.dfki.de"
    ip = os.environ['PEPPER_IP']
    # Porter
    # ip = "192.168.1.102"

    connection_url = ip + ":9559"

    app = qi.Application(["--qi-url=" + connection_url])
    app.start()
    session = app.session
    motion = session.service('ALMotion')
    leds = session.service("ALLeds")

    #motion.setExternalCollisionProtectionEnabled('All', False)
    #motion.setCollisionProtectionEnabled('Arms', False)
    print('arms collison protection: ' + str(motion.getCollisionProtectionEnabled('Arms')))
    print('external collison protection: ' + str(motion.getExternalCollisionProtectionEnabled('All')))
    motion.wakeUp()

    GameHandler = GameHandler(session, ip, motion, leds)
