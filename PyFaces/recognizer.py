#!/usr/bin/python3
from cv2 import cv2 
import face_recognition as recognizer
from .handlers import DefaultHandlers
from threading import Thread
from time import sleep

class Recognizer(DefaultHandlers):
	_LOOP = True
	capture = cv2.VideoCapture(0)
	_known_encodings = {}
	THREADS = []

	def __init__(self, face_paths:dict, shoot:bool=False,
				path_to_shoot:str='detected_face/', 
				debug:bool=False, thread:bool=False):

		self.shoot = shoot
		self.path_to_shoot = path_to_shoot
		self.debug = debug
		self.thread = thread

		self.load_faces(**face_paths)

	def load_faces(self, **face_paths):

		for name, path in face_paths.items():
			image = recognizer.load_image_file(path)
			face_locations = recognizer.face_locations(image)
			face_encoding = recognizer.face_encodings(image, face_locations)
			self._known_encodings[name] = face_encoding

	def run_by_thread(self, function, *args, **kwargs):

		th = Thread(target=function, args=args, kwargs=kwargs)
		self.THREADS.append(th)
		th.start()

	def run(self):
		while self._LOOP:
			try:
				if not self.capture.isOpened():
					sleep(5)

				_, frame = self.capture.read()
				frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]
				face_locations = recognizer.face_locations(frame)
				face_have = len(face_locations) >= 1
				compare = []

				if face_have:
					face_encodings = recognizer.face_encodings(frame, face_locations)
					for face_encoding in face_encodings:
						for name, encoding in self._known_encodings.items():
							matches = recognizer.compare_faces(encoding, face_encoding)
							compare.append([name, matches[0]])

				known = True in [c[1] for c in compare]

				if not face_have:
					if self.thread:
						self.run_by_thread(self._not_faces_handler())
					else:
						self._not_faces_handler()

				if not known and face_have:
					if self.shoot:
						cv2.imwrite(self.path_to_shoot+'unknown.jpg', frame)

					if self.thread:
						self.run_by_thread(self._unknown_handler(frame))
					else:
						self._unknown_handler(frame)

					if self.debug:
						print('[ LOG ] - Unknown')

				elif known:
					for item in compare:
						if item[1]:
							if self.thread:
								self.run_by_thread(self._known_handler(item[0]))
							else:
								self._known_handler(item[0])

					if self.debug:
						print('[ LOG ] - Known')

			except Exception as e:

				if self.debug:
					print(f'[ ERROR ] - {e} .')

			except KeyboardInterrupt:
				break


	def stop(self):
		self._LOOP=False
		self.capture.release()
		cv2.destroyAllWindows()
		for thread in self.THREADS:
			thread.join()

	def known(self):
		def outer(func):
			self._known_handler = func
			return
		return outer

	def no_faces(self):
		def outer(func):
			self._not_faces_handler = func
			return
		return outer

	def unknown(self):
		def outer(func):
			self._unknown_handler = func
			return
		return outer
