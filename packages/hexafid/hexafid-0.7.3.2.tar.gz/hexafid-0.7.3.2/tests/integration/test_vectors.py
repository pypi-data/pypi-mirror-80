# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import unittest
import base64

# Third party imports
# Local application imports

import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen


class TestSpecificVectors(unittest.TestCase):
    maxDiff = None

    def test_encrypt(self):
        self.assertEqual(
            hexafid.encrypt(
                'It is not the critic who counts; not the man who points out how the strong man '
                'stumbles, or where the doer of deeds could have done them better. The credit '
                'belongs to the man who is actually in the arena, whose face is marred by dust and '
                'sweat and blood; who strives valiantly; who errs, who comes short again and '
                'again, because there is no effort without error and shortcoming; but who does '
                'actually strive to do the deeds; who knows great enthusiasms, the great '
                'devotions; who spends himself in a worthy cause; who at the best knows in the end '
                'the triumph of high achievement, and who at the worst, if he fails, '
                'at least fails while daring greatly, so that his place shall never be with those '
                'cold and timid souls who neither know victory nor defeat. -Theodore Roosevelt',
                keygen.use_quadress_layout('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'),
                'ECB', '31337', 5, 1, separator=False, preserve=False),
            'eDSyp8HrQufDUmqdmcQE+Db2G+B1oXXWmvC+BwA0+B/Y4+KsQZuh7kz8GKlo+B350XS7qY6qYp1ZPe5Nsn6WlD7'
            '/2SdHtyDot53V2SzmLTa+/FqrmHXJv+7FyZy7N+Ca0J6LSxsfSKMKyZ66BunFsm8ErcuVXpvq9E4woD71tw2S+HjF'
            '/ubN6L3ZlZfehwovdm36N0gS+B5gz2R7+pbKSbp+aGCZuj6XG7I4gIuh3sB6LxFMbKRflLrUFwg99u42T3qDXTtfIwd97z+LhEs'
            '+C8xZfD8OtXSzsN6L5kM8ENOl+TOIKVX9iwbL3TJ+g9kz2R7uKdHtQ2D7/2S/Agwp+ipAhLr19l+C1i4fDb6BslaVyTb75t+DSSp'
            '+icQEqrb2W8EZ2wslOn6/BwiHnx67AdmcIk4Peh9fDn4l+ihRhya1z5bLexd+CpvR2RhC2yYwiJqpz/kbK3dtdmcA06PWhc'
            '+DxkqRe9r66I7ZJmx+2RPjM+S9EIyqPjkX14M4jk+SeiY2S0ib8FqomNnvEi6Ifz9Tf0vM+BSoPyb7iAk1uzb8GNXR'
            '+DtyC9Eoxq6Japt+IuUpuh7Il9E6dLD7/fJVU5aZybpGK0X7ziwBHwY=',
        )

    def test_decrypt(self):
        self.assertEqual(
            hexafid.decrypt(
                'eDSyp8HrQufDUmqdmcQE+Db2G+B1oXXWmvC+BwA0+B/Y4+KsQZuh7kz8GKlo+B350XS7qY6qYp1ZPe5Nsn6WlD7'
                '/2SdHtyDot53V2SzmLTa+/FqrmHXJv+7FyZy7N+Ca0J6LSxsfSKMKyZ66BunFsm8ErcuVXpvq9E4woD71tw2S+HjF'
                '/ubN6L3ZlZfehwovdm36N0gS+B5gz2R7+pbKSbp+aGCZuj6XG7I4gIuh3sB6LxFMbKRflLrUFwg99u42T3qDXTtfIwd97z'
                '+LhEs+C8xZfD8OtXSzsN6L5kM8ENOl+TOIKVX9iwbL3TJ+g9kz2R7uKdHtQ2D7/2S/Agwp+ipAhLr19l'
                '+C1i4fDb6BslaVyTb75t+DSSp+icQEqrb2W8EZ2wslOn6/BwiHnx67AdmcIk4Peh9fDn4l+ihRhya1z5bLexd'
                '+CpvR2RhC2yYwiJqpz/kbK3dtdmcA06PWhc+DxkqRe9r66I7ZJmx+2RPjM+S9EIyqPjkX14M4jk'
                '+SeiY2S0ib8FqomNnvEi6Ifz9Tf0vM+BSoPyb7iAk1uzb8GNXR+DtyC9Eoxq6Japt+IuUpuh7Il9E6dLD7'
                '/fJVU5aZybpGK0X7ziwBHwY=',
                keygen.use_quadress_layout('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'),
                'ECB', 5, 1, separator=False, preserve=False),
            hexafid.prepare_message(
                'It is not the critic who counts; not the man who points out how the strong man '
                'stumbles, or where the doer of deeds could have done them better. The credit '
                'belongs to the man who is actually in the arena, whose face is marred by dust and '
                'sweat and blood; who strives valiantly; who errs, who comes short again and '
                'again, because there is no effort without error and shortcoming; but who does '
                'actually strive to do the deeds; who knows great enthusiasms, the great '
                'devotions; who spends himself in a worthy cause; who at the best knows in the end '
                'the triumph of high achievement, and who at the worst, if he fails, '
                'at least fails while daring greatly, so that his place shall never be with those '
                'cold and timid souls who neither know victory nor defeat. -Theodore Roosevelt', separator=False)
        )

    def test_encrypt_with_separator(self):
        self.assertEqual(
            hexafid.encrypt(
                'Attack at dawn',
                keygen.use_quadress_layout('dBCDEUGxIQKLMNOjJRSTFAWXnZmbctefghkp2laYoPqrsu9VvyHz13i045678w+/'),
                'ECB', '31337', 5, 1, separator=True, preserve=False),
            'U3Vyc6ub+rnnzEE='  # was U3Vyc6ub+rnzZC==
        )

    def test_decrypt_with_separator(self):
        self.assertEqual(
            hexafid.decrypt(
                'U3Vyc6ub+rnnzEE=',
                keygen.use_quadress_layout('dBCDEUGxIQKLMNOjJRSTFAWXnZmbctefghkp2laYoPqrsu9VvyHz13i045678w+/'),
                'ECB', 5, 1, separator=True, preserve=False),
            'Attack/at/dawn'
        )


