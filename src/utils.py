def remove_none(l: list) -> list:
	"""
		Returns a list that does not contain any`None` values.

		@param l: The list to filter
		@return: a new list
	"""

	return list(filter(None, l))


def pad_right_with(l: list, sz: int, pd) -> list:
	"""
		Return a new `sz`-sized list obtained by right padding `l` with `pd`.
		If the starting list is of size `sz` or greater, no change is applyed.

		@param l: The list to pad. No changes are made to this list.
		@param sz: The final size of the list if it needs to be padded. A negative value will result in no changes.
		@param pd: the element to ose as padding.
		@return: A new list of size `sz`, or greater if `l` was greater.
	"""
	if(sz < 0 or len(l) >= sz):
		return l.copy()

	return (l + sz * [pd])[:sz]


def to_ffmpeg_duration_string(s: float) -> str:
	"""
		Returns a duration string formatted following the ffmpeg documentation
		@param s: The number of seconds of the duration.
		@return: A string formatted as `HH:MM:SS.mmm`
	"""
	hours = int(s / (60 * 60))
	mins = int((s / 60) % 60)
	secs = int(s % 60)
	millis = int((s - int(s)) * 1000)
	return "{hours:2d}:{mins:2d}:{secs:2d}.{millis:3d}".format(hours=hours, mins=mins, secs=secs, millis=millis).replace(' ', '0')
