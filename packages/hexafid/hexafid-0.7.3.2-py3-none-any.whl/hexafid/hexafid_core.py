# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import re
import sys
import math
import base64

# Third party imports
# Local application imports
import hexafid.hexafid_keygen as keygen

# DONE Enhance: feed methods with period
# DONE Module: regression tests suite
# DONE Feature: verbose output
# DONE Feature: word separator
# DONE Module: file encryptor/decryptor
# DONE Feature: multiple round logic
# DONE Feature: password based keygen
# DONE Enhance: pass keygen reverse alternate
# DONE Enhance: make clipboard cross platform
# DONE Module: separate key generation
# DONE Enhance: pen and code keygen parity
# DONE Defect: rounds should operate on blocks not as super encryption
# DONE Feature: block pad - method 2 ISO/IEC 9797-1 or n bytes of n
# DONE Feature: ECB, CBC and CTR modes
# DONE Module: NIST randomness tests
# PART Enhance: unit tests for each method
# PART Enhance: performance refactoring

# Base64 symbol set
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
BITS = 6
VERBOSE = False


def main():
    test_vectors = [
        # first Hexafid by hand - before IV (CBC) and pad feature
        ['DROP', SYMBOLS, 'ECB', '1337', 4, 1, False, False, 'Aiw5'],
        # first Stegafid by hand - before IV (CBC) and pad feature - was SGVsbG8= ('Hello' in B64)
        ['SGVsbG8sfQHOss==', 'sBEFwRUnDCHSktXWMNzJcGYZP8LKfeIaQx01ghTlbyr2jiomO945AdVp/+76vu3q',
         'ECB', '1234567', 7, 1, False, False, 'Itworks'],
        ['Hello World!!!', 'MyPassword123', 'ECB', '31337', 5, 1, False, False,
         'I31AsfWdyfypMMM='],  # was 'I31AsfWdyf==' before pad feature
        ['Attack at dawn', 'MyPassword123', 'ECB', '31337', 5, 1, False, False],
        # first Hexafid in CBC mode by hand
        ['Hello World!!!', 'MyPassword123', 'CBC', 'kLi7d', 5, 1, False, False,
         'kLi7doFcCv9yTi7EW2cM'],  # was 'oFcCv9yTi7==' before IV (CBC) and pad feature
        ['Hello World!!!', 'MyPassword123', 'CBC', 'fLuwo3b', 7, 1, True, False,
         'fLuwo3bpCJMQEulzELPCBedVKGxS'],
        # Test vector for field cipher use - worked by hand
        ['Keep it secret. Keep it safe.', 'MyPassword123', 'CBC', 'w3Der4LeOd', 10, 1, True, False,
         'w3Der4LeOdLCI81kj1u7vJcTFfBtssEhItv24P3m'],
    ]
    example = 6
    my_plaintext = test_vectors[example][0]
    my_key = keygen.get_key_from_pass(test_vectors[example][1], 'forward', False)  # False to skip KDF
    my_mode = test_vectors[example][2]  # CBC, CTR or ECB
    my_iv = test_vectors[example][3]  # for test and demo purposes only, use random IVs
    my_period = test_vectors[example][4]  # 10  # 8-32 seems standard, no greater than 1/2 key length
    my_rounds = test_vectors[example][5]  # 1  # 16-32 rounds seem standard for most block ciphers
    my_separator = test_vectors[example][6]
    my_preserve = test_vectors[example][7]
    # my_ciphertext = test_vectors[example][8]

    # my_key = SYMBOLS
    # my_iv = keygen.get_iv(my_period)

    encrypted = encrypt(my_plaintext, my_key, my_mode, my_iv, my_period, my_rounds, my_separator, my_preserve)
    decrypted = decrypt(encrypted, my_key, my_mode, my_period, my_rounds, my_separator, my_preserve)

    print('Message: %s' % my_plaintext)
    print('Key: %s' % my_key)
    print('IV: %s' % my_iv)
    print('Mode: %s' % my_mode)
    print('Period: %s' % my_period)
    print('Rounds: %s' % my_rounds)
    print('Encrypted Text: %s' % encrypted)
    print('Decrypted Text: %s' % decrypted)


