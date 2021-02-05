#!/usr/bin/python3
from PyFaces import Recognizer
import config as c

app = Recognizer(c.KNOWN, thread=True)

@app.known()
def known(uname):
	print("[ KNOWN ] - ", uname)

@app.no_faces()
def noface():
	pass

@app.unknown()
def unknown(frame):
	pass

app.run()
