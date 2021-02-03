import re
import string
import os
import sys
from sqlite3 import connect
from parse_funcs import *
from debug_funcs import *
from stat_classes import Pokemon, Side, Game

##########################
# HELPER FUNCTIONS       #
##########################

def get_replay_id(replay_data):
	replay_id = re.search('(?<=gen[0-9]ou-)[0-9]+', replay_data).group(0)
	return replay_id

def get_player_names(replay_data):
	p1_name = re.search('(?<=\|player\|p1\|)[^\|]+', replay_data).group(0)
	p2_name = re.search('(?<=\|player\|p2\|)[^\|]+', replay_data).group(0)
	return [p1_name, p2_name]

def get_team_sizes(replay_data):
	p1_ts = re.search('(?<=\|teamsize\|p1\|)[1-6]', replay_data).group(0)
	p2_ts = re.search('(?<=\|teamsize\|p2\|)[1-6]', replay_data).group(0)
	return [p1_ts, p2_ts]

def set_nicknames(replay_data, game):
	pattern = re.compile(r'(?<=\|switch\|p([0-9])a: )([^\|]+)\|([^\|,]+)')
	for m in re.finditer(pattern, replay_data):
		player_num = m.group(1)
		nickname = m.group(2)
		actual_name = m.group(3)
		# skip reoccurrences
		if nickname in game.sides[player_num].pokemon:
			continue
		game.sides[player_num].pokemon[nickname] = Pokemon()
		game.sides[player_num].pokemon[nickname].name = actual_name
		# TODO query db for pokemon HP stat and set hp stat for each pokemon
		# statement = "SELECT hp FROM pokedex WHERE pokemon=?"

def get_preturn1_data(replay_data):
	data = re.search(r'((.|\n)*?)(?=\|turn\|1)', replay_data).group(0)
	return data

def get_leads(preturn1_data):
	p1_lead = re.search(r'(?<=\|switch\|p1a: )([^\|]+)\|([^\|,]+)', preturn1_data).group(1)
	p2_lead = re.search(r'(?<=\|switch\|p2a: )([^\|]+)\|([^\|,]+)', preturn1_data).group(1)
	return [p1_lead, p2_lead]

def check_and_set_weather(preturn1_data, game):
	weather_pattern = re.compile(r'(?<=-weather)\|([^\|]+)\|([^\|]+)\|\[of\] p([1-2])a: (.*)')
	for m in re.finditer(weather_pattern, preturn1_data):
		weather_type = m.group(1)
		side = m.group(3)
		pok_name = m.group(4)

		# clear weather
		game.weather['sandstorm'] = ""
		game.weather['hail'] = ""
		game.weather['startedby'] = ""
		
		if weather_type == 'RainDance' or weather_type == 'SunnyDay':
			continue
		if weather_type == 'Sandstorm':
			game.weather['sandstorm'] = pok_name
		if weather_type == 'Hail':
			game.weather['hail'] = pok_name

		game.weather['startedby'] = side

##########################
# MAIN FUNCTION          #
##########################

# TODO after all testing, change the test_games directory to the directory where the
# replay files will actually be stored

test_filename = ""
if(len(sys.argv) == 2):
	test_filename = sys.argv[1]
else:
	sys.exit("Please provide only a filename from the test_games directory as a command line argument")

parent_dir = os.path.dirname(os.getcwd())
test_filepath = os.path.join(parent_dir, 'test_games', test_filename)

with open(test_filepath) as f:
	replay = f.read()

game = Game()

##########################
# PRE-TURN 1 PARSING     #
##########################

# get replay id
game.replay_id = get_replay_id(replay)

# get player names
player_names = get_player_names(replay)
game.sides['1'].player_name = player_names[0]
game.sides['2'].player_name = player_names[1]

# get team size on each side
team_sizes = get_team_sizes(replay)
game.sides['1'].team_size = team_sizes[0]
game.sides['2'].team_size = team_sizes[1]

# parse replay for nicknames, map nicknames to pokemon
set_nicknames(replay, game)

# get text before turn 1 for lead poks and possible weather
preturn1_data = get_preturn1_data(replay)

# get pokemon leads for each side
leads = get_leads(preturn1_data)
game.sides['1'].activepok = leads[0]
game.sides['2'].activepok = leads[1]

check_and_set_weather(preturn1_data, game)

##########################
# TURN BY TURN PARSING   #
##########################