def encrypt(message: str, key: str, mode: str, iv: str, period: int, rounds: int,
            separator: bool = False, preserve: bool = True) -> str:
    """
    The core encryption function and main entry point for encrypting a message with Hexafid.

    :param message:         the original message string to be encrypted
    :param key:             a string permutation of the Base64 character set
    :param mode:            the chosen block cipher mode: ECB, CBC, or CTR
    :param iv:              an initialization vector for use in CBC and CTR modes
    :param period:          the block size, or length, in number of characters
    :param rounds:          the number of iterations for the round function
    :param separator:       a flag - True to replace whitespace with a Base64 separator "/"
    :param preserve:        a flag - True to preserve the original message format by Base64 encoding
    :return:                the final ciphertext string after encryption
    """
    if not key_is_valid(key):
        sys.exit('There is an error in the key or symbol set.')
    if not iv_is_valid(iv, period):
        sys.exit('There is an error in the IV or symbol set.')
    # if not period_is_valid(period):
    #      sys.exit('There is an error in the period or block size.')
    # if not rounds_is_valid(rounds):
    #      sys.exit('There is an error in the number of rounds.')

    round_keyset = setup_keys(key, rounds)

    if preserve:
        message = base64.b64encode(bytes(message, 'utf-8')).decode('utf-8')  # ISO-8859-1 or utf-8

    plaintext = prepare_message(message, separator)  # if separator add it and remove non-b64 chars
    plaintext_blocks = _separate_plain_blocks(plaintext, period, key, mode)  # put into blocks and add any padding

    if mode == 'CBC':
        assembled_ciphertext = _encrypt_mode_cbc(plaintext_blocks, rounds, round_keyset, iv)
    elif mode == 'CTR':
        assembled_ciphertext = _encrypt_mode_ctr(plaintext_blocks, rounds, round_keyset, iv)
    elif mode == 'ECB':
        assembled_ciphertext = _encrypt_mode_ecb(plaintext_blocks, rounds, round_keyset)
    else:
        sys.exit("There is an error in the mode request.")

    return assembled_ciphertext


def _encrypt_mode_cbc(plaintext_blocks: list, rounds: int, round_keyset: list, iv: str) -> str:
    """
    This function encrypts a list of plaintext block strings using CBC mode over a number of rounds with a given
    initialization vector and a set of round keys.

    :param plaintext_blocks:    a list of block strings
    :param rounds:              an integer number of rounds for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :param iv:                  an initialization vector equal in length to each block
    :return:                    an assembled ciphertext string
    """
    seq_encoder = round_keyset[0][2]
    seq_decoder = round_keyset[0][3]
    ciphertext_blocks = list()
    previous_block = ''
    index = 0

    for plaintext_block in plaintext_blocks:
        # Cipher Block Chaining (CBC) Mode
        # IV must be random to preserve semantic security against CPA
        if previous_block == '':
            previous_block = iv
            ciphertext_blocks.append(iv)
        else:
            previous_block = ciphertext_blocks[index]

        input_block = _add_blocks_mod64(plaintext_block, previous_block, seq_encoder, seq_decoder)
        output_block = _block_encrypt(input_block, rounds, round_keyset)
        ciphertext_blocks.append(output_block)
        index += 1

    assembled_ciphertext = add_b64_padding(''.join(ciphertext_blocks))

    return assembled_ciphertext


def _encrypt_mode_ctr(plaintext_blocks: list, rounds: int, round_keyset: list, iv: str) -> str:
    """
    This function encrypts a list of plaintext block strings using CTR mode over a number of rounds with a given
    initialization vector and a set of round keys.

    :param plaintext_blocks:    a list of block strings
    :param rounds:              an integer number of rounds for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :param iv:                  an initialization vector equal in length to each block
    :return:                    an assembled ciphertext string
    """
    seq_encoder = round_keyset[0][2]
    seq_decoder = round_keyset[0][3]
    period = len(plaintext_blocks[0])
    ciphertext_blocks = list()
    counter = 0
    for plaintext_block in plaintext_blocks:
        # Check for counter roll over that would result in easily breakable two time pad
        if len(plaintext_blocks) > (10 ** (period / 2)) - 1:  # watch for rollover
            sys.exit('Counter mode roll over warning. A larger block size is required for this message.')
        else:
            # input_block = iv[:-len(str(counter))] + str(counter)  # grow space for counter
            # input_block is a random nonce (rounded up per NIST 800-38a) on left concatenated with counter on right
            input_block = iv[:int(math.ceil(period / 2))] + str(counter).zfill(int(math.floor(period / 2)))
        if counter == 0:
            # ciphertext_blocks.append(input_block)
            ciphertext_blocks.append(iv)  # insert full iv at start of ciphertext

        output_block = _block_encrypt(input_block, rounds, round_keyset)
        ciphertext_block = _add_blocks_mod64(output_block, plaintext_block, seq_encoder, seq_decoder)
        ciphertext_blocks.append(ciphertext_block)
        counter += 1

    assembled_ciphertext = add_b64_padding(''.join(ciphertext_blocks))

    return assembled_ciphertext


def _encrypt_mode_ecb(plaintext_blocks: list, rounds: int, round_keyset: list) -> str:
    """
    This function encrypts a list of plaintext block strings using ECB mode over a number of rounds with
    a set of round keys.

    :param plaintext_blocks:    a list of block strings
    :param rounds:              an integer number of rounds for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :return:                    an assembled ciphertext string
    """
    ciphertext_blocks = list()
    for plaintext_block in plaintext_blocks:
        # Electronic Code Book (ECB) Mode - preserved to maintain compatibility as field cipher
        # NOT semantically secure beyond one block with same key; use unique keys for each block
        input_block = plaintext_block
        output_block = _block_encrypt(input_block, rounds, round_keyset)
        ciphertext_blocks.append(output_block)

    assembled_ciphertext = add_b64_padding(''.join(ciphertext_blocks))

    return assembled_ciphertext


