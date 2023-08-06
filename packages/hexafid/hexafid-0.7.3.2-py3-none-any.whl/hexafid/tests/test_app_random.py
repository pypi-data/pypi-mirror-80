# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import string
import random
import time
import sys
import os

# Third party imports
# Local application imports
# hack to import module for iOS/Pythonista/ExternalFiles/WorkingCopy
module_path = os.path.join(os.path.dirname(sys.path[0]), 'hexafid')
sys.path.append(module_path)

import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen


def main():
    tic = time.perf_counter()
    random_tests()
    toc = time.perf_counter()
    print('All in %s seconds' % (toc - tic))


def random_tests():
    random.seed(42)  # static seed
    mode_list = ['ECB', 'CBC', 'CTR']
    key_list = []
    counter = 0

    # build random key list
    for i in range(1):
        key_list.append(keygen.get_random_key())

    # tests random messages in stated range
    for i in range(3):

        # build random message of printable ASCII
        message = ''.join(random.SystemRandom().choice(string.printable) for m in range(1024))

        # tests keys from key list
        for key in key_list:

            # tests each available block cipher mode
            for mode in mode_list:

                # tests period (block size = period * 6 bits) in stated range
                for period in range(8, 17):  # multiples of key size

                    # clean message
                    plaintext = hexafid.add_block_padding(hexafid.prepare_message(message, separator=False),
                                                          period, key, mode)

                    # # dirty message
                    # plaintext = message

                    # Select random IV
                    iv = keygen.get_iv(period)

                    # tests block cipher rounds in stated range
                    for rounds in range(8, 17):

                        encrypted = hexafid.encrypt(plaintext, key, mode, iv, period, rounds)
                        decrypted = hexafid.decrypt(encrypted, key, mode, period, rounds)

                        print(
                            'Test #%s:\n'
                            'Cipher: Hexafid\n'
                            'Message: %s...\n'
                            'Cleaned: %s...\n'
                            'Key: %s...\n'
                            'Mode: %s\n'
                            'IV: %s\n'
                            'Period: %s\n'
                            'Rounds: %s\n'
                            % (counter + 1, message[:20], plaintext[:20], key[:20], mode, iv, period, rounds))
                        counter += 1

                        # throw error is no match
                        if plaintext != decrypted:
                            print('Mismatch with... \nKEY: %s \nPERIOD: %s \nMESSAGE: %s' % (key, period, plaintext))
                            print('DECRYPT: ' + decrypted)
                            sys.exit()

    print('Hexafid random tests passed')


if __name__ == '__main__':
    main()
