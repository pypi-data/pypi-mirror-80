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
import hexafid.hexafid_keygen as keygen
import hexafid.hexafid_utilities as utilities


def main():
    encrypt = True  # encrypt or decrypt
    input_filename = './data/frankenstein.txt'
    output_hex_filename = './data/frankenstein.hex'
    output_bin_filename = './data/frankenstein.bin'
    # output_hex_filename = './data/frankenstein_' + \
    #                       my_mode + '_' + 'P' + str(my_period) + 'R' + str(my_rounds) + '.hex'
    # output_bin_filename = './data/frankenstein_' + \
    #                       my_mode + '_' + 'P' + str(my_period) + 'R' + str(my_rounds) + '.bin'
    my_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    # my_key = keygen.get_random_key()
    my_mode = 'CBC'
    my_period = 20  # 16
    my_rounds = 20  # 16
    my_iv = keygen.get_iv(my_period)
    binary_content = ''

    # check for no input file
    if not os.path.exists(input_filename):
        print('The file %s does not exist. Quitting...' % input_filename)
        sys.exit()

    # check for overwrite
    if os.path.exists(output_hex_filename):
        print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % output_hex_filename)
        response = input('> ')
        if not response.lower().startswith('c'):
            sys.exit()

    # read message from file utf8
    input_file = io.open(input_filename, mode="r", encoding="utf-8")
    content = input_file.read()
    input_file.close()

    # measure time of process
    start_time = time.time()
    if encrypt:
        print('Encrypting...')
        translated = hexafid.encrypt(content, my_key, my_mode, my_iv, my_period, my_rounds)
        print('Encryption complete.')
        binary_content = utilities.hex2bin(translated, my_key, my_rounds)

    else:
        print('Decrypting...')
        translated = hexafid.decrypt(content, my_key, my_mode, my_period, my_rounds)
        print('Decryption complete.')

    total_time = round(time.time() - start_time, 2)
    print('Processing time: %s seconds' % total_time)

    # write translated message to file
    output_file = io.open(output_hex_filename, 'w', encoding="utf-8")
    output_file.write(translated)
    output_file.close()

    if binary_content not in '':
        output_file = io.open(output_bin_filename, 'w', encoding="utf-8")
        output_file.write(binary_content)
        output_file.close()

    print('Done processing %s (%s characters).' % (input_filename, len(content)))
    print('Output file is %s.' % output_hex_filename)
    print('Shannon\'s entropy: %s' % entropy.shannon(translated))

    if content == hexafid.decrypt(translated, my_key, my_mode, my_period, my_rounds):
        print('Bijective test passed.')
    else:
        print('Bijective test failed.')


# if run instead of called as module
if __name__ == '__main__':
    main()