def _block_encrypt(current_block: str, rounds: int, round_keys: list) -> str:
    """
    This is the eponymous round function for encryption that includes the fundamental
    fractionated substitution and columnar transposition steps of the Hexafid cipher.

    :param current_block:       the plaintext block string under encryption
    :param rounds:              the number of round iterations for the algorithm
    :param round_keys:          a list of the round keys for each round
    :return:                    the ciphertext block string after encryption
    """
    for r in range(rounds):

        # Binary substitution step
        substituted_bitslist = _get_quadress_values(current_block, round_keys[r][0])

        # Columnar transposition step
        unpacked_bitslist = [''.join(s) for s in zip(*substituted_bitslist)]
        transposed_bitstring = ''.join(unpacked_bitslist)
        transposed_bitslist = [transposed_bitstring[i:i + BITS] for i in range(0, len(transposed_bitstring), BITS)]

        # Turn back into character string
        transposed_charlist = _get_quadress_chars(transposed_bitslist, round_keys[r][1])
        current_block = ''.join(transposed_charlist)

        # Add round key
        # round_key_block = ''.join(round_keys[r][2])
        # current_block = _add_blocks_mod64(current_block, round_key_block, round_keys[r][2], round_keys[r][3])

    return current_block


def setup_keys(key: str, rounds: int) -> list:
    """
    This function sets up and returns the round keys. This is a pre-computation step for the cipher algorithm and
    requires the source key and the number of rounds for setup.

    :param key:             a string permutation of the Base64 character set
    :param rounds:          an integer number of iterations intended for the block algorithm
    :return:                a list of lists; each round list item contains a list of a quadress encoder/decoder,
                            sequence encoder/decoder and a dynamic magic number that drives row shifting in
                            the key schedule
    """
    # setup encoders
    seq_encoder, seq_decoder = setup_sequence_addresses(key)
    quad_encoder, quad_decoder = setup_quadtree_addresses(key)

    # setup round keys for key schedule
    round_keyset = list()
    magic_number = 42  # nothing up my sleeves number to initialize key schedule
    # This first round key allows for direct use of K0 = K to simplify field use before key scheduling
    round_keyset.append((quad_encoder, quad_decoder, seq_encoder, seq_decoder, magic_number))
    # The rest of the key schedule is established here
    for r in range(rounds - 1):
        round_keyset.append(get_round_keys(round_keyset[r][0], round_keyset[r][1],
                                           round_keyset[r][2], round_keyset[r][3], round_keyset[r][4]))

    return round_keyset


def get_round_keys(quad_encoder: dict, quad_decoder: dict, seq_encoder: dict, seq_decoder: dict,
                   magic_number: int) -> (dict, dict, dict, dict, int):
    """
    This function implements the key schedule and establishes the set of round keys used for the cipher. The
    key schedule includes substitution of each key character through an APN s-box, a shifting of key rows,
    and a permutation of key columns.

    :param quad_encoder:        a dictionary of key (character), value (quadress) pairs - inverse of decoder
    :param quad_decoder:        a dictionary of key (quadress), value (character) pairs - inverse of encoder
    :param seq_encoder:         a dictionary of key (character), value (sequence) pairs - inverse of decoder
    :param seq_decoder:         a dictionary of key (sequence), value (character) pairs - inverse of encoder
    :param magic_number:        an integer pointer combined with the key to drive the shift rows step
    :return:                    a round key stored as encoder and decoder dicts and the next magic number
    """
    # Key Schedule
    # follows a mix of Fides (s-box) and shift rows and mix columns (rotate) applied to key schedule
    # kn = Substitute (s-box) -> Shift (kn-1, xn) -> Permute (rotate90)
    # also: kn = Permute(Shift(Substitute(kn-1), xn))
    # where: xn = (xn-1 + x'n-1) % 64

    # Find next shift number (xn) from magic seed its position in the base symbol set
    sequence_number = SYMBOLS.find(seq_decoder[magic_number]) + 1
    shift_number = (magic_number + sequence_number) % 64
    if shift_number == 0:  # addresses 64 % 64 = 0 cycling back to 64 in alignment with end user sequence
        shift_number = 64

    # SubBytes - Substitute encoder values from trip to the APN s-box
    boxed_quad_encoder, boxed_quad_decoder = _sbox_encoders(quad_encoder, quad_decoder)

    # ShiftRows - Shift key left in each row by a dynamic generator seeded with a magic number
    shifted_quad_encoder, shifted_quad_decoder = _shift_rows(boxed_quad_encoder, shift_number)

    # Mix Columns - by rotating keysquare clockwise 90 degrees
    mixed_quad_encoder, mixed_quad_decoder = _rotate_encoders(shifted_quad_encoder, shifted_quad_decoder)

    # Build new sequence encodings
    key = ''.join(list(mixed_quad_encoder))
    mixed_seq_encoder, mixed_seq_decoder = setup_sequence_addresses(key)

    return mixed_quad_encoder, mixed_quad_decoder, mixed_seq_encoder, mixed_seq_decoder, shift_number


