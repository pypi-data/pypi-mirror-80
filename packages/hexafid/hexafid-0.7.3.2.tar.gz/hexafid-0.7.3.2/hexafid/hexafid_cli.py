# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import logging as log
# Third party imports
import click
# Local application imports
import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen


@click.command()
@click.option(
    '--encrypt/--decrypt',
    type=bool,
    default=True,
    help='A flag to specify whether you want to encrypt or decrypt something. If not provided, the '
         'default is encrypt.'
)
@click.option(
    '--filein',
    type=click.File(mode='r', encoding='utf-8'),
    help='A file location containing text (encoded as utf-8) that you want to encrypt or decrypt. '
         'If not provided, you will be prompted to type some input text.'
)
@click.option(
    '--fileout',
    type=click.File(mode='w', encoding='utf-8'),
    help='A file location to which the encrypted or decrypted text will be written (encoded as utf-8). '
         'If not provided, your output text will be printed to screen.'
)
@click.option(
    '--key',
    type=str,
    default='',
    help='A secret string used for encryption or decryption. '
         'Valid keys are a permutation of the Base64 character set. '
         'You may also enter a password and a full key will be derived for you. '
         'If not provided, the default key is randomly generated.'
)
@click.option(
    '--mode',
    type=click.Choice(['CBC', 'CTR', 'ECB'], case_sensitive=False),
    default='CBC',
    help='A string representing the block cipher mode of operation. '
         'Valid options are CBC (Cipher Block Chaining), CTR (Counter), and ECB (Electronic Code Book). '
         'If not provided, the default mode is CBC.'
)
# @click.option(
#     '--iv',
#     type=str,
#     help='An initialization vector (IV) that provides unique material to initiate the cipher. '
#          'Valid IVs derive from the Base64 character set and match the period size in length. '
#          'The default option generates a random IV.'
# )
# @click.option(
#     '--period',
#     type=click.IntRange(min=8, max=32),
#     default=16,
#     help='A period defines the size of a character block within the algorithm. '
#          'Valid periods are integers 8-32; which correspond, internally, to block sizes of 48-196 Hexafid bits. '
#          'The default is 16 characters for the Hexafid Block Cipher.'
# )
# @click.option(
#     '--rounds',
#     type=click.IntRange(min=8, max=32),
#     default=16,
#     help='A round determines the number of time the block algorithm iterates. '
#          'Valid rounds are integers between 8 and 32. '
#          'The default is 16 rounds for the Hexafid Block Cipher.'
# )
# @click.option(
#     '--separator',
#     type=bool,
#     default=False,
#     help='Specify whether you want to include a word separator (/) for spaces in the plaintext. During non-format'
#          'preserving encryption with Hexafid, all characters not in the Base64 character set are removed - which '
#          'includes spaces and most punctuation. Adding a space separator preserves readability after this pre-'
#          'processing step. The default for separator is true.'
# )
# @click.option(
#     '--preserve',
#     type=bool,
#     default=True,
#     help='Specify whether you want to preserve plaintext formatting with pre/post Base64 en/decoding for '
#          'lossless encryption and decryption or reduce the plaintext/ciphertext pairs cipher to Base64 '
#          'characters - which is lossy without pre/post processing. This is useful for simulating pen and paper '
#          'use of Hexafid in the field where an agent may not efficiently Base64 en/decode by hand. '
#          'The default for preserve is true.'
# )
@click.option(
    '--soft/--field',
    type=bool,
    default=True,
    help='A flag to specify whether you want to operate under Software Use or Field Use settings. '
         'Software settings default to CBC mode with period 20, rounds 20, and full preservation of plaintext. '
         'Field settings default to CBC mode with period 10, rounds 1, reduction of plaintext to Base64 characters, '
         'and insertion of a word separator (/) to preserve readability. Restrict Field Use to short messages '
         'of short lifespan and rotated unique keys. If not provided, the default is Software Use.'
)
@click.version_option()
@click.pass_context
# possible removal of separator and preserve as CLI options since the use cases would adjust those automatically
def main(ctx, encrypt, filein, fileout, key, mode, soft):  # removed iv, period, rounds, separator, preserve,
    if not key:
        key = keygen.get_random_key()
    elif not hexafid.key_is_valid(key):
        key = keygen.get_key_from_pass(key, 'forward', soft)  # true for KDF; false no KDF

    if mode == 'CBC':       # this CBC mode passes 99.7% randomness tests for values tested
        period = 20
        rounds = 20         # starts testing random at P20R1
        separator = False
        preserve = True
        disclaimer = '!!! WARNING not proven secure with academic rigour DANGER !!!\n'
        restriction = '\nRESTRICT USE to short messages of short lifespan and rotated UNIQUE KEYS'
    elif mode == 'CTR':     # this CTR mode passes 100% randomness tests for values tested
        period = 20
        rounds = 20         # starts testing random at P20R5
        separator = False
        preserve = True
        disclaimer = '!!! WARNING not proven secure with academic rigour DANGER !!!\n'
        restriction = '\nRESTRICT USE to short messages of short lifespan and rotated UNIQUE KEYS'
    else:                   # ECB mode - not secure beyond one block with random key - but 99.7% passes at this
        period = 20         # for short messages (< period), short lifespans (< day), and rotating unique keys
        rounds = 20         # starts testing random at P20R3
        separator = False
        preserve = True
        disclaimer = '!!! WARNING not proven secure with academic rigour DANGER !!!\n'
        restriction = '\nRESTRICT USE to short messages of short lifespan and rotated UNIQUE KEYS'

    if not soft:  # CBC P10R1 passed full NIST STS 15/16 times (94%) and 255/256 (99.6%) of tests in those 16 runs
        mode = 'CBC'
        period = 10
        rounds = 1
        separator = True
        preserve = False
        disclaimer = '!!! WARNING not secure against sophisticated adversaries DANGER !!!\n'
        restriction = '\nRESTRICT USE to short messages of short lifespan and rotated UNIQUE KEYS'

    # Automatically generate random IV
    iv = keygen.get_iv(period)

    # if not iv:
    #     iv = keygen.get_iv(period)
    # elif not hexafid.iv_is_valid(iv, period):
    #     click.echo('Initialization Vector is either invalid in length or characters. '
    #                'It must match length of period and be from the Base64 character set.')
    # else:
    #     iv

    # If key storage needed import 'keyring' and do following:
    # keyring.set_password('hexafid_cli', 'hexafid_key', key)
    # keyring.get_password('hexafid_cli', 'hexafid_key'))

    if filein:
        message = _handle_file(filein)
    else:
        message = click.prompt('Enter your message here')

    print(disclaimer)

    if fileout and encrypt:  # encrypt message to disk
        print('Hexafid Encrypt: %s mode with %s character block size and %s rounds\n'
              'Hexafid Key: %s' % (mode, period, rounds, key))
        fileout.write(hexafid.encrypt(message, key, mode, iv, period, rounds, separator, preserve))
    elif fileout and not encrypt:  # decrypt message to disk
        print('Hexafid Decrypt: %s mode with %s character block size and %s rounds\n'
              'Hexafid Key: %s' % (mode, period, rounds, key))
        fileout.write(hexafid.decrypt(message, key, mode, period, rounds, separator, preserve))
    elif not fileout and encrypt:  # encrypt message to standard out
        print('Hexafid Encrypt: %s mode with %s character block size and %s rounds\n'
              'Hexafid Key: %s' % (mode, period, rounds, key))
        encrypted = hexafid.encrypt(message, key, mode, iv, period, rounds, separator, preserve)
        click.echo('Ciphertext: %s' % encrypted)
    else:  # decrypt message to standard out
        print('Hexafid Decrypt: %s mode with %s character block size and %s rounds\n'
              'Hexafid Key: %s' % (mode, period, rounds, key))
        decrypted = hexafid.decrypt(message, key, mode, period, rounds, separator, preserve)
        click.echo('Plaintext: %s' % decrypted)

    print(restriction)


def _handle_file(filein):
    try:
        message = filein.read()
    except UnicodeDecodeError as e:
        log.debug(str(e), exc_info=True)
        raise click.FileError(
            filein.name,
            "<file> must be encoded using 'utf-8'.")

    return message


if __name__ == '__main__':
    main()
#