turn_pattern = re.compile(r'(?<=\|turn\|)([0-9]+)((.|\n)*?)((?=\|turn\|)|(?=\|win\|))')
for m in re.finditer(turn_pattern, replay):
	turn_number = m.group(1)
	turn_data = m.group(2)
	print("parsing turn " + turn_number)
	for line in turn_data.split('\n'):
		
		# if switch
		if re.search(r'(?<=\|switch\|p([1-2])a: )([^\|]+)', line) != None:
			m = re.search(r'(?<=\|switch\|p([1-2])a: )([^\|]+)', line)
			switch(m, game)

		# if damage
		if re.search(r'(?<=-damage\|)p([1-2])a: ([^\|]+)\|([^\|]+)\|?([^\|]+)?\|?([^\|]+)?', line) != None:
			m = re.search(r'(?<=-damage\|)p([1-2])a: ([^\|]+)\|([^\|]+)\|?([^\|]+)?\|?([^\|]+)?', line)
			# TODO implement
			#damage(m, game)

		# if move
		if re.search(r'(?<=\|move\|p([1-2])a: )([^\|]+)\|([^\|]+)', line) != None:
			m = re.search(r'(?<=\|move\|p([1-2])a: )([^\|]+)\|([^\|]+)', line)
			move(m, game)

		# if leech seed starts
		if re.search(r'(?<=-start\|p([1-2])a: )([^\|]+)\|move: Leech Seed', line) != None:
			m = re.search(r'(?<=-start\|p([1-2])a: )([^\|]+)\|move: Leech Seed', line)
			ls_start(m, game)
		
		# if leech seed ends
		if re.search(r'(?<=-end\|p([1-2])a: )([^\|]+)\|Leech Seed', line) != None:
			m = re.search(r'(?<=-end\|p([1-2])a: )([^\|]+)\|Leech Seed', line)
			ls_end(m, game)

		# if hazards start
		if re.search(r'(?<=-sidestart\|p([1-2]): )[^\|]+\|(move: )?(.*)', line) != None:
			m = re.search(r'(?<=-sidestart\|p([1-2]): )[^\|]+\|(move: )?(.*)', line)
			hazard_start(m, game)

		# if hazards end
		if re.search(r'(?<=-sideend\|p([1-2]): )[^\|]+\|(move: )?([^\|]+)', line) != None:
			m = re.search(r'(?<=-sideend\|p([1-2]): )[^\|]+\|(move: )?([^\|]+)', line)
			hazard_end(m, game)

		# if weather starts/ends/changes
		if re.search(r'-weather\|([^\|]+)(\|([^\|]+)\|?(.*)?)?', line) != None:
			m = re.search(r'-weather\|([^\|]+)(\|([^\|]+)\|?(.*)?)?', line)
			weather(m, game)

		# if poison or burn or tox starts
		if re.search(r'(?<=-status\|p([1-2])a: )([^\|]+)\|(.*)', line) != None:
			m = re.search(r'(?<=-status\|p([1-2])a: )([^\|]+)\|([^\|]+)\|?(.*)?', line)
			status_start(m, game)

		# if poison or burn or tox ends
		if re.search(r'(?<=-curestatus\|)p([1-2])a?: ([^\|]+)\|([^\|]+)', line) != None:
			m = re.search(r'(?<=-curestatus\|)p([1-2])a?: ([^\|]+)\|([^\|]+)', line)
			cure_status(m, game)

		# if crit
		if re.search(r'(?<=-crit\|p([1-2])a: )', line) != None:
			m = re.search(r'(?<=-crit\|p([1-2])a: )', line)
			crit(m, game)

		# if miss
		if re.search(r'(?<=-miss\|p([1-2])a: )([^\|]+)', line) != None:
			m = re.search(r'(?<=-miss\|p([1-2])a: )([^\|]+)', line)
			miss(m, game)

		# if faint, clear pok1 or pok2, and update death for current pokemon
		if re.search(r'(?<=faint\|p([1-2])a: )(.*)', line) != None:
			m = re.search(r'(?<=faint\|p([1-2])a: )(.*)', line)
			faint(m, game)

		# TODO if heal
		# TODO if mega (change HP stat and actual pok name (not nickname))
		# TODO destiny bond
		# TODO future sight
		# TODO yawn (dont remember why we need to check for this when i wrote this TODO)
		# TODO start flag (handles curse, confused, future sight, sub, belly drum)
		# TODO ghost curse
		# TODO confused
		# TODO terrains
		
		# TODO increment active turns for the activepok if they're still alive
		# clear moves
		game.sides['1'].move = ""
		game.sides['2'].move = ""
		game.sides['1'].usedmove = False
		game.sides['2'].usedmove = False
		# clear switches
		game.sides['1'].switch = False
		game.sides['2'].switch = False


# TODO increment appearance value in db for all pokemon in p1pok and p2pok
# TODO get actual player names, calculate score and return stats





	







