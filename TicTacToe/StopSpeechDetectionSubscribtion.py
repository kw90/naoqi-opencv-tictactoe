import qi

# Amber
ip = "192.168.1.101"

# Porter
# ip = "192.168.1.102"

connection_url = ip + ":9559"

app = qi.Application(["--qi-url=" + connection_url])
app.start()
session = app.session

service = session.service("ALSpeechRecognition")
service.unsubscribe("SpeechDetection")
