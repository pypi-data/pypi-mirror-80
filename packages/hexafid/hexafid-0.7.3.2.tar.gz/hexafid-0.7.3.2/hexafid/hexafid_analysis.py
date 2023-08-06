# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import math
import random

# Third party imports
# Local application imports
import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen


def shannon(sentence):  # H
    """Equation for Shannon's Entropy is implemented.
    Adapted from Aerin Kim 2018, The Intuition Behind Shannons' Entropy"""
    entropy = 0
    # There are 256 possible ASCII characters
    for character_i in range(256):
        prob_x = sentence.count(chr(character_i)) / len(sentence)  # Px
        if prob_x > 0:
            entropy += - prob_x * math.log(prob_x, 2)

    return entropy


def check_related_keys(key, rounds):
    """Naive function for seeing if keys repeat over time. WARNING: memory intensive."""
    source_key = keygen.use_sequence_layout(key)
    key_ring = list()

    # setup encoders
    seq_encoder, seq_decoder = hexafid.setup_sequence_addresses(key)
    quad_encoder, quad_decoder = hexafid.setup_quadtree_addresses(key)

    # setup round keys for key schedule
    round_keyset = list()
    magic_number = 42  # nothing up my sleeves number to initialize key schedule
    # This first round key allows for direct use of K0 = K to simplify field use before key scheduling
    round_keyset.append((quad_encoder, quad_decoder, seq_encoder, seq_decoder, magic_number))
    # The rest of the key schedule is established here
    for r in range(rounds - 1):
        round_keyset.append(hexafid.get_round_keys(round_keyset[r][0], round_keyset[r][1],
                                                   round_keyset[r][2], round_keyset[r][3], round_keyset[r][4]))
        key_ring.append(''.join(list(round_keyset[r + 1][0])))

    return source_key in key_ring


def main():
    # When using only 32 chars
    simple_message = "".join([chr(random.SystemRandom().randint(0, 32)) for i in range(10000)])
    # When using only 64 chars
    medium_message = "".join([chr(random.SystemRandom().randint(0, 64)) for j in range(10000)])
    # When using all 255 chars
    complex_message = "".join([chr(random.SystemRandom().randint(0, 255)) for k in range(10000)])

    print(shannon(simple_message))
    print(shannon(medium_message))
    print(shannon(complex_message))

    key = keygen.get_random_key()
    print(check_related_keys(key, 100000))  # tested so far up to 1000000 - more memory required above that


if __name__ == '__main__':
    main()
