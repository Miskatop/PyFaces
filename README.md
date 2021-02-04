# PyFaces - Face Recognition library in python3

## Requirements\`

#### NOTE\` 

### dlib v19.04+
```bash
  pip install dlib
```
### open cv v4.0+
```bash
  pip install opencv-python
```
### face-recognition v1.3+
```bash
  pip install face-recognition
```
## Examples\`

This Example from the main.py

```python

#!/usr/bin/python3
from PyFaces import Recognizer
import config as c

app = Recognizer(c.KNOWN, debug=True, thread=True)

@app.known()
def known():
	print("Known Face Detected")

@app.no_faces()
def noface():
	print("Not faces in picture")

@app.unknown()
def unknown():
	print("Unknown Face Detected")

app.run()


```
