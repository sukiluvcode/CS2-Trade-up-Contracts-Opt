import threading
import time

class Throttle:
	def __init__(self, capacity: int, recovery_rate: float):
		"""
		Initialize the Throttle.

		:param capacity: Maximum number of tokens in the bucket.
		:param recovery_rate: Tokens recovered per second.
		"""
		self.capacity = capacity
		self.recovery_rate = recovery_rate
		self.tokens = capacity
		self.last_check = time.time()
		self.lock = threading.Lock()
		self.cond = threading.Condition(self.lock)
		
	def _recover(self):
		now = time.time()
		elapsed = now - self.last_check
		recovered = elapsed * self.recovery_rate
		if recovered > 0:
			prev_tokens = self.tokens
			self.tokens = min(self.capacity, self.tokens + recovered)
			self.last_check = now
			if int(self.tokens) > int(prev_tokens):
				self.cond.notify_all()

	def consume(self, amount: int = 1) -> bool:
		"""
		Attempt to consume tokens. Returns True if successful, False otherwise.
		Thread-safe.
		"""
		with self.cond:
			self._recover()
			if self.tokens >= amount:
				self.tokens -= amount
				return True
			return False

	def wait_consume(self, amount: int = 1):
		"""
		Block until able to consume the requested amount.
		Thread-safe.
		Efficient: uses condition variable to avoid busy-waiting.
		"""
		with self.cond:
			while True:
				self._recover()
				if self.tokens >= amount:
					self.tokens -= amount
					return
				# Wait for up to 0.5s, then recheck (in case of spurious wakeups)
				self.cond.wait(timeout=0.5)

	def freeze(self, time_seconds: float):
		"""
		Freeze the throttle for a specified duration.
		Thread-safe.
		"""
		with self.cond:
			self.tokens = 0
			self.last_check = time.time() + time_seconds

def wait(throttler: Throttle):
	def outer(func):
		def wrapper(*args, **kwargs):
			throttler.wait_consume()
			return func(*args, **kwargs)
		return wrapper
	return outer
		