# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import unittest

# Third party imports
# Local application imports
import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen


class TestGlobalConstants(unittest.TestCase):

    def test_symbols(self):
        self.assertEqual(len(hexafid.SYMBOLS), 64)
        self.assertEqual(hexafid.SYMBOLS, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')

    def test_bits(self):
        self.assertEqual(hexafid.BITS, 6)


class TestKeyIsValid(unittest.TestCase):

    def test_key_match(self):
        self.assertEqual(hexafid.key_is_valid('password'), False, "Should match Base64 symbol set")


class TestCipherTextIsValid(unittest.TestCase):

    def test_bad_B64_padding_length(self):
        self.assertFalse(hexafid.ciphertext_is_valid('testy', 4),
                         "Wrong Base64 length; ciphertext should fail")

    def test_bad_ciphertext_iv_length(self):
        self.assertFalse(hexafid.ciphertext_is_valid('test', 6),
                         "Insufficient length for IV; ciphertext should fail")

    def test_bad_block_padding_length(self):
        self.assertFalse(hexafid.ciphertext_is_valid('tester', 4),
                         "Not a multiple of block length; ciphertext should fail")


class TestPadBlockMessage(unittest.TestCase):

    def test_pad_block_0(self):
        self.assertEqual(hexafid.add_block_padding('test', 9, hexafid.SYMBOLS, 'ECB'),
                         'testNNNNNNNNNNNNNN', "Should be testNNNNNNNNNNNNNN")  # testEEEEE

    def test_pad_block_1(self):
        self.assertEqual(hexafid.add_block_padding('test', 9, hexafid.SYMBOLS, 'CBC'),
                         'testEEEEE', "Should be testNNNNNNNNNNNNNN")  # testEEEEE


class TestPad64Message(unittest.TestCase):

    def test_pad_0(self):
        self.assertEqual(hexafid.add_b64_padding('test'), 'test', "Should be test")

    def test_pad_1(self):  # should never occur, see test_pad_b64_length
        self.assertEqual(hexafid.add_b64_padding('testy'), 'testy===', "Should be testy===")

    def test_pad_2(self):
        self.assertEqual(hexafid.add_b64_padding('tester'), 'tester==', "Should be tester==")

    def test_pad_3(self):
        self.assertEqual(hexafid.add_b64_padding('testing'), 'testing=', "Should be testing=")


class TestPrepareMessage(unittest.TestCase):

    def test_separator(self):
        self.assertEqual(hexafid.prepare_message('test this', separator=True),
                         'test/this', "Does not add correct separator")
        self.assertEqual(hexafid.prepare_message('test this', separator=False),
                         'testthis', "Words should not be separated")

    def test_remove_invalids(self):
        self.assertEqual(hexafid.prepare_message('test.this', separator=False),
                         'testthis', "Non Base64 chars should be removed")


class TestEncrypt(unittest.TestCase):

    def test_machine_encrypt(self):
        message = 'Hello World'
        key = 'MyPasword123ABCDEFGHIJKLNOQRSTUVWXYZbcefghijklmnpqtuvxz0456789+/'
        mode = 'ECB'
        period = 5
        rounds = 1
        iv = keygen.get_iv(period)
        self.assertEqual(
            hexafid.encrypt(message, key, mode, iv, period, rounds, separator=False, preserve=False),
            'I31AsfWdyfypMMM='  # without block padding 'I31AsfWdyf=='
        )


class TestDecrypt(unittest.TestCase):

    def test_machine_decrypt(self):
        message = 'I31AsfWdyfypMMM='  # without block padding 'I31AsfWdyf==
        key = 'MyPasword123ABCDEFGHIJKLNOQRSTUVWXYZbcefghijklmnpqtuvxz0456789+/'
        mode = 'ECB'
        period = 5
        rounds = 1
        self.assertEqual(
            hexafid.decrypt(message, key, mode, period, rounds, separator=False, preserve=False),
            'HelloWorld'
        )


class TestBijectiveness(unittest.TestCase):
    def test_round_trip(self):
        my_message = hexafid.prepare_message('Hello World!!!', separator=False)
        my_key = keygen.get_key_from_pass('MyPassword123', 'forward')
        my_mode = 'CBC'  # CBC or ECB
        my_period = 5
        my_iv = keygen.get_iv(my_period)  # 'kLi7d'  # for test only, use random IVs
        my_rounds = 32
        encrypted = hexafid.encrypt(my_message, my_key, my_mode, my_iv, my_period, my_rounds)
        decrypted = hexafid.decrypt(encrypted, my_key, my_mode, my_period, my_rounds)
        self.assertTrue(
            decrypted == my_message
        )
        return decrypted == my_message


if __name__ == '__main__':
    unittest.main()
