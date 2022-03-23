import datetime
import os
from typing import Any
from Tiktok_Analytics.services.rotator import Rotator
from loguru import logger


def get_logging() -> logger:

	"""Prepare logger with general configuration
	Returns:
	logger: Configured logger instance
	"""
	"""Prepare logger with general configuration

	Returns:
		logger: Configured logger instance
	"""
	# Rotate file if over 500 MB or at midnight every day
	rotator: Rotator = Rotator(size=5e+8, at=datetime.time(0, 0, 0))
	# design rotators
	logger.add(
		"./log/file_{time}.log", rotation=rotator.should_rotate)
	return logger



def config(key: str, default: str = None, cast=str) -> Any:
	"""Get environment variables will mainting the fastapi config interface
	"""
	logger.info('Get variables from env')
	# look for value
	value = os.getenv(key, default)
	# check if value is not None
	if value is not None:
		# change value type
		return cast(value)
	# we could've used implicit None function return but explicit is always better
	return None

def to_bool(value: str) -> bool:
	"""Map string variables to bool
	"""
	valid: dict = {'true': True, 't': True, '1': True,
				   'false': False, 'f': False, '0': False}

	if isinstance(value, bool):
		return value

	if not isinstance(value, str):
		raise ValueError('invalid literal for boolean. Not a string.')

	lower_value = value.lower()
	if lower_value in valid:
		return valid[lower_value]
	else:
		raise ValueError('invalid literal for boolean: "%s"' % value)


logger = get_logging()