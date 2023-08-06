# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import random
import sys
# Third party imports
# Local application imports
import hexafid.hexafid_core as hexafid

# Base64 symbol set
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
# Association of quadtree addresses to row/col addresses in keysquare
KEYMAP = {
	'A1': '000000', 'B1': '000001', 'C1': '000100', 'D1': '000101',
	'E1': '010000', 'F1': '010001', 'G1': '010100', 'H1': '010101',
	'A2': '000011', 'B2': '000010', 'C2': '000111', 'D2': '000110',
	'E2': '010011', 'F2': '010010', 'G2': '010111', 'H2': '010110',
	'A3': '001100', 'B3': '001101', 'C3': '001000', 'D3': '001001',
	'E3': '011100', 'F3': '011101', 'G3': '011000', 'H3': '011001',
	'A4': '001111', 'B4': '001110', 'C4': '001011', 'D4': '001010',
	'E4': '011111', 'F4': '011110', 'G4': '011011', 'H4': '011010',
	'A5': '110000', 'B5': '110001', 'C5': '110100', 'D5': '110101',
	'E5': '100000', 'F5': '100001', 'G5': '100100', 'H5': '100101',
	'A6': '110011', 'B6': '110010', 'C6': '110111', 'D6': '110110',
	'E6': '100011', 'F6': '100010', 'G6': '100111', 'H6': '100110',
	'A7': '111100', 'B7': '111101', 'C7': '111000', 'D7': '111001',
	'E7': '101100', 'F7': '101101', 'G7': '101000', 'H7': '101001',
	'A8': '111111', 'B8': '111110', 'C8': '111011', 'D8': '111010',
	'E8': '101111', 'F8': '101110', 'G8': '101011', 'H8': '101010',
}


def main():

	print('Random Key: ' + get_random_key())

	key = SYMBOLS
	print('Case 0 Key (sequence order): ' + SYMBOLS)
	print('Case 0 Key (quadress order): ' + use_sequence_layout(key))
	print('Case 0: ' + 'DROP --> ' + hexafid.encrypt('DROP', key, 'ECB', '1337', 4, 1))

	key = use_sequence_layout(get_key_from_pass('MyPassword123', 'forward'))
	print('Case 1 Key (sequence order): ' + get_key_from_pass('MyPassword123', 'forward'))
	print('Case 1 key (quadress order): ' + key)
	print('Case 1: ' + 'Hello World --> ' + hexafid.encrypt('Hello World', key, 'ECB', '31337', 5, 1))

	key = use_quadress_layout(use_sequence_layout(get_key_from_pass('MyPassword123', 'forward')))
	print('Case 2 Key (sequence order): ' + get_key_from_pass('MyPassword123', 'forward'))
	print('Case 2 key (quadress order(sequence order)): ' + key)
	print('Case 2: ' + 'Hello World --> ' + hexafid.encrypt('Hello World', key, 'ECB', '31337', 5, 1))


def get_iv(period: int) -> str:
	"""
	This functions returns a randomly generated initialization vector given the period.

	:param period:		an integer representing the number of Base64 characters in a block
	:return: 			a string representing an IV matching the period length
	"""
	return ''.join(random.SystemRandom().choices(list(SYMBOLS), k=period))


def get_random_key() -> str:
	"""
	This function returns a randomly generated key from the Base64 character set.

	:return:			a string representing a permutation of the Base64 character set
	"""
	key = list(SYMBOLS)
	random.SystemRandom().shuffle(key)

	return ''.join(key)


# helper to preserve order in set()
def unique(sequence: str) -> list:
	"""
	This function returns an ordered list of distinct characters given a string with possible duplicates.

	:param sequence:		a string that could have possible duplicate values
	:return: 				a list with the original character string order preserved but duplicates removed
	"""
	seen = set()
	return [x for x in sequence if not (x in seen or seen.add(x))]