def _shift_rows(quad_encoder: dict, shift_number: int) -> (dict, dict):
    """
    This function performs a dynamic shift on the encoders. A simple cyclic shift would look like this:
    e.g. {'M': '000000', 'y': '000001', 'P': '000100}  --> {'M': '000001', 'y': '000100', 'P': '000000'}
    The actual shift applies a different shift to each row in the keysquare based on a dynamically changing
    shift number.

    :param quad_encoder:        a dictionary of key (quadress), value (character) pairs
    :param shift_number:        a shift number that drives different row shifts of the keysquare
    :return:                    a new row-shifted quad encoder/decoder pair
    """
    # ShiftRows - Shift key left in each row by a dynamic generator seeded with a magic number
    key = ''.join(list(quad_encoder))
    old_rows, new_rows = [], []
    col = 8  # for the 64 char key this equates to an 8x8 matrix
    for row in range(8):  # int(len(key) / col)):
        old_rows.append(key[row * col:(row + 1) * col])
        gen = shift_number % col
        # new_rows.append(old_rows[row][(gen * row) % col:] + old_rows[row][:(gen * row) % col])  # 7 shifts + 1 none
        new_rows.append(old_rows[row][(gen ** row) % col:] + old_rows[row][:(gen ** row) % col])  # 8 shifts, unique
        # new_rows.append(old_rows[row][(row ** gen) % col:] + old_rows[row][:(row ** gen) % col])  # 5 shifts, 3 repeat

    # # ShiftRows - Shift key left in each row by row number - no dynamic shift number used
    # key = ''.join(list(quad_encoder))
    # old_rows, new_rows = [], []
    # col = 8  # 8x8 matrix for 64 char key
    # for row in range(8):  # 8x8 matrix for 64 char key
    #     old_rows.append(key[row * col:(row + 1) * col])
    #     new_rows.append(old_rows[row][row:] + old_rows[row][:row])

    shifted_key = ''.join(new_rows)
    shifted_quad_encoder, shifted_quad_decoder = setup_quadtree_addresses(shifted_key)

    return shifted_quad_encoder, shifted_quad_decoder


def _add_blocks_mod64(first_block: str, second_block: str, seq_encoder: dict, seq_decoder: dict) -> str:
    """
    This function looks up the sequence values for each character in each block using the current key
    and then adds the two blocks together modulo 64.

    :param first_block:         a block string of characters
    :param second_block:        another block string of characters
    :param seq_encoder:         the current key represented as an encoder dictionary
    :param seq_decoder:         the current key represented as a decoder dictionary
    :return:                    the combined block string.
    """
    # Sequential substitution step
    first_block_list = _get_sequence_values(first_block, seq_encoder)
    second_block_list = _get_sequence_values(second_block, seq_encoder)

    # Modular addition step
    modulo_numlist = [(x + y) % 64 for x, y in zip(first_block_list, second_block_list)]
    modulo_charlist = _get_sequence_chars(modulo_numlist, seq_decoder)

    combined_block = ''.join(modulo_charlist)

    return combined_block


def _subtract_blocks_mod64(first_block: str, second_block: str, seq_encoder: dict, seq_decoder: dict) -> str:
    """
    This function looks up the sequence values for each character in each block using the current key
    and then subtracts the second block from the first block modulo 64.

    :param first_block:         a string of characters
    :param second_block:        another string of characters
    :param seq_encoder:         the current key represented as an encoder dictionary
    :param seq_decoder:         the current key represented as a decoder dictionary
    :return:                    the combined block string.
    """
    # Sequential substitution step
    first_block_list = _get_sequence_values(first_block, seq_encoder)
    second_block_list = _get_sequence_values(second_block, seq_encoder)

    # Modular subtraction step
    modulo_numlist = [(x - y) % 64 for x, y in zip(first_block_list, second_block_list)]
    modulo_charlist = _get_sequence_chars(modulo_numlist, seq_decoder)

    uncombined_block = ''.join(modulo_charlist)

    return uncombined_block


