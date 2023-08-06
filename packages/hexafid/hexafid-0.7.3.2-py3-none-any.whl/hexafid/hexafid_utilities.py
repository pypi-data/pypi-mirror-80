# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import os
import sys
import io
import time
# Third party imports
# Local application imports
import hexafid.hexafid_analysis as entropy
import hexafid.hexafid_core as hexafid

# import hexafid.hexafid_keygen as keygen

binary = True


def main():
    input_filename = './data/frankenstein_CTR_81.hex'
    output_filename = input_filename + '.bin'
    my_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    rounds = 16  # for testing purposes; should be dynamic

    # check for no input file
    if not os.path.exists(input_filename):
        print('The file %s does not exist. Quitting...' % input_filename)
        sys.exit()

    # check for overwrite
    if os.path.exists(output_filename):
        print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % output_filename)
        response = input('> ')
        if not response.lower().startswith('c'):
            sys.exit()

    # read message from file utf8
    input_file = io.open(input_filename, mode="r", encoding="utf-8")
    content = input_file.read()
    input_file.close()

    # measure time of process
    start_time = time.time()
    if binary:
        print('Transforming Hexafid file to binary file...')
        translated = hex2bin(content, my_key, rounds)
        print('Transformation complete.')

    else:
        print('Transforming binary file to Hexafid file...')
        translated = bin2hex(content, my_key, rounds)
        print('Transformation complete.')

    total_time = round(time.time() - start_time, 2)
    print('Processing time: %s seconds' % total_time)

    # write translated message to file
    output_file = io.open(output_filename, 'w', encoding="utf-8")
    output_file.write(translated)
    output_file.close()

    print('Done processing %s (%s characters).' % (input_filename, len(content)))
    print('Output file is %s.' % output_filename)
    print('Shannon\'s entropy: %s' % entropy.shannon(translated))


def hex2bin(content, key, rounds):
    """Return stream of bits from stream of hex."""
    key = get_last_round_key(key, rounds)
    quad_encoder, quad_decoder = hexafid.setup_quadtree_addresses(key)

    bitstring = content.translate(str.maketrans(quad_encoder))

    return bitstring


def bin2hex(content, key, rounds):
    """Return stream of hex from stream of bits."""
    key = get_last_round_key(key, rounds)
    quad_encoder, quad_decoder = hexafid.setup_quadtree_addresses(key)

    hexstring = content.translate(str.maketrans(quad_decoder))

    return hexstring


def get_last_round_key(key, rounds):
    """Return the last round key used in an encryption/decryption."""
    quad_encoder, quad_decoder = hexafid.setup_quadtree_addresses(key)
    seq_encoder, seq_decoder = hexafid.setup_sequence_addresses(key)

    # setup round keys for key schedule
    round_keyset = list()
    magic_number = 42  # nothing up my sleeves number to initialize key schedule
    round_keyset.append((quad_encoder, quad_decoder, seq_encoder, seq_decoder, magic_number))
    for r in range(rounds - 1):
        round_keyset.append(hexafid.get_round_keys(round_keyset[r][0], round_keyset[r][1],
                                                   round_keyset[r][2], round_keyset[r][3], round_keyset[r][4]))

    return ''.join(str(x) for x in round_keyset[rounds - 1][1].values())


# If run instead of called
if __name__ == '__main__':
    main()
