# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import time
import sys
import os

# Third party imports
# Local application imports
# hack to import module for iOS/Pythonista/ExternalFiles/WorkingCopy
module_path = os.path.join(os.path.dirname(sys.path[0]), 'hexafid')
sys.path.append(module_path)

import hexafid.hexafid_core as hexafid


def main():
    tic = time.perf_counter()
    specific_tests()
    toc = time.perf_counter()
    print('All in %s seconds' % (toc - tic))


def specific_tests():
    counter = 0

    # test_list [(key, period, plaintext, ciphertext)]
    test_list = [
        ('It is not the critic who counts; not the man who points out how the strong man stumbles, or where '
         'the doer of deeds could have done them better. The credit belongs to the man who is actually in the '
         'arena, whose face is marred by dust and sweat and blood; who strives valiantly; who errs, who comes '
         'short again and again, because there is no effort without error and shortcoming; but who does '
         'actually strive to do the deeds; who knows great enthusiasms, the great devotions; who spends '
         'himself in a worthy cause; who at the best knows in the end the triumph of high achievement, '
         'and who at the worst, if he fails, at least fails while daring greatly, so that his place shall '
         'never be with those cold and timid souls who neither know victory nor defeat. -Theodore Roosevelt',
         'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', 'ECB', 'khuf7', 5, 1,
         'eDSyp8HrQufDUmqdmcQE+Db2G+B1oXXWmvC+BwA0+B/Y4+KsQZuh7kz8GKlo+B350XS7qY6qYp1ZPe5Nsn6WlD7'
         '/2SdHtyDot53V2SzmLTa+/FqrmHXJv+7FyZy7N+Ca0J6LSxsfSKMKyZ66BunFsm8ErcuVXpvq9E4woD71tw2S+HjF'
         '/ubN6L3ZlZfehwovdm36N0gS+B5gz2R7+pbKSbp+aGCZuj6XG7I4gIuh3sB6LxFMbKRflLrUFwg99u42T3qDXTtfIwd97z+LhEs'
         '+C8xZfD8OtXSzsN6L5kM8ENOl+TOIKVX9iwbL3TJ+g9kz2R7uKdHtQ2D7/2S/Agwp+ipAhLr19l+C1i4fDb6BslaVyTb75t+DSSp'
         '+icQEqrb2W8EZ2wslOn6/BwiHnx67AdmcIk4Peh9fDn4l+ihRhya1z5bLexd+CpvR2RhC2yYwiJqpz/kbK3dtdmcA06PWhc'
         '+DxkqRe9r66I7ZJmx+2RPjM+S9EIyqPjkX14M4jk+SeiY2S0ib8FqomNnvEi6Ifz9Tf0vM+BSoPyb7iAk1uzb8GNXR+DtyC9Eoxq6Japt'
         '+IuUpuh7Il9E6dLD7/fJVU5aZybpGK0X7zixz'),
        ('Attack at dawn',
         'dBCDEUGxIQKLMNOjJRSTFAWXnZmbctefghkp2laYoPqrsu9VvyHz13i045678w+/', 'ECB', 'khuf7', 5, 1,
         'U3VycHJpc2Vk')
    ]

    for test in test_list:
        message = test[0]
        key = test[1]
        mode = test[2]
        iv = test[3]
        period = test[4]
        rounds = test[5]
        # ciphertext = test[6]

        if not hexafid.key_is_valid(key):
            sys.exit('There is an error in the key or symbol set.')

        plaintext = hexafid.add_block_padding(hexafid.prepare_message(message, separator=False), period, key, mode)

        encrypted = hexafid.encrypt(plaintext, key, mode, iv, period, rounds)
        decrypted = hexafid.decrypt(encrypted, key, mode, period, rounds)

        print(
            'Test #%s:\n'
            'Cipher: Hexafid\n'
            'Mode: %s\n'
            'Message: %s...\n'
            'Clean: %s...\n'
            'Key: %s...\n'
            'IV: %s\n'
            'Period: %s\n'
            'Rounds: %s\n'
            % (counter + 1, mode, message[:20], plaintext[:20], key[:20], iv, period, rounds))
        counter += 1

        # throw error is no match
        if plaintext != decrypted:
            print('Mismatch with... \nKEY: %s \nPERIOD: %s \nMESSAGE: %s' % (key, period, plaintext))
            print('DECRYPT: ' + decrypted)
            sys.exit()

    print('Hexafid specific tests passed')


if __name__ == '__main__':
    main()