def decrypt(message: str, key: str, mode: str, period: int, rounds: int, separator: bool = False,
            preserve: bool = True) -> str:
    """
    The core decryption function and main entry point for decrypting a Hexafid encrypted message.

    :param message:         the original message string to be decrypted
    :param key:             a string permutation of the Base64 character set
    :param mode:            the chosen block cipher mode: ECB, CBC, or CTR
    :param period:          the block size, or length, in number of characters
    :param rounds:          the number of iterations for the round function
    :param separator:       a flag - True to replace whitespace with a Base64 separator "/"
    :param preserve:        a flag - True to preserve the original message format by Base64 encoding
    :return:                the final plaintext string after decryption
    """
    if not key_is_valid(key):
        sys.exit('There is an error in the key or symbol set.')
    if not ciphertext_is_valid(message, period):
        sys.exit('There is an error in the ciphertext.')
    # if not period_is_valid(period):
    #      sys.exit('There is an error in the period or block size.')
    # if not rounds_is_valid(rounds):
    #      sys.exit('There is an error in the number of rounds.')

    round_keyset = setup_keys(key, rounds)

    ciphertext = prepare_message(message, separator)  # also removes any b64 padding
    ciphertext_blocks = _separate_cipher_blocks(ciphertext, period)

    if mode == 'CBC':
        assembled_plaintext = _decrypt_mode_cbc(ciphertext_blocks, rounds, round_keyset)
    elif mode == 'CTR':
        assembled_plaintext = _decrypt_mode_ctr(ciphertext_blocks, rounds, round_keyset)
    elif mode == 'ECB':
        assembled_plaintext = _decrypt_mode_ecb(ciphertext_blocks, rounds, round_keyset)
    else:
        sys.exit("There is an error in the mode request.")

    if preserve:
        assembled_plaintext = base64.b64decode(add_b64_padding(assembled_plaintext)).decode('utf-8')

    return assembled_plaintext


def _decrypt_mode_cbc(ciphertext_blocks: list, rounds: int, round_keyset: list) -> str:
    """
    This function decrypts a list of ciphertext block strings using CBC mode over a number of rounds using a
    given set of round keys and extracting an initialization vector from the first block.

    :param ciphertext_blocks:   a list of block strings
    :param rounds:              an integer number of iterations for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :return:                    an assembled ciphertext string
    """
    # Cipher Block Chaining (CBC) Mode - IV must be random to preserve semantic security against CPA
    source_key = keygen.use_quadress_layout(''.join(round_keyset[0][0]))
    seq_encoder = round_keyset[0][2]
    seq_decoder = round_keyset[0][3]
    plaintext_blocks = list()
    previous_block = ''
    index = 0

    for ciphertext_block in ciphertext_blocks:
        if previous_block == '':
            previous_block = ciphertext_blocks[0]  # IV
        else:
            previous_block = ciphertext_blocks[index - 1]

        input_block = ciphertext_block
        output_block = _block_decrypt(input_block, rounds, round_keyset)
        plaintext_block = _subtract_blocks_mod64(output_block, previous_block, seq_encoder, seq_decoder)
        plaintext_blocks.append(plaintext_block)
        index += 1

    # Adjust assembled plaintext for IV and padding
    assembled_plaintext = remove_block_padding(''.join(plaintext_blocks[1:]), source_key)

    return assembled_plaintext


def _decrypt_mode_ctr(ciphertext_blocks: list, rounds: int, round_keyset: list) -> str:
    """
    This function decrypts a list of ciphertext block strings using CTR mode over a number of rounds using a
    given set of round keys and extracting an initialization vector from the first block.

    :param ciphertext_blocks:   a list of block strings
    :param rounds:              an integer number of iterations for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :return:                    an assembled ciphertext string
    """
    source_key = keygen.use_quadress_layout(''.join(round_keyset[0][0]))
    seq_encoder = round_keyset[0][2]
    seq_decoder = round_keyset[0][3]
    period = len(ciphertext_blocks[0])
    plaintext_blocks = list()
    counter = 0

    for ciphertext_block in ciphertext_blocks:
        if len(ciphertext_blocks) > (10 ** (period / 2)) - 1:  # watch for rollover
            sys.exit('Counter mode roll over warning. A larger block size is required for this message.')
        if counter + 1 < len(ciphertext_blocks):
            # input_block = iv[:-len(str(counter))] + str(counter)  # dynamically grow for counter; watch rollover
            # input block is a random nonce on left concatenated with counter on right
            input_block = ciphertext_blocks[0][:int(math.ceil(period / 2))] + str(counter).zfill(
                int(math.floor(period / 2)))  # nonce size rounded up per NIST 800-38a

            output_block = _block_encrypt(input_block, rounds, round_keyset)  # notice encrypt for CTR decryption
            plaintext_block = _subtract_blocks_mod64(ciphertext_blocks[counter + 1],
                                                     output_block, seq_encoder, seq_decoder)
            plaintext_blocks.append(plaintext_block)
            counter += 1

    # Adjust assembled plaintext for IV and padding
    assembled_plaintext = remove_block_padding(''.join(plaintext_blocks), source_key)

    return assembled_plaintext


