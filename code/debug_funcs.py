import re
def db_print_switches(game):
	for key in game.sides['1'].pokemon:
		name = game.sides['1'].pokemon[key].name
		switchouts = game.sides['1'].pokemon[key].stats['switchouts']
		switchins = game.sides['1'].pokemon[key].stats['switchins']
		print(key + " switched out " + str(switchouts) + " and switched in " + str(switchins))

	for key in game.sides['2'].pokemon:
		name = game.sides['2'].pokemon[key].name
		switchouts = game.sides['2'].pokemon[key].stats['switchouts']
		switchins = game.sides['2'].pokemon[key].stats['switchins']
		print(key + " switched out " + str(switchouts) + " and switched in " + str(switchins))

def db_print_miss(game):
	for key in game.sides['1'].pokemon:
		name = game.sides['1'].pokemon[key].name
		misses = game.sides['1'].pokemon[key].stats['misses']
		print(key + " missed " + str(misses))

	for key in game.sides['2'].pokemon:
		name = game.sides['2'].pokemon[key].name
		misses = game.sides['2'].pokemon[key].stats['misses']
		print(key + " missed " + str(misses))


def db_print_crit(game):
	for key in game.sides['1'].pokemon:
		misses = game.sides['1'].pokemon[key].stats['crits']
		print(key + " got " + str(misses) + " crits")

	for key in game.sides['2'].pokemon:
		misses = game.sides['2'].pokemon[key].stats['crits']
		print(key + " got " + str(misses) + " crits")

def db_print_leechseed(game):
	for key in game.sides['1'].pokemon:
		if game.sides['1'].pokemon[key].leechseed != "":
			lspok = game.sides['1'].pokemon[key].leechseed
			print(key + " is " + " leechseeded by " + lspok)

	for key in game.sides['2'].pokemon:
		if game.sides['2'].pokemon[key].leechseed != "":
			lspok = game.sides['2'].pokemon[key].leechseed
			print(key + " is " + " leechseeded by " + lspok)

def db_print_moves(game):
	print("printing moves")
	print("side 1: " + game.sides['1'].move)
	print("side 2: " + game.sides['2'].move)

def db_print_statuses(game):
	for key in game.sides['1'].pokemon:
		if game.sides['1'].pokemon[key].burned != "":
			statuser = game.sides['1'].pokemon[key].burned
			print(key + " is burned by " + statuser)
		if game.sides['1'].pokemon[key].poisoned != "":
			statuser = game.sides['1'].pokemon[key].poisoned
			print(key + " is poisoned by " + statuser)
	
	for key in game.sides['2'].pokemon:
		if game.sides['2'].pokemon[key].burned != "":
			statuser = game.sides['2'].pokemon[key].burned
			print(key + " is burned by " + statuser)
		if game.sides['2'].pokemon[key].poisoned != "":
			statuser = game.sides['2'].pokemon[key].poisoned
			print(key + " is poisoned by " + statuser)

def db_print_hazards(game):
	print('hazards on side 1')
	sp1_1 = game.sides['1'].hazards['spikes1']
	sp1_2 = game.sides['1'].hazards['spikes2']
	sp1_3 = game.sides['1'].hazards['spikes3']
	ns1 = game.sides['1'].hazards['numspikes']
	sr1 = game.sides['1'].hazards['stealthrocks']
	ts1 = game.sides['1'].hazards['tspikes']
	if sp1_1 != '':
		print("1st spikes: " + sp1_1)
	if sp1_2 != '':
		print("2nd spikes: " + sp1_2)
	if sp1_3 != '':
		print("3rd spikes: " + sp1_3)
	if ns1 != 0:
		print("numspikes: " + str(ns1))
	if sr1 != '':
		print("stealth rocks: " + sr1)
	if ts1 != '':
		print("toxic spikes: " + ts1)

	print('hazards on side 2')
	sp2_1 = game.sides['2'].hazards['spikes1']
	sp2_2 = game.sides['2'].hazards['spikes2']
	sp2_3 = game.sides['2'].hazards['spikes3']
	ns2 = game.sides['2'].hazards['numspikes']
	sr2 = game.sides['2'].hazards['stealthrocks']
	ts2 = game.sides['2'].hazards['tspikes']
	if sp2_1 != '':
		print("1st spikes: " + sp2_1)
	if sp2_2 != '':
		print("2nd spikes: " + sp2_2)
	if sp2_3 != '':
		print("3rd spikes: " + sp2_3)
	if ns2 != 0:
		print("numspikes: " + str(ns2))
	if sr2 != '':
		print("stealth rocks: " + sr2)
	if ts2 != '':
		print("toxic spikes: " + ts2)

