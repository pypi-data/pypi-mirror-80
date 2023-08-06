Hexafid Welcome!
================

Welcome to the Hexafid project. Hexafid is a `block cipher`_, extending the classical `Bifid Cipher`_,
with elements of modern `information theory`_. Here, you will find
:ref:`written instructions <Hexafid Field Cipher>` for both the pen and paper field cipher and the
:ref:`software installation <Hexafid Software Installation>` for the it's stronger software implementation.

.. contents:: Home Contents
    :local:

This Python software exposes both a :ref:`Command Line Interface (CLI)`, with suggested settings for (in)secure
(see :ref:`disclaimer <rst-disclaimer>`) communication, and an :ref:`Application Programming
Interface (API)`, with more freedom for testing and experimentation.

For more information on the background and algorithms of the cipher, please go :ref:`here. <hexafid-background>`

Hexafid Field Cipher
--------------------
Hexafid began as a modern evolution to the field ciphers of `Felix Delastelle`_. The instructions outlined here
describe how to encrypt and decrypt messages using the simplified Hexafid Field Cipher using pen and paper.
It uses the 64 character key with Cipher Block Chaining (CBC) mode across a period of 10 characters but only
1 round of the substitution and transposition algorithm and no key schedule.

- :download:`Download written instructions <../xtra/Hexafid_Field_Cipher.pdf>`

Hexafid Software Installation
-----------------------------
Use the package manager `pip`_ to install hexafid in your `virtual environment`_:

.. code-block:: console

   $ pip install hexafid

Command Line Interface (CLI)
----------------------------
As an end user you can execute commands, like the following, in your `virtual environment`_:

.. code-block:: console

   $ hexafid --version
   $ hexafid --help
   $ hexafid

The full **CLI Documentation** is :ref:`here. <cli-documentation>`

Application Programming Interface (API)
---------------------------------------
As a developer, you can enter the Hexafid Cipher at two key points--encryption and decryption:

.. code-block:: python

   from hexafid import hexafid_core as hexafid
   hexafid.encrypt(message, key, mode, iv, period, rounds)  # returns ciphertext string
   hexafid.decrypt(message ,key, mode, period, rounds)  # returns plaintext string

NOTE: developer use of these libraries assumes that you understand the cryptographic implications of changing the parameters in the function calls.

The full **API Documentation** is :ref:`here. <api-documentation>`

Clipboard Widget (GUI)
----------------------
As an iOS user, you can use the Hexafid Clipboard Widget to bring Hexafid encryption/decryption to your device's
Graphical User Interface (GUI) by first installing `Pythonista`_.

The full **Widget Documentation** is :ref:`here. <widget-documentation>`

Contributing
------------

The project is hosted at https://gitlab.com/hexafid/hexafid/

We expect team members to have minimum knowledge as found at https://www.coursera.org/learn/crypto.

Merge requests are welcome. Please open an issue first to discuss what you would like to change.
Please make sure to include and/or update tests as appropriate.

.. _rst-disclaimer:

Disclaimer
----------
Hexafid began as a hobby project during the COVID-19 pandemic. While attempts have been made to create good crypto,
the work has NOT been peer reviewed by the academic community. The algorithms have NOT been proven to have
strong security. The software is released under an :ref:`open source licence (MIT) <license>` that (a) Limits ANY liability,
and (b) Provides NO warranty.

.. _Bifid Cipher: https://en.wikipedia.org/wiki/Bifid_cipher
.. _block cipher: https://en.wikipedia.org/wiki/Block_cipher
.. _information theory: https://en.wikipedia.org/wiki/Information_theory
.. _Felix Delastelle: https://en.wikipedia.org/wiki/F%C3%A9lix_Delastelle
.. _pip: https://pip.pypa.io/en/stable/
.. _virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
.. _Pythonista: https://omz-software.com/pythonista/

.. toctree::
   :caption: Further documentation
   :maxdepth: 2

   hexafid-background
   hexafid-cli
   hexafid-api
   hexafid-widget
   hexafid-license
   indices-tables