def _decrypt_mode_ecb(ciphertext_blocks: list, rounds: int, round_keyset: list) -> str:
    """
    This function decrypts a list of ciphertext block strings using ECB mode over a number of rounds using a
    given set of round keys; note that there is no initialization vector for ECB mode.

    :param ciphertext_blocks:   a list of block strings
    :param rounds:              an integer number of iterations for the block algorithm
    :param round_keyset:        a set of round keys derived from the key schedule
    :return:                    an assembled ciphertext string
    """
    source_key = keygen.use_quadress_layout(''.join(round_keyset[0][0]))
    plaintext_blocks = list()

    # Electronic Code Book (ECB) Mode - preserved to maintain compatibility as field cipher
    # NOT semantically secure beyond one block with same key; use unique keys for each block
    for ciphertext_block in ciphertext_blocks:
        input_block = ciphertext_block
        output_block = _block_decrypt(input_block, rounds, round_keyset)
        plaintext_blocks.append(output_block)

    # Adjust assembled plaintext padding
    assembled_plaintext = remove_block_padding(''.join(plaintext_blocks), source_key)

    return assembled_plaintext


def _block_decrypt(current_block: str, rounds: int, round_keys: list) -> str:
    """
    This is the eponymous round function for decryption that includes the fundamental
    fractionated substitution and columnar transposition steps of the Hexafid cipher.

    :param current_block:   the ciphertext block string under encryption
    :param rounds:          the number of round iterations for the algorithm
    :param round_keys:      a list of the round keys for each round
    :return:                the plaintext block string after encryption
    """
    for r in range(rounds):

        # # Subtract round key
        # round_key_block = ''.join(round_keys[rounds - 1 - r][2])
        # current_block = _subtract_blocks_mod64(
        #     current_block, round_key_block, round_keys[rounds - 1 - r][2], round_keys[rounds - 1 - r][3])

        # Binary substitution step
        substituted_bitslist = _get_quadress_values(current_block, round_keys[rounds - 1 - r][0])
        substituted_bitstring = ''.join(substituted_bitslist)

        # Columnar transposition step
        transposed_bitslist = [substituted_bitstring[
                               j::len(substituted_bitslist)] for j in range(len(substituted_bitslist))]

        # Turn back into character string
        transposed_charlist = _get_quadress_chars(transposed_bitslist, round_keys[rounds - 1 - r][1])
        current_block = ''.join(transposed_charlist)

    return current_block


def key_is_valid(key: str) -> bool:
    """
    This function checks to see if the key is a permutation of Base64 character set.

    :param key:         the source key represented as a string
    :return:            true if key is valid; false otherwise
    """
    key_list = list(key)
    symbol_list = list(SYMBOLS)
    key_list.sort()
    symbol_list.sort()

    return key_list == symbol_list


def iv_is_valid(iv: str, period: int) -> bool:
    """
    This function checks to see if the initialization vector matches the period length
    and only contains allowed characters (i.e. from the Base64 character set).

    :param iv:              the initialization vector as a string
    :param period:          the period, or block size, as an integer
    :return:                true if the iv is valid; false otherwise
    """
    if len(iv) != period:
        return False

    for c in iv:
        if c not in SYMBOLS:
            return False

    return True


def ciphertext_is_valid(message: str, period: int) -> bool:
    """
    This functions checks to make sure that a ciphertext has sufficient length and structure to (a) have an
    embedded IV, (b) be formed with correct Base64 length, and (c) be formed with correct length for block padding

    :param message:     a string of the ciphertext message
    :param period:      an integer specifying the period length
    :return:            a boolean - True if valid, False otherwise
    """

    # too short to contain embedded IV
    if len(message) <= period:
        return False

    # incorrect Base64 padding
    if len(message) % 4 != 0:
        return False
    else:  # len(message) % 4 == 0: # valid Base64 length
        # after stripping Base64 padding, message not multiple of block size
        if len(message.replace('=', '')) % period != 0:
            return False

    return True


def _sbox_encoders(encoder: dict, decoder: dict) -> (dict, dict):
    """
    This function substitutes key values for s-box values, effectively shuffling the key in an almost
    perfect non-linear (APN) manner. The 6-bit s-box is from FIDES (https://eprint.iacr.org/2015/424.pdf).

    :param encoder:         the current key represented as a sequence encoder dictionary
    :param decoder:         the current key represented as a sequence decoder dictionary
    :return:                the shuffled key as new sequence encode and decoder pair
    """
    sbox = [54, 0, 48, 13, 15, 18, 35, 53, 63, 25, 45, 52, 3, 20, 33, 41,
            8, 10, 57, 37, 59, 36, 34, 2, 26, 50, 58, 24, 60, 19, 14, 42,
            46, 61, 5, 49, 31, 11, 28, 4, 12, 30, 55, 22, 9, 6, 32, 23,
            27, 39, 21, 17, 16, 29, 62, 1, 40, 47, 51, 56, 7, 43, 38, 44]

    # extract values from dicts
    encoder_list = list(encoder)
    decoder_list = list(decoder)

    # substitute key values for s-box values
    sboxed_encoder_list = [encoder_list[c] for c in [sbox[i] for i in range(64)]]
    sboxed_decoder_list = [decoder_list[q] for q in [sbox[i] for i in range(64)]]

    # replace key values into dictionaries
    sboxed_encoder = dict(zip(sboxed_encoder_list, sboxed_decoder_list))
    sboxed_decoder = dict(zip(sboxed_decoder_list, sboxed_encoder_list))

    return sboxed_encoder, sboxed_decoder


