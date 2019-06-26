import qi

ip = os.environ['PEPPER_IP']

connection_url = ip + ":9559"

app = qi.Application(["--qi-url=" + connection_url])
app.start()
session = app.session

service = session.service("ALSpeechRecognition")
service.unsubscribe("SpeechDetection")
