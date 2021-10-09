from enum import Enum, auto
from typing import List, Literal


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


class FileType(Enum):
	FILETYPE_IMAGE = auto()
	FILETYPE_VIDEO = auto()
	FILETYPE_UNKNOWN = auto()

	@classmethod
	def get_filetype(cls, filepath: str) -> Literal[None]:
		IMAGE_EXTENSIONS: List[str] = [
                    # Raster
                				".jpg",
                				".jpeg",
                				".jp",
                				".jif",
                				".jfif",
                				".jfi",
                				".png",
                				".gif",
                				".webp",
                				".tiff",
                				".tif",
                				".psd",
                				".raw",
                				".arw",
                				".cr2",
                				".nrw",
                				".k25",
                				".bmp",
                				".dib",
                				"heif",
                				"heic",
                				"ind",
                				"indd",
                				"indt",
                				"jp2",
                				"j2k",
                				"jpf",
                				"jpx",
                				"jpm",
                				"mj2",
                				# Vector
                				"svg",
                				"svgz",
                				"ai",
                				"eps",
                				"pdf",
                ]
		VIDEO_EXTENSIONS: List[str] = [
			".webm",
			".mpg",
			".mp2",
			".mpeg",
			".mpe",
			".mpv",
			".ogg",
			".mp4",
			".m4p",
			".m4v",
			".avi",
			".wmv",
			".mov",
			".qt",
			".flv",
			".swf",
			".avchd",
		]
		if(any(map(lambda x: filepath.lower().endswith(x), IMAGE_EXTENSIONS))):
			return cls.FILETYPE_IMAGE
		elif(any(map(lambda x: filepath.lower().endswith(x), VIDEO_EXTENSIONS))):
			return cls.FILETYPE_VIDEO
		else:
			return cls.FILETYPE_UNKNOWN
