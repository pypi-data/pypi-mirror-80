#!python3

# MIT License
# Copyright (c) 2020 h3ky1

"""
The Hexafid Clipboard Widget in iOS 13/14 widget for Pythonista 3.3 shows the current contents of the clipboard
which can be encrypted or decrypted by tapping the respective buttons.
"""

# Standard library imports
import re
import sys

# Third party imports
if sys.platform == 'ios':
    import appex
    import clipboard
    import keychain
    import sound
    import ui

    # Local application imports
    import hexafid_core as hexafid
    import hexafid_keygen as keygen

    # load any previous key from iOS keychain
    key = keychain.get_password('hexafid_widget', 'hexafid_key')
    if key is None:
        key = ''


def _button_tapped(sender):
    """
    This callback function handles the various button features of the Hexafid Clipboard Widget in iOS. The
    buttons, and actions are:

    - **encrypt**       this button (jagged arrow right) encrypts clipboard text with saved key
    - **decrypt**       this button (jagged arrow left) decrypts clipboard text with saved key
    - **keygen**        this button (circular arrow) generates and saves new key into keystore
    - **keypaste**      this button (unlocked lock) pastes (imports) copied key to clipboard and keystore
    - **keycopy**       this button (upright key) copies (exports) current key from keystore to clipboard

    :param sender:  the button that calls this handling function
    :return:        nothing; although button presses update the UI through this function
    """
    global IMPORTED_KEY
    global key
    message = clipboard.get()
    mode = 'CBC'
    period = 20  # 16
    rounds = 20  # 16
    iv = keygen.get_iv(period)

    if message:

        if key == '':
            key = keygen.get_random_key()

        if sender.name == 'encrypt':
            sound.play_effect('arcade:Jump_4')
            translated = hexafid.encrypt(message, key, mode, iv, period, rounds)
            clipboard.set(translated)

        elif sender.name == 'decrypt':
            sound.play_effect('arcade:Laser_2')
            translated = hexafid.decrypt(message, key, mode, period, rounds)
            clipboard.set(translated)

        elif sender.name == 'keygen':
            sound.play_effect('arcade:Powerup_1')

            # check for possible key in clipboard
            if re.match(r'^(?!.*(.).*\1)[A-Za-z0-9+/]+$', clipboard.get()):
                key = clipboard.get()
                IMPORTED_KEY = True
            else:
                key = keygen.get_random_key()
                IMPORTED_KEY = False

            translated = message

        elif sender.name == 'keycopy':
            sound.play_effect('arcade:Coin_3')
            translated = message
            clipboard.set(key)

    # store key in secure iOS keychain
    keychain.set_password('hexafid_widget', 'hexafid_key', key)

    sender.superview['message_label'].text = translated + '\n\nKey: ' + key[:7] + '...' + key[-7:]


def main():
    """
    The main function that sets up the UI for the Hexafid Clipboard Widget on iOS.

    :return:       none
    """
    global IMPORTED_KEY
    IMPORTED_KEY = False

    v = ui.View(frame=(0, 0, 320, 220))
    v.background_color = '#333333'

    header_label = ui.Label(frame=(64, 10, 320 - 64 - 64, 20), flex='w')
    header_label.name = 'header_label'
    header_label.font = ('Courier', 12)
    header_label.text_color = '#ffffff'
    header_label.number_of_lines = 0
    v.add_subview(header_label)

    message_label = ui.Label(frame=(64, 30, 320 - 64 - 64, 220 - 30), flex='wh')
    message_label.name = 'message_label'
    message_label.font = ('Courier', 12)
    message_label.text_color = '#00d200'
    message_label.number_of_lines = 0
    v.add_subview(message_label)

    encrypt_btn = ui.Button(name='encrypt',
                            image=ui.Image('iow:arrow_graph_up_right_256'),
                            flex='l',
                            tint_color='#ffdb00')
    encrypt_btn.frame = (320 - 54, 10 - 5, 44, 44)
    encrypt_btn.action = _button_tapped
    v.add_subview(encrypt_btn)

    decrypt_btn = ui.Button(name='decrypt',
                            image=ui.Image('iow:arrow_graph_down_left_256'),
                            flex='r',
                            tint_color='#ffdb00')
    decrypt_btn.frame = (10, 10 - 5, 44, 44)
    decrypt_btn.action = _button_tapped
    v.add_subview(decrypt_btn)

    # check for possible key in clipboard
    if re.match(r'^(?!.*(.).*\1)[A-Za-z0-9+/]+$', clipboard.get()) or IMPORTED_KEY:
        keygen_btn = ui.Button(name='keygen',
                               image=ui.Image('iow:unlocked_256'),
                               flex='l',
                               tint_color='#ffdb00')
        IMPORTED_KEY = True
    else:
        keygen_btn = ui.Button(name='keygen',
                               image=ui.Image('iow:refresh_256'),
                               flex='l',
                               tint_color='#ffdb00')

    keygen_btn.frame = (320 - 54, 64 - 5, 44, 44)
    keygen_btn.action = _button_tapped
    v.add_subview(keygen_btn)

    keycopy_btn = ui.Button(name='keycopy',
                            image=ui.Image('iow:key_256'),
                            flex='r',
                            tint_color='#ffdb00')
    keycopy_btn.frame = (10 - 5, 64 - 5, 44, 44)
    keycopy_btn.action = _button_tapped
    v.add_subview(keycopy_btn)

    appex.set_widget_view(v)
    text = clipboard.get()
    header_label.text = 'Hexafid Clipboard:'
    message_label.text = text + '\n\nKey: ' + key[:7] + '...' + key[-7:]


if __name__ == '__main__':
    if sys.platform == 'ios':
        main()