def _get_matrix(flat_list: list, n: int) -> list:
    """
    This functions transforms a list into a list of lists (i.e. matrix) of size n X n.

    :param flat_list:      a list to be transformed into a 2-dimensional matrix
    :param n:           a size to establish the rows and columns
    :return:            a list of lists representing an n X n matrix
    """
    matrix = []
    for i in range(0, len(flat_list), n):
        matrix.append(flat_list[i:i + n])

    return matrix


def _rotate_encoders(encoder: dict, decoder: dict) -> (dict, dict):
    """
    This function rotates the keysquare matrix 90 degrees clockwise around it's centre axis.

    :param encoder:         the current key represented as a quadress encoder dictionary
    :param decoder:         the current key represented as a quadress decoder dictionary
    :return:                the rotated key as a pair of encoder/decoder dictionaries
    """
    # extract keys from dictionary into list of lists (i.e. matrix)
    encoder_matrix = _get_matrix(list(encoder.keys()), 8)
    decoder_matrix = _get_matrix(list(decoder.keys()), 8)

    # rotate matrix by 90 degrees
    rotated_encoder_matrix = list(zip(*encoder_matrix[::-1]))
    rotated_decoder_matrix = list(zip(*decoder_matrix[::-1]))
    rem = list(sum(rotated_encoder_matrix, ()))
    rdm = sorted(list(sum(rotated_decoder_matrix, ())))

    # replace keys into dictionaries
    rotated_encoder = dict(zip(rem, rdm))
    rotated_decoder = dict(zip(rdm, rem))

    return rotated_encoder, rotated_decoder


def setup_quadtree_addresses(key: str) -> (dict, dict):
    """
    This function produces the quadtree encoding and decoding dictionaries from the key.

    :param key:         a string permutation of the Base64 character set
    :return:            a pair of quadtree encoder and decoder dicts in the form
                        of {'M': '000000',...} and {'000000': 'M',...}
    """
    key = keygen.use_sequence_layout(key)
    quads = ['00', '01', '10', '11']
    decode_dict = {}
    encode_dict = {}
    index = 0

    for top in quads:
        for middle in quads:
            for bottom in quads:
                address = top + middle + bottom
                decode_dict[address] = key[index]
                encode_dict[key[index]] = address
                index = index + 1

    return encode_dict, decode_dict


def setup_sequence_addresses(key: str) -> (dict, dict):
    """
    This function produces the sequence encoding and decoding dictionaries from the key.

    :param key:         a string permutation of the Base64 character set
    :return:            a pair of sequence encoder and decoder dicts in the form
                        of {'M': 1,...} and {1: 'M',...}
    """
#    key = keygen.use_sequence_layout(key)  # TODO Make all key generation naturally human

    decode_dict = {}
    encode_dict = {}

    for i in range(1, 65):
        decode_dict[i] = key[i - 1]
        encode_dict[key[i - 1]] = i

    return encode_dict, decode_dict


def _get_sequence_values(block_chars: str, seq_encoder: dict) -> list:
    """
    This function substitutes each block string character with its corresponding sequence address in the keysquare.

    :param block_chars:         a block string of characters
    :param seq_encoder:         the key as a sequence of values in an encoder dictionary
    :return:                    a list of sequence values in a block
    """
    substituted_values = list()
    for c in block_chars:
        substituted_values.append(seq_encoder[c])

    return substituted_values


def _get_sequence_chars(values_list: list, seq_decoder: dict) -> list:
    """
    This function substitutes each sequence address in a list with its corresponding character in the keysquare.

    :param values_list:         a list of sequence values in a block
    :param seq_decoder:         the key as a sequence of values in a decoder dictionary
    :return:                    a list of block characters
    """
    substituted_chars = list()
    for v in values_list:
        if v == 0:  # addresses 64 % 64 = 0 cycling back to 64 in alignment with end user sequence
            substituted_chars.append(seq_decoder[64])
        else:
            substituted_chars.append(seq_decoder[v])

    return substituted_chars


def _get_quadress_values(block_chars: str, quad_encoder: dict) -> list:
    """
    This function substitutes each block string character with its corresponding quadress in the keysquare.

    :param block_chars:             a block string of characters
    :param quad_encoder:            the key as a quadress encoder dictionary
    :return:                        a list of quadress values in a block
    """
    substituted_values = list()
    for c in block_chars:
        substituted_values.append(quad_encoder[c])

    return substituted_values


def _get_quadress_chars(values_list: list, quad_decoder: dict) -> list:
    """
    This function substitutes each quadress in a list with its corresponding character in the keysquare.

    :param values_list:             a list of quadress values in a block
    :param quad_decoder:            the key as a quadress decoder dictionary
    :return:                        a list of block characters
    """
    substituted_chars = list()
    for v in values_list:
        substituted_chars.append(quad_decoder[v])

    return substituted_chars