def db_print_weather(game):
	print('printing game weather')
	if game.weather['hail'] != '':
		pok = game.weather['hail']
		side = game.weather['startedby']
		print('Weather: Hail')
		print('Started by: ' + pok)
		print('Side: ' + side)
	elif game.weather['sandstorm'] != '':
		pok = game.weather['sandstorm']
		side = game.weather['startedby']
		print('Weather: Sandstorm')
		print('Started by: ' + pok)
		print('Side: ' + side)
	else:
		print('No weather')

def db_test_damage_regex():
	print('testing damage regex')
	allexs = [
		'|-damage|p1a: Registeel|297\\/301',
		'|-damage|p1a: Registeel|260\\/301|[from] move: Bind|[partiallytrapped]',
		'|-damage|p1a: Registeel|223\\/301 brn|[from] brn',
		'|-damage|p2a: m|75\\/100',
		'|-damage|p2a: f|88\\/100|[from] item: Black Sludge',
		'|-damage|p1a: Registeel|35\\/301 brn',
		'|-damage|p1a: Registeel|0 fnt|[from] brn',
		'|-damage|p1a: Regigigas|316\\/361|[from] Spikes',
		'|-damage|p2a: f|57\\/100',
		'|-damage|p1a: Regigigas|271\\/361|[from] ability: Iron Barbs|[of] p2a: f',
		'|-damage|p1a: Regigigas|226\\/361|[from] Leech Seed|[of] p2a: f',
		'|-damage|p1a: Regigigas|187\\/361',
		'|-damage|p1a: Regigigas|0 fnt',
		'|-damage|p1a: Regirock|246\\/301|[from] Hail',
		'|-damage|p2a: abo|99\\/100|[from] Recoil',
		'|-damage|p1a: Regirock|102\\/301|[from] Curse',
		'|-damage|p2a: g|45\\/100',
		'|-damage|p1a: Regirock|81\\/301|[from] confusion',
		'|-damage|p1a: Regirock|0 fnt|[from] confusion'
	]
	testing = [
		'|-damage|p1a: Registeel|297\\/301',
		'|-damage|p1a: Registeel|260\\/301|[from] move: Bind|[partiallytrapped]',
		'|-damage|p1a: Registeel|223\\/301 brn|[from] brn',
		'|-damage|p2a: m|75\\/100',
		'|-damage|p2a: f|88\\/100|[from] item: Black Sludge',
		'|-damage|p1a: Registeel|35\\/301 brn',
		'|-damage|p1a: Registeel|0 fnt|[from] brn',
		'|-damage|p1a: Regigigas|316\\/361|[from] Spikes',
		'|-damage|p2a: f|57\\/100',
		'|-damage|p1a: Regigigas|271\\/361|[from] ability: Iron Barbs|[of] p2a: f',
		'|-damage|p1a: Regigigas|226\\/361|[from] Leech Seed|[of] p2a: f',
		'|-damage|p1a: Regigigas|187\\/361',
		'|-damage|p1a: Regigigas|0 fnt',
		'|-damage|p1a: Regirock|246\\/301|[from] Hail',
		'|-damage|p2a: abo|99\\/100|[from] Recoil',
		'|-damage|p1a: Regirock|102\\/301|[from] Curse',
		'|-damage|p2a: g|45\\/100',
		'|-damage|p1a: Regirock|81\\/301|[from] confusion',
		'|-damage|p1a: Regirock|0 fnt|[from] confusion'
	]
	for line in testing:
		m = re.search(r'(?<=-damage\|)p([0-9])a: ([^\|]+)\|([^\|]+)\|?([^\|]+)?\|?([^\|]+)?', line)
		print("parsing: " + line)
		playernum = m.group(1)
		damagedpok = m.group(2)
		hpinfo = m.group(3)
		frominfo = m.group(4)
		ofinfo = m.group(5)
		if re.search(r'fnt', hpinfo) != None:
			faintflag = True
		# get damage done otherwise
		else:
			dmg = re.search(r'([0-9]+)\\/', hpinfo)
			newremhp = dmg.group(1)
			# assume damage is figured out
		#print(frominfo)
		# things to look for in the from
		# move:, brn, tox, pos, item:, Spikes, Leech, Hail, Recoil, confusion, Curse, ability:, Stealth
		# need to take into acount self-damaging moves
		# self damaging moves are curse, belly drum, substitute
		# there's a differnet pattern when the pokemon fainted and not fainted
		if frominfo != None:
			print("detected from section")
			#if re.search(r'\[from\] ([A-Za-z]+)') != None:
				# increment the damage done to this mon
		








