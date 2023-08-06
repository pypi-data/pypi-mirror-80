.. _hexafid-background:

Background
==========

Hexafid is a `block cipher`_, extending the classical `Bifid Cipher`_, with elements of modern `information theory`_.

In classical terms, Hexafid's Field Mode accepts a 64 character key and operates on a message over a period of
10 characters; it uses substitution with fractionation then transposition to achieve confusion and diffusion.

In modern terms, Hexafid's Field Mode accepts a ~296 bit key--a permutation of the Base 64
character set--and operates on a message over a 60 bit block size (i.e. 10 characters of 6 bits each);
each cipher block passes through a single round of the substitution and transposition algorithm and is
chained together.

Here are the :download:`written instructions <../xtra/Hexafid_Field_Cipher.pdf>` for using Hexafid as a
pen and paper field cipher:

Strengthened in software, Hexafid operates with a sophisticated `key schedule`_ over multiple rounds and across
various `block cipher modes`_ (e.g. ECB, CTR, CBC). Within this context, Hexafid is implemented as a 120 bit
block cipher over 20 rounds with sub-keys generated through addition, substitution, shifts, and rotations.

.. parsed-literal::

         0            0
          \\          /
           1100110011
          110000000011
    0 -- 11000000000011 -- 0
          110000000011
           1100110011
          /          \\
         0            0

A post-apocalyptic field cipher: where the remnants of humanity fight for survival,
they need a simple and secure way to share secrets.

Inception
---------

Historical Context
    * Bifid/Trifid Ciphers - `Felix Delastelle (1902)`_
    * Bits of Information - `Claude Shannon (1948)`_
    * Quadtree Data Structures - `Finkel and Bentley (1974)`_
    * Base64 Encoding - `IETF PEM (1987)`_

Design Goals
    * Works easily with pen and paper
    * Secures confidentiality of information
    * Offers plausible deniability if discovered
    * Exhibits greater strength in software


At the core...
--------------
The Key Square

+-----+-----+-----+-----+-----+-----+-----+-----+
|  M  |  y  |  P  |  a  |  s  |  w  |  o  |  r  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  d  |  1  |  2  |  3  |  A  |  B  |  C  |  D  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  E  |  F  |  G  |  H  |  I  |  J  |  K  |  L  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  N  |  O  |  Q  |  R  |  S  |  T  |  U  |  V  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  W  |  X  |  Y  |  Z  |  b  |  c  |  e  |  f  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  g  |  h  |  i  |  j  |  k  |  l  |  m  |  n  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  p  |  q  |  t  |  u  |  v  |  x  |  z  |  0  |
+-----+-----+-----+-----+-----+-----+-----+-----+
|  4  |  5  |  6  |  7  |  8  |  9  | \+  |  /  |
+-----+-----+-----+-----+-----+-----+-----+-----+

The Sequence Key (Ks)

+-----+------+
| 01  | ...  |
+-----+------+
| ... |  64  |
+-----+------+

The Quadress Key (Kq)

+------+------+
|  00  |  01  |
+------+------+
|  11  |  10  |
+------+------+

Substitution

+-----+-----+-----+-----+-----+
|  H  |  E  |  L  |  L  |  O  |
+=====+=====+=====+=====+=====+
|  0  |  1  |  1  |  1  |  0  |
+-----+-----+-----+-----+-----+
|  0  |  0  |  0  |  0  |  1  |
+-----+-----+-----+-----+-----+
|  1  |  0  |  0  |  0  |  0  |
+-----+-----+-----+-----+-----+
|  0  |  1  |  0  |  0  |  1  |
+-----+-----+-----+-----+-----+
|  0  |  0  |  1  |  1  |  0  |
+-----+-----+-----+-----+-----+
|  1  |  0  |  0  |  0  |  0  |
+-----+-----+-----+-----+-----+

Transposition

+-----+-----+-----+-----+-----+
|[ 0  |  1  |  1  |  1  |  0  |
+-----+-----+-----+-----+-----+
|  0 ]|[ 0  |  0  |  0  |  1  |
+-----+-----+-----+-----+-----+
|  1  |  0 ]|[ 0  |  0  |  0  |
+-----+-----+-----+-----+-----+
|  0  |  1  |  0 ]|[ 0  |  1  |
+-----+-----+-----+-----+-----+
|  0  |  0  |  1  |  1 ]|[ 0  |
+-----+-----+-----+-----+-----+
|  1  |  0  |  0  |  0  |  0 ]|
+-----+-----+-----+-----+-----+
|**I**|**3**|**1**|**A**|**s**|
+-----+-----+-----+-----+-----+

Block Cipher Modes
------------------

Hexafid - Electronic Code Book Mode

.. parsed-literal::
         Pt
         |
    Kn-- S
         T
         |
         Ct


Hexafid - Counter Mode

.. parsed-literal::
       IV001        IV002
         |            |
    Kn-- S       Kn-- S
         T            T
         |            |
    Pt-- +       Pt-- +
         |            |
         Ct           Ct

Hexafid - Cipher Block Chaining Mode

.. parsed-literal::
         Pt           Pt
         |            |
    IV-- + --Ks   --- + --Ks   -- ...
         |       |    |       |
         S --Kn  |    S --Kn  |
         T       |    T       |
         | ------     | ------
         Ct           Ct

Key Schedule
------------

Hexafid - Key Schedule

.. parsed-literal::
                    Pt
                    |
            K1------S
            |       T
    NUMS-- + %      |
          << R      Ct
            |       |
            K2------S
            |       T
    K1---- + %      |
          << R      Ct
            |       |
            K3------S
            |       T
    K2---- + %      |
          << R      Ct
            |       |
            Kn
            |

.. _Felix Delastelle (1902): https://archive.org/details/8VSUP3207b
.. _Claude Shannon (1948): http://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
.. _Finkel and Bentley (1974): https://www.researchgate.net/profile/Raphael_Finkel/publication/220197855_Quad_Trees_A_Data_Structure_for_Retrieval_on_Composite_Keys/links/0c9605273bba2ece7b000000/Quad-Trees-A-Data-Structure-for-Retrieval-on-Composite-Keys.pdf
.. _IETF PEM (1987): https://tools.ietf.org/html/rfc989

.. _Bifid Cipher: https://en.wikipedia.org/wiki/Bifid_cipher
.. _block cipher: https://en.wikipedia.org/wiki/Block_cipher
.. _block cipher modes: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
.. _information theory: https://en.wikipedia.org/wiki/Information_theory
.. _key schedule: https://en.wikipedia.org/wiki/Key_schedule
