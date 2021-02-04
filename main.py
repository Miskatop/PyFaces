#!/usr/bin/python3
from PyFaces import Recognizer
import config as c

app = Recognizer(c.KNOWN, debug=True, thread=True)

@app.known()
def known():
	pass

@app.no_faces()
def noface():
	pass

@app.unknown()
def unknown():
	pass

app.run()
