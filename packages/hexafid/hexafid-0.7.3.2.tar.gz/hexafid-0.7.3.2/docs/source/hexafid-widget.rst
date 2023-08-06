.. _widget-documentation:

Hexafid Widget
==============

The functions here describe operation of the Hexafid Clipboard Widget. This module is a graphical
user interface (GUI) for iOS devices.

Installation
------------
These steps will integrate the Hexafid Clipboard Widget into the Today view of your iOS device.

#. You must have `Pythonista`_ running on your iOS device.
#. Add the following three files to a project subfolder:

    - hexafid_core.py
    - hexafid_keygen.py
    - hexafid_widget.py

#. Add Pythonista as a Widget to your iOS Today View.
#. Run "hexafid_widget.py" module from within Pythonista
#. Select 'Use in "Today"'

Features
--------

By copying some text on your device and then navigating to the Hexafid Clipboard Widget in the Today View,
you will gain access to a clipboard view with a number of buttons.

The callback function of the module hexafid_widget handles the various button features of the
Hexafid Clipboard Widget in iOS. The buttons, and actions, are:

    - **encrypt**       this button (jagged arrow right) encrypts clipboard text with saved key
    - **decrypt**       this button (jagged arrow left) decrypts clipboard text with saved key
    - **keygen**        this button (circular arrow) generates and saves new key into keystore
    - **keypaste**      this button (unlocked lock) pastes (imports) copied key to clipboard and keystore
    - **keycopy**       this button (upright key) copies (exports) current key from keystore to clipboard

.. _Pythonista: https://omz-software.com/pythonista/