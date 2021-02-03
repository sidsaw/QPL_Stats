import re

def switch(m, game):
	game.lastevent = "switch"
	playernum = m.group(1)
	switch_in = m.group(2)
	switch_out = game.sides[playernum].activepok
	# if the switch in is coming after a pokemon fainted
	if switch_out == "":
		game.sides[playernum].activepok = switch_in
		return
	# clear leech seed and activated moves for the active pokemon
	game.sides[playernum].pokemon[switch_out].leechseed = ""
	game.sides[playernum].pokemon[switch_out].activatedmove = ""
	# add 1 to switch out for current active pokemon
	game.sides[playernum].pokemon[switch_out].stats['switchouts'] += 1
	# add 1 to switch in for switch_in pokemon
	game.sides[playernum].pokemon[switch_in].stats['switchins'] += 1
	# set switch flag to true
	game.sides[playernum].switch = True
	# change active pokemon name
	game.sides[playernum].activepok = switch_in

def faint(m, game):
	playernum = m.group(1)
	faintedpok = m.group(2)
	# update to fainted
	game.sides[playernum].pokemon[faintedpok].alive = False
	# clear active pokemon
	game.sides[playernum].activepok = ""

def miss(m, game):
	playernum = m.group(1)
	misspok = m.group(2)
	# update faints
	game.sides[playernum].pokemon[misspok].stats['misses'] += 1

def crit(m, game):
	# group 1 is player num of pokemon that was HIT with crit
	playernum = m.group(1)
	if playernum == '1':
		critpok = game.sides['2'].activepok
		game.sides['2'].pokemon[critpok].stats['crits'] += 1
	else:
		critpok = game.sides['1'].activepok
		game.sides['1'].pokemon[critpok].stats['crits'] += 1

def ls_start(m, game):
	# group 1 is player number
	playernum = m.group(1)
	# group 2 is pokemon nickname
	startpok = m.group(2)
	if playernum == '1':
		# get other active pokemon (the one that used leech seed)
		ls_starter = game.sides['2'].activepok
		# set leechseed on pokemon
		game.sides['1'].pokemon[startpok].leechseed = ls_starter
	else:
		# get other active pokemon (the one that used leech seed)
		ls_starter = game.sides['1'].activepok
		# set leechseed on pokemon
		game.sides['2'].pokemon[startpok].leechseed = ls_starter

def ls_end(m, game):
	# group 1 is player number
	playernum = m.group(1)
	# group 2 is pokemon nickname
	endpok = m.group(2)
	game.sides[playernum].pokemon[endpok].leechseed = ""

def status_start(m, game):
	# player num
	playernum = m.group(1)
	othernum = ""
	if playernum == '1':
		othernum = '2'
	else:
		othernum = '1'
	# nickname of pokemon that is statused
	statuspok = m.group(2)
	# status condition
	status = m.group(3)
	# additional status info
	extrainfo = m.group(4)
	
	# if status condition isn't burn/psn/tox, ignore
	if status != 'psn' and status != 'brn' and status != 'tox':
		return
	# if from item
	if extrainfo != None and extrainfo.find('item') != -1:
		#print("found item status")
		# assign statuser to itself
		if status == 'brn':
			game.sides[playernum].pokemon[statuspok].burned = "self"
		else:
			game.sides[playernum].pokemon[statuspok].poisoned = "self"
		return
	# if from ability in the extra info, assign statuser as other active pokemon
	if extrainfo != None and extrainfo.find('ability') != -1:
		#print("found ability status")
		# get other active pokemon
		statuser = game.sides[othernum].activepok
		# assign statuser to otherpok
		if status == 'brn':
			game.sides[playernum].pokemon[statuspok].burned = statuser
		else:
			game.sides[playernum].pokemon[statuspok].poisoned = statuser
	# if brn, assign to other active pokemon
	if status == 'brn':
		# get other active pokemon
		statuser = game.sides[othernum].activepok
		game.sides[playernum].pokemon[statuspok].burned = statuser
	# if poison, check if last event was switch (then cause was hazards)
	if status == 'tox' or status == 'psn':
		if game.lastevent == 'switch':
			assert(game.sides[playernum].hazards['tspikes'] != ''), "Detected status and switch, but no tspiker"
			tspiker = game.sides[playernum].hazards['tspikes']
			game.sides[playernum].pokemon[statuspok].poisoned = tspiker
		else:
			# get other active pokemon
			statuser = game.sides[othernum].activepok
			game.sides[playernum].pokemon[statuspok].poisoned = statuser

def cure_status(m, game):
	# group 1 is player number
	# group 3 is the status condition
	playernum = m.group(1)
	statusedpok = m.group(2)
	# clear all statuses for the pokemon
	game.sides[playernum].pokemon[statusedpok].poisoned = ""
	game.sides[playernum].pokemon[statusedpok].burned = ""

def move(m, game):
	game.lastevent = "move"
	# group 1 is player number
	playernum = m.group(1)
	# group 2 is pok nickname
	movepok = m.group(2)
	# group 3 is move
	themove = m.group(3)
	# set move
	game.sides[playernum].move = themove
	game.sides[playernum].usedmove = True

def hazard_start(m, game):
	#print("hazard started")
	# group 1 is the player num the hazards are now on
	playernum = m.group(1)
	move = m.group(3)
	hazardstarter = ""
	# get other active pokemon that used hazard move
	if playernum == '1':
		hazardstarter = game.sides['2'].activepok
	else:
		hazardstarter = game.sides['1'].activepok
	# set the name of the pokemon that used the hazard move in the hazards dictionary
	# of the side that the hazards are on
	if move == 'Stealth Rock':
		game.sides[playernum].hazards['stealthrocks'] = hazardstarter
	elif move == 'Toxic Spikes':
		game.sides[playernum].hazards['tspikes'] = hazardstarter
	else:
		# increment number of spikes on the side
		game.sides[playernum].hazards['numspikes'] += 1
		spikenum = game.sides[playernum].hazards['numspikes']
		# set spiker
		spikekey = 'spikes' + str(spikenum)
		game.sides[playernum].hazards[spikekey] = hazardstarter

def hazard_end(m, game):
	#print("hazard ended")
	playernum = m.group(1)
	move = m.group(3)
	if move == 'Stealth Rock':
		game.sides[playernum].hazards['stealthrocks'] = ''
	elif move == 'Toxic Spikes':
		game.sides[playernum].hazards['tspikes'] = ''
	else:
		# clear all spikes and numspikes
		game.sides[playernum].hazards['spikes1'] = ''
		game.sides[playernum].hazards['spikes2'] = ''
		game.sides[playernum].hazards['spikes3'] = ''
		game.sides[playernum].hazards['numspikes'] = 0

def weather(m, game):
	typeweather = m.group(1)
	upkeep = m.group(3)
	abilityinfo = m.group(4)
	# if upkeep, ignore
	if upkeep == '[upkeep]':
		return
	# clear weather
	game.weather['sandstorm'] = ""
	game.weather['hail'] = ""
	game.weather['startedby'] = ""
	# if none, weather ended so return
	if typeweather == 'none':
		return
	# if last even was switch, weather was started from ability
	if game.lastevent == 'switch':
		# match side and pokemon name
		a = re.search(r'p([0-9])a: (.*)', abilityinfo)
		side = a.group(1)
		pokname = a.group(2)
		if typeweather == 'Hail':
			game.weather['hail'] = pokname
			game.weather['startedby'] = side
		if typeweather == 'Sandstorm':
			game.weather['sandstorm'] = pokname
			game.weather['startedby'] = side
	if game.lastevent == 'move':
		# don't record if its not Sandstorm or Hail
		if typeweather == 'RainDance' or typeweather == 'SunnyDay':
			return
		if typeweather == 'Sandstorm':
			# check which side used sandstorm
			if game.sides['1'].move == "Sandstorm":
				game.weather['sandstorm'] = game.sides['1'].activepok
				game.weather['startedby'] = '1'
			else:
				game.weather['sandstorm'] = game.sides['2'].activepok
				game.weather['startedby'] = '2'
		if typeweather == 'Hail':
			# check which side used sandstorm
			if game.sides['1'].move == "Hail":
				game.weather['hail'] = game.sides['1'].activepok
				game.weather['startedby'] = '1'
			else:
				game.weather['hail'] = game.sides['2'].activepok
				game.weather['startedby'] = '2'
	
# Assumes no EVs, max IVs, and level 100
def calcHPfromstat(HPstat):
	return ((2 * HPstat + 31) * 100) + 110

# TODO remember that damage from status can come due to the pokemon itself, so "self" might be statuser
# TODO remember damagedpok's ability might cause pok to take damage (ex: Dry Skin in Sun)
# TODO this doesn't handle shedninja, something to fix for next league
def damage(m, game):
	playernum = m.group(1)
	damagedpok = m.group(2)
	hpinfo = m.group(3)
	frominfo = m.group(4)
	ofinfo = m.group(5)
	pokhpstat = game.sides[playernum].pokemon[damagedpok].hpstat
	remhp = game.sides[playernum].pokemon[damagedpok].remaininghp
	damagedone = 0
	faint = False
	fromabl = False
	frommov = False
	fromcurse = False
	fromspikes = False
	fromrocks = False
	# check if pokemon fainted
	if re.search(r'fnt', hpinfo) != None:
		faintflag = True
		# calculate damage done
		damagedone = 0.01 * remhp * calcHPfromstat(pokhpstat)
		# set remhp to 0
		game.sides[playernum].pokemon[damagedpok].remaininghp = 0
	# get damage done otherwise
	else:
		dmg = re.search(r'([0-9]+)\\/([0-9]+)', hpinfo)
		newremhp = int(dmg.group(1))
		totalhp = int(dmg.group(2))
		# normalize hp out of 100 if it isn't already
		if totalhp != 100:
			newremhp = 100 * newremhp / totalhp
			totalhp = 100
		# calculate new 
		damagedone = 0.01 * (remhp - newremhp) * calcHPfromstat(pokhpstat)
		# set new remaining hp
		game.sides[playernum].pokemon[damagedpok].remaininghp = newremhp