def get_key_from_pass(pwd: str, mode: str, kdf: bool = True) -> str:
	"""
	This function returns a key sting given a password and the method for completing the keysquare. Following
	classical methods, a password is first stripped of any duplicate characters before assignment at the beginning
	(i.e. the top left positions) of the keysquare.	Then the remaining available characters in the Base64 character
	set fill the remaining cells in the keysquare ordered left to right (i.e. cols) top to bottom (i.e. rows).
	The method for filling the remaining cells can signal the 'forward', 'reverse', or 'alternating' placement of
	remaining characters.

	:param kdf:			a flag - True if using KDF with salt, otherwise do not use KDF
	:param pwd: 		a string representing a user selected password
	:param mode: 		a string representing the filling method: 'forward', 'reverse', or 'alternating'
	:return: 			a string key that is a permutation of the Base64 character set
	"""
	# check for valid b64 symbols
	if not all(s in SYMBOLS for s in pwd):
		sys.exit('Invalid Password')

	pwd_distinct = ''.join(unique(pwd))
	# sym_distinct forward mode
	sym_distinct = ''.join(s for s in SYMBOLS if s not in pwd_distinct)

	if mode == 'reverse':
		sym_distinct = sym_distinct[::-1]
	elif mode == 'alternate':
		sym_distinct = sym_distinct[1::2] + sym_distinct[0::2][::-1]

	key = pwd_distinct + sym_distinct

	if kdf:
		salt = list(sym_distinct)  # ideally this is globally unique
		random.SystemRandom().shuffle(salt)
		salted_key = pwd_distinct + ''.join(salt)
		key = derive_master_key(salted_key, 2048)  # this number affects time and memory

	return key


def derive_master_key(key: str, rounds: int) -> str:
	"""
	This function transforms a weak key (e.g. password) into a stronger key by iterating through the key schedule
	a large number of times with a memory intensive computation.

	:param key: 		a permutation of the Base 64 character set
	:param rounds: 		an integer representing the number of iterations through the key schedule
	:return: 			a strengthened key that has emerged from a large number of key schedule iterations
	"""
	round_keyset = hexafid.setup_keys(key, rounds)

	return ''.join(round_keyset[rounds - 1][0])


def use_quadress_layout(key: str) -> str:
	"""
	This function reorganizes key characters to sort following a quadress ordering scheme (i.e. 000000 to 111111).
	It returns a key that, when sequence-addressed (as a natural key) in this algorithm, reverts to the machine order
	of expressing a key through quadtree addressing.

	:param key:			a string permutation of the Base64 character set
	:return:			a re-ordered string permutation of the Base64 character set
	"""
	quads = ['00', '01', '10', '11']
	machine_layout = {}
	index = 0

	for top in quads:
		for middle in quads:
			for bottom in quads:
				address = top + middle + bottom
				machine_layout[address] = key[index]
				index = index + 1

	human_layout = {}
	for human, machine in KEYMAP.items():
		if machine in machine_layout.keys():
			human_layout[human] = machine_layout[machine]

	# sort key according to natural addresses (i.e. row by row sequence)
	values = []
	for k in human_layout:
		values.append(human_layout[k])
	key = ''.join(values)

	return key


def use_sequence_layout(key: str) -> str:
	"""
	This function reorganizes characters in a key to sort following a sequence ordering scheme (i.e. 1 to 64).
	It returns a key that, when addressed as a quadtree in this algorithm, mimics the natural order of
	writing a key by hand - row by row (i.e. sequence addressing).

	:param key: 		a string permutation of the Base64 character set
	:return: 			a re-ordered string permutation of the Base64 character set
	"""
	# create human_layout dict representing most natural row/col addressing of key
	rows = '12345678'
	cols = 'ABCDEFGH'
	human_layout = {}
	index = 0
	for row in rows:
		for col in cols:
			address = col + row
			human_layout[address] = key[index]
			index = index + 1

	# create machine_layout dict representing quadtree addressing of key
	machine_layout = {}
	for k in KEYMAP.keys():
		if k in human_layout.keys():
			machine_layout[KEYMAP[k]] = human_layout[k]

	# sort key according to quadtree addresses (i.e. quadresses)
	values = []
	for k in sorted(machine_layout):
		values.append(machine_layout[k])
	key = ''.join(values)

	# print(human_layout)
	# print(machine_layout)

	return key


# If run instead of called
if __name__ == '__main__':
	main()