class TestHumanFieldUse(unittest.TestCase):

    def test_human_encrypt(self):
        message = 'Hello World'
        key = 'MyPasword123ABCDEFGHIJKLNOQRSTUVWXYZbcefghijklmnpqtuvxz0456789+/'
        mode = 'ECB'
        iv = '31337'
        period = 5
        rounds = 1
        self.assertEqual(
            hexafid.encrypt(message, key, mode, iv, period, rounds, separator=False, preserve=False),
            'I31AsfWdyfypMMM='  # Now with padding; was 'I31AsfWdyf==' by hand without padding
        )

    def test_human_decrypt(self):
        message = 'I31AsfWdyfypMMM='  # Now with padding; was 'I31AsfWdyf==' by hand without padding
        key = 'MyPasword123ABCDEFGHIJKLNOQRSTUVWXYZbcefghijklmnpqtuvxz0456789+/'
        mode = 'ECB'
        period = 5
        rounds = 1
        self.assertEqual(
            hexafid.decrypt(message, key, mode, period, rounds, separator=False, preserve=False),
            'HelloWorld'
        )


class TestSteganography(unittest.TestCase):
    # Plaintext: Attack/At/Dawn and
    # Stegatext: Hold/Forces (Hold Forces) and
    # Ciphertext/Base64: SG9sZC9Gb3JjZXM= (SG9sZCBGb3JjZXM=)
    def test_encrypt(self):
        message = 'Attack at dawn'
        key = keygen.use_quadress_layout('dBCDEUGxIQKLMNOjJRSTFAWXnZmbctefghkp2laYoPqrsu9VvyHz13i045678w+/')
        mode = 'ECB'
        iv = '31337'
        period = 5
        rounds = 1
        self.assertEqual(
            hexafid.encrypt(message, key, mode, iv, period, rounds, separator=False, preserve=False),
            'U3VycHJpc2hpUvJ='  # now fixed but PKCS#7 pads last block; was 'U3VycHJpc2Vk' by hand
        )

    def test_decrypt(self):
        message = 'U3VycHJpc2hpUvJ='
        key = keygen.use_quadress_layout('dBCDEUGxIQKLMNOjJRSTFAWXnZmbctefghkp2laYoPqrsu9VvyHz13i045678w+/')
        mode = 'ECB'
        period = 5
        rounds = 1
        self.assertEqual(
            hexafid.decrypt(message, key, mode, period, rounds, separator=False, preserve=False),
            'Attackatdawn'
        )

    def test_decode(self):
        self.assertEqual(
            base64.b64decode('U3VycHJpc2Vk'),  # needs updating with PKCS#7 padding; was 'U3VycHJpc2Vk' by hand
            b'Surprised'
        )


if __name__ == '__main__':
    unittest.main()
