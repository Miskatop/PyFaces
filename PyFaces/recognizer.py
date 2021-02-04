#!/usr/bin/python3
from cv2 import cv2 
import face_recognition as recognizer
from .handlers import DefaultHandlers
from threading import Thread
from time import sleep

class Recognizer(DefaultHandlers):
	_LOOP = True
	capture = cv2.VideoCapture(0)
	_known_encodings = []
	self.THREADS = []

	def __init__(self, face_paths: list, shoot: bool=False,
				path_to_shoot:str='detected_face/', debug:bool=False, thread:bool=False):
		self.shoot = shoot
		self.path_to_shoot = path_to_shoot
		self.debug = debug
		self.thread = thread

		self.load_faces(*face_paths)

	def load_faces(self, *args:list, face_paths:list=[]):

		face_paths = list(args).extend(face_paths)

		for path in face_paths:
			image = recognizer.load_image_file(path)
			face_locations = recognizer.face_locations(image)
			face_encoding = recognizer.face_encodings(image, face_locations)
			self._known_encodings.append(face_encoding)

	def run_by_thread(self, function):
		th = Thread(target=function)
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

				# Setting variables to work
				face_have = len(face_locations) >= 1
				compare = []

				# capture have a faces condition
				if face_have:
					face_encodings = recognizer.face_encodings(frame, face_locations)
					for face_encoding in face_encodings:
						for known_encoding in self._known_encodings:
							matches = recognizer.compare_faces(known_encoding, face_encoding)
							compare.append(matches[0])

				known = True in compare

				if not face_have:
					if self.thread:
						self.run_by_thread(self._not_faces_handler())
					else:
						self._not_faces_handler()

				if not known and face_have:
					if self.shoot:
						cv2.imwrite(self.path_to_shoot+'unknown.jpg', frame)

					if self.thread:
						self.run_by_thread(self._unknown_handler())
					else:
						self._unknown_handler()

					if self.debug:
						print('[ LOG ] - Unknown')

				elif known:
					if self.thread:
						self.run_by_thread(self._known_handler())
					else:
						self._known_handler()

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