def prepare_message(message_string: str, separator: bool) -> str:
    """
    This function replaces whitespace in the message if separator is True and it also removes any characters
    not found within the Base64 character set.

    :param message_string:          the message string intended for enciphering
    :param separator:               a flag - True to include a separator replacing whitespace
    :return:                        the clean message string excluding non-Base64 characters
    """
    if separator:
        # add separator for readability at the cost of cryptanalytic resistance
        message = '/'.join(message_string.split())
        # .replace('.','+').replace('-','+')
    else:
        message = ''.join(message_string.split())

    # remove non-base64 characters
    plaintext_string = re.sub(r'[^A-Za-z0-9+/]+', '', message)

    return plaintext_string


def _separate_cipher_blocks(full_string: str, period: int) -> list:
    """
    This function separates the ciphertext into a list of period-sized block strings.

    :param full_string:         the full ciphertext string before separation into blocks
    :param period:              the period determining the length of each block
    :return:                    a list of ciphertext block strings
    """
    block_list = [full_string[i:i + period] for i in range(0, len(full_string), period)]

    return block_list


def _separate_plain_blocks(full_string: str, period: int, key: str, mode: str) -> list:
    """
    This function separates the plaintext into a list of period-sized block strings.

    :param full_string:         the full plaintext string before separation into blocks
    :param period:              the period determining the length of each block
    :param key:                 a string permutation of the Base64 character set
    :param mode:                a code for the block cipher mode of operation
    :return:                    a list of plaintext block strings
    """
    padded_string = add_block_padding(full_string, period, key, mode)
    block_list = [padded_string[i:i + period] for i in range(0, len(padded_string), period)]

    return block_list


def add_block_padding(full_string: str, period: int, key: str, mode: str) -> str:
    """
    This function adds padding to the plaintext sufficient to satisfy the immediate demands of
    PKCS#7 padding in addition to the later demands of obtaining a valid Base64 length for the Hexafid cipher.

    :param full_string:         the full plaintext string before separation into blocks
    :param period:              the period determining the length of each block
    :param key:                 a string permutation of the Base64 character set
    :param mode:                a code for the block cipher mode of operation
    :return:                    the block-padded plaintext string
    """
    # There is a slight performance hit with reconstructing dict as opposed to passing it in,
    # but for the gain of interoperability with external modules
    seq_encoder, seq_decoder = setup_sequence_addresses(key)

    if mode == 'CBC' or mode == 'CTR':
        iv_length = period
    else:
        iv_length = 0

    pad_length = (period - len(full_string)) % period
    if pad_length == 0:
        pad_length = period

    # check for lengths not equal to period or not legal for Base 64
    while (iv_length + len(full_string) + pad_length) % period != 0 or \
            (iv_length + len(full_string) + pad_length) % 4 == 1:
        pad_length += 1

    pad_char = seq_decoder[pad_length]
    padding = pad_char * pad_length

    return full_string + padding


def remove_block_padding(plaintext: str, key: str) -> str:
    """
    This function removes block padding in a manner similar to that specified in PKCS#7. The last character
    of the plaintext string specifies how many characters to remove as padding.

    :param plaintext:       the string from which to remove padding
    :param key:             a string permutation of the Base64 character
                            that enables sequence lookup of the last character
    :return:                the trimmed plaintext without PKCS#7 padding
    """
    # There is slight performance hit here with reconstructing the dicts as opposed to passing it in,
    # but for the gain of interoperability with external modules that use this function.
    seq_encoder, seq_decoder = setup_sequence_addresses(key)

    pad_length = seq_encoder[plaintext[-1]]

    # # WARNING - potential padding oracle commented out; allowing incorrect trimming of bad pad - but no oracle
    # if plaintext[-pad_length:] != plaintext[-1] * pad_length:
    #     sys.exit("There is an error in the ciphertext.")  # Incorrect block padding

    trimmed_plaintext = plaintext[:(len(plaintext) - pad_length)]

    return trimmed_plaintext


def add_b64_padding(message: str) -> str:
    """
    This function adds Base64 padding to a message.

    :param message:     the message for padding
    :return:            the message with Base64 padding
    """

    if len(message) % 4 == 1:  # Technically this should never occur (RFC 4648); thus, pre-pad block
        message_padded = message + '==='
    elif len(message) % 4 == 2:
        message_padded = message + '=='
    elif len(message) % 4 == 3:
        message_padded = message + '='
    else:
        message_padded = message

    return message_padded


def remove_b64_padding(message: str) -> str:
    """
    This function removes Base64 padding from a message.

    :param message:     the message with Base64 padding
    :return:            the message without padding
    """
    return str.replace(message, '=', '')


# If run instead of called
if __name__ == '__main__':
    main()
