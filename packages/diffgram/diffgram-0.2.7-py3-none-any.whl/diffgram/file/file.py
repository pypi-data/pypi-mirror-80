from ..regular.regular import refresh_from_dict


class File():
	"""
	file literal object
	See File Constructor for creating new files in Diffgram Service
	
	Feb 3, 2020. Perhaps should be all in the same File class.
	"""


	def __init__(
		self,
		id = None,
		client = None):

		self.id = id
		self.client = client


	def new(
			client, 
			file_json):
		"""
		New is new object from *Dict*
		get_xxx methods are for getting object 
		from Diffgram Service.

		In the current context a user doesn't create a new 
		File directly, the system creates a file at import
		and/or when copying / operating on a file.

		Could also call this new_from_dict()?

		Feb 3, 2020
			For now this is following pattern as in 
			Export class

		"""
		
		file = File(client=client)
		refresh_from_dict(file, file_json)
		return file


	def serialize(self):

		return {
			'id' : self.id
			}


	# WIP
	def update(
			self,
			instance_list: list = None,		# for Images
			frame_packet_map: dict = None,	# for Video
			overwrite: bool = False
			):
		"""
		"""

		packet = {}
		packet['file_id'] = self.id
		packet['mode'] = "update"
		packet['frame_packet_map'] = frame_packet_map
		packet['instance_list'] = instance_list

		# Current default server side is to not overwrite
		# packet['overwrite'] = overwrite

		self.client.file.from_packet(packet = packet)


	def copy(
		
		):

		raise NotImplementedError



