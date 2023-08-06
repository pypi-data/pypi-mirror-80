.. _api-documentation:

Hexafid API
===========

Hexafid Core API
----------------
This API accesses the core features of Hexafid with the key entry points as below:

.. code-block:: python

   from hexafid import hexafid_core as hexafid
   hexafid.encrypt(message, key, mode, iv, period, rounds)  # returns ciphertext string
   hexafid.decrypt(message ,key, mode, period, rounds)  # returns plaintext string

.. automodule:: hexafid.hexafid_core
   :members:

Hexafid Keygen API
------------------
This API accesses key generation features to support Hexafid encryption and decryption.

.. automodule:: hexafid.hexafid_keygen
   :members:
