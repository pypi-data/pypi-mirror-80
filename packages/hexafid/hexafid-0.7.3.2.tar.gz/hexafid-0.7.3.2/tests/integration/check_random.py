# MIT License
# Copyright (c) 2020 h3ky1

import io
import os
import sys
import time
import datetime
import base64

from sts.FrequencyTest import FrequencyTest
from sts.RunTest import RunTest
from sts.Matrix import Matrix
from sts.Spectral import SpectralTest
from sts.TemplateMatching import TemplateMatching
from sts.Universal import Universal
from sts.Complexity import ComplexityTest
from sts.Serial import Serial
from sts.ApproximateEntropy import ApproximateEntropy
from sts.CumulativeSum import CumulativeSums
from sts.RandomExcursions import RandomExcursions

import hexafid.hexafid_core as hexafid
import hexafid.hexafid_keygen as keygen
# import hexafid.hexafid_utilities as utilities


def main():
    key_list = list()
    bad_key_list = list()
    input_filename = '../data/frankenstein.txt'
    # key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    # iv = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    # iv = keygen.get_iv(64)  # random fixed iv for tests

    # known bad keys
    bad_key_list.append(['eGkvR2J5x7qVE40rtdNfs9iOhY/8AHpKbXza36WUMmIBC1owuycDngPFjTLZlQS+',
                        'CBC', 'tdSCmw21M3MsDhA5', 16, 16])
    bad_key_list.append(['ZwH6fMYpgsQG1XcNEVRaKtqmy8l/LTAu42vznF7DSxo93drjUePbJ0+O5CBkhIiW',
                        'CBC', 'PmxznBHaC7vEY1/6', 16, 16])
    bad_key_list.append(['ibWOZjXPT28g5Ke9kcry7CluE1/Ad+4MGhSNJoDnqsI3FwBzYtQUpxLvfaRm60HV',
                        'CBC', 'KSgehGSNHoz7SPFL', 16, 16])
    bad_key_list.append(['VQJECotTuUl6xZaO1sY9c8hq2ymz03gHfRdbn+BpSGFIiAWr/5D7jLwvMPXKe4Nk',
                        'CBC', '9Zp0C//tIvGv0Jd/', 16, 16])
    bad_key_list.append(['7G9KHAbgCMYJ25ByS4FO1qWPNRmIQpcfn+zEtxLu8aVviDehToUjkdl3Xr60wsZ/',
                         'CBC', 'tdSCmw21M3MsDhA5', 16, 16])

    for k in range(5):
        # key_list.append(bad_key_list[k][0])  # range 5
        key_list.append(keygen.get_random_key())

    mode_list = ['ECB', 'CBC', 'CTR']  # 'ECB', 'CTR']

    # check for no input file
    if not os.path.exists(input_filename):
        print('The file %s does not exist. Quitting...' % input_filename)
        sys.exit()

    # read message from file utf8
    input_file = io.open(input_filename, mode="r", encoding="utf-8")
    content = input_file.read()
    input_file.close()

    # tests modes from list
    for mode in mode_list:

        # tests period (block size = period * 6 bits) in stated range
        for period in range(20, 21):  # range(20, 21):  # multiples of key size

            iv = keygen.get_iv(period)
            # iv = iv[:period]

            # tests block cipher rounds in stated range
            for rounds in range(20, 21):

                for key in key_list:  # used for evaluating how a set of keys works on same parameters

                    for attempt in range(1):  # used for evaluating whether a fixed key has different results

                        intermediate_filename = '../data/frankenstein.hex'

                        start_time = time.time()
                        print('Encrypting...')
                        print('Key: ' + key)
                        print('Mode: ' + mode)
                        print('IV: ' + iv[:period])
                        print('Period: ' + str(period))
                        print('Rounds:' + str(rounds))
                        translated = hexafid.encrypt(content, key, mode, iv[:period], period, rounds,
                                                     separator=True, preserve=False)
                        print('Encryption complete.')

                        # write translated message to file
                        output_file = io.open(intermediate_filename, 'w', encoding="utf-8")
                        output_file.write(translated)
                        output_file.close()

                        # use last Hexafid key to map chars to binary
                        # binary_file = utilities.hex2bin(translated, key, rounds)

                        # or use base64 decoding to map chars to binary
                        decoded = base64.b64decode(translated)
                        binary_file = ''.join(('{:08b}'.format(x) for x in decoded))

                        output_filename = '../data/frankenstein_' \
                            + mode + '_' + 'P' + str(period) + 'R' + str(rounds) + '.bin'

                        # write translated message to file
                        output_file = io.open(output_filename, 'w', encoding="utf-8")
                        output_file.write(binary_file)
                        output_file.close()

                        total_time = round(time.time() - start_time, 2)
                        print('Processing time: %s seconds' % total_time)

                        # test_file('frankenstein_' + mode + '_' + 'P' + str(period) + 'R' + str(rounds) + '.bin')
                        find_threshold('frankenstein_' + mode + '_' + 'P' + str(period) + 'R' + str(rounds) + '.bin',
                                       key, mode, iv[:period], period, rounds, total_time)


def find_threshold(filename, key, mode, iv, period, rounds, total_time):
    # Open Data File and read the binary data of e
    data_list = []
    data_path = os.path.join(os.pardir, 'data', filename)
    handle = open(data_path)
    for line in handle:
        data_list.append(line.strip().rstrip())
    binary_data = ''.join(data_list)

    test_list = [
        (FrequencyTest.monobit_test, binary_data[:1000000]),
        (FrequencyTest.block_frequency, binary_data[:1000000]),
        (RunTest.run_test, binary_data[:1000000]),
        (RunTest.longest_one_block_test, binary_data[:1000000]),
        (Matrix.binary_matrix_rank_text, binary_data[:1000000]),
        (SpectralTest.sepctral_test, binary_data[:1000000]),
        (TemplateMatching.non_overlapping_test, binary_data[:1000000]),
        (TemplateMatching.overlapping_patterns, binary_data[:1000000]),
        (Universal.statistical_test, binary_data[:1000000]),
        (ComplexityTest.linear_complexity_test, binary_data[:1000000]),
        (Serial.serial_test, binary_data[:1000000]),  # 'e[1] for e in
        (ApproximateEntropy.approximate_entropy_test, binary_data[:1000000]),
        (CumulativeSums.cumulative_sums_test, binary_data[:1000000], 0),  # forward is the default
        (CumulativeSums.cumulative_sums_test, binary_data[:1000000], 1),  # also can test in reverse
        (RandomExcursions.random_excursions_test, binary_data[:1000000]),
        (RandomExcursions.variant_test, binary_data[:1000000])
    ]

    test_results = []

    for test in test_list:
        if len(test) == 3:
            if False in test[0](test[1], test[2]):
                test_results.append('F')
            else:
                test_results.append('.')
        else:
            if False in test[0](test[1]):
                test_results.append('F')
            else:
                test_results.append('.')

    filename = 'frankenstein_' + mode + '_' + 'P' + str(period) + 'R' + str(rounds) + '.bin'
    output_file = io.open('../data/frankenstats.txt', 'a', encoding="utf-8")
    output_file.write(
        str(datetime.datetime.now().date().strftime("%Y-%m-%d")) + ',' +
        str(datetime.datetime.now().time().strftime("%H:%M:%S")) + ',' +
        filename + ',' +
        str(total_time) + ',' +
        str(''.join(test_results)) + ',' +
        key + ',' +
        mode + ',' +
        iv + ',' +
        str(period) + ',' +
        str(rounds) + '\n'
    )
    output_file.close()


def test_file(filename):

    # Open Data File and read the binary data of e
    data_path = os.path.join(os.pardir, 'data', filename)
    handle = open(data_path)
    data_list = []

    for line in handle:
        data_list.append(line.strip().rstrip())

    binary_data = ''.join(data_list)

    print('The statistical test of ' + filename)
    print('2.01. Frequency Test:\t\t\t\t\t\t\t\t',
          FrequencyTest.monobit_test(binary_data[:1000000]))
    print('2.02. Block Frequency Test:\t\t\t\t\t\t\t',
          FrequencyTest.block_frequency(binary_data[:1000000]))
    print('2.03. Run Test:\t\t\t\t\t\t\t\t\t\t',
          RunTest.run_test(binary_data[:1000000]))
    print('2.04. Run Test (Longest Run of Ones): \t\t\t\t',
          RunTest.longest_one_block_test(binary_data[:1000000]))
    print('2.05. Binary Matrix Rank Test:\t\t\t\t\t\t',
          Matrix.binary_matrix_rank_text(binary_data[:1000000]))
    print('2.06. Discrete Fourier Transform (Spectral) Test:\t',
          SpectralTest.sepctral_test(binary_data[:1000000]))
    print('2.07. Non-overlapping Template Matching Test:\t\t',
          TemplateMatching.non_overlapping_test(binary_data[:1000000], '000000001'))
    print('2.08. Overlapping Template Matching Test: \t\t\t',
          TemplateMatching.overlapping_patterns(binary_data[:1000000]))
    print('2.09. Universal Statistical Test:\t\t\t\t\t',
          Universal.statistical_test(binary_data[:1000000]))
    print('2.10. Linear Complexity Test:\t\t\t\t\t\t',
          ComplexityTest.linear_complexity_test(binary_data[:1000000]))
    print('2.11. Serial Test:\t\t\t\t\t\t\t\t\t',
          Serial.serial_test(binary_data[:1000000]))
    print('2.12. Approximate Entropy Test:\t\t\t\t\t\t',
          ApproximateEntropy.approximate_entropy_test(binary_data[:1000000]))
    print('2.13. Cumulative Sums (Forward):\t\t\t\t\t',
          CumulativeSums.cumulative_sums_test(binary_data[:1000000], 0))
    print('2.13. Cumulative Sums (Backward):\t\t\t\t\t',
          CumulativeSums.cumulative_sums_test(binary_data[:1000000], 1))

    result = RandomExcursions.random_excursions_test(binary_data[:1000000])
    print('2.14. Random Excursion Test:')
    print('\t\t STATE \t\t\t xObs \t\t\t\t P-Value \t\t\t Conclusion')
    for item in result:
        print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
              (item[4] >= 0.01))

    result = RandomExcursions.variant_test(binary_data[:1000000])
    print('2.15. Random Excursion Variant Test:\t\t\t\t\t\t')
    print('\t\t STATE \t\t COUNTS \t\t\t P-Value \t\t Conclusion')
    for item in result:
        print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
              (item[4] >= 0.01))


# if run instead of called as module
if __name__ == '__main__':
    main()
