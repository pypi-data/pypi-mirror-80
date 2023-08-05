from serial import Serial as _Serial
from threading import Lock as _Lock


class DigitalController:
	Head = b'\x40'

	@staticmethod
	def calc_crc(*args):
		crc = 0
		for arg in args:
			for seg in arg:
				crc += seg
		return crc % 256

	def __init__(self, port: str, baudrate=19200, timeout=0.3):
		self._controller = _Serial(port=port, baudrate=baudrate, timeout=timeout)
		self._lock = _Lock()
		self.device_type: int = 1
		self.device_id: int = 0

	def _recv_frame_body(self):
		head = self._controller.read()
		while len(head) == 1 and head != DigitalController.Head:
			head = self._controller.read()
		if len(head) != 1:
			raise IOError('Read frame head timeout.')
		length = self._controller.read()
		if len(length) != 1:
			raise IOError('Read data length timeout.')
		body = self._controller.read(length[0])
		if len(body) != length[0]:
			raise IOError('Read frame body timeout.')
		crc = self._controller.read()
		if len(crc) != 1:
			raise IOError('Read CRC timeout.')

		crc1 = DigitalController.calc_crc(head, length, body)
		if crc[0] != crc1:
			raise IOError('CRC incorrect.')

		return body

	def _send_frame_body(self, body):
		length = bytearray([len(body)])
		crc = DigitalController.calc_crc(DigitalController.Head, length, body)
		self._controller.write(DigitalController.Head)
		self._controller.write(length)
		self._controller.write(body)
		self._controller.write(bytearray([crc]))

	def write_something(self, body):
		with self._lock:
			self._controller.flushInput()
			self._send_frame_body(body)
			feedback = self._recv_frame_body()
		assert len(feedback) == 3
		if feedback[2] != 0:
			raise IOError('Configure device failed.')

	def read_something(self, body):
		with self._lock:
			self._controller.flushInput()
			self._send_frame_body(body)
			return self._recv_frame_body()

	def set_light_strength(self, strength: int, channel: int = 0):
		assert 0 <= strength < 256
		body = bytearray([self.device_type, self.device_id, 0x1A, channel, strength])
		self.write_something(body)

	def close(self):
		self._controller.close()

	def open(self):
		self._controller.open()

	@property
	def is_open(self) -> bool:
		return self._controller.is_open
