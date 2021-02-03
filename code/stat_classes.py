class Pokemon:
	def __init__(self):
		self.name = ""
		self.hpstat = 0
		# this is a percentage
		self.remaininghp = 100
		self.poisoned = ""
		self.burned = ""
		self.leechseed = ""
		self.activatedmove = ""
		self.cursed = ""
		self.confused = ""
		self.alive = True
		self.stats = dict()
		self.stats['kills'] = 0
		self.stats['totaldd'] = 0
		self.stats['directdd'] = 0
		self.stats['indirectdd'] = 0
		self.stats['activeturns'] = 0
		self.stats['switchins'] = 0
		self.stats['switchouts'] = 0
		self.stats['misses'] = 0
		self.stats['crits'] = 0


class Side:
	def __init__(self):
		
		self.player_name = ""
		self.remaining = 0
		self.team_size = 0
		# this is the hazards on the other side, value should be pokemon on THIS side
		# key is hazard name, value is pokemon nickname, exception is key numspikes, which takes a number
		self.hazards = dict()
		self.hazards['numspikes'] = 0
		self.hazards['spikes1'] = ""
		self.hazards['spikes2'] = ""
		self.hazards['spikes3'] = ""
		self.hazards['stealthrocks'] = ""
		self.hazards['tspikes'] = ""

		# key is be nickname, value is be pokemon object
		self.pokemon = dict()

		# Turn data
		self.activepok = ""
		self.move = ""
		self.usedmove = False
		self.switch = False


class Game:
	def __init__(self):
		self.replay_id = ""

		# key is weather name, value is pokemon name
		self.weather = dict()
		self.weather['sandstorm'] = ""
		self.weather['hail'] = ""
		self.weather['startedby'] = ""

		# key is integer [1, 2], value is side object
		self.sides = dict()
		self.sides['1'] = Side()
		self.sides['2'] = Side()

		# stores last event in game
		self.lastevent = ""

