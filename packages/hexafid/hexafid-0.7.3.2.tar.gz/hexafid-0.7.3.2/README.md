## Hexafid

Hexafid is a post-apocalyptic field cipher. 

The project goals are to produce a cipher that:
- works easily with pen and paper
- secures confidentiality of information
- offers plausible deniability if discovered
- exhibits greater strength in software

The project includes a:
- cipher reference implementation in Python
- cross platform application with Command Line Interface (CLI)
- iOS Today View widget usable within Pythonista
- website hosting a cryptographic oracle (TBD)

all of which implement the Hexafid Cipher.

### Caveat Emptor

- Hexafid began as a hobby project during the COVID-19 pandemic
- The work has NOT been peer reviewed by the academic community
- The algorithms have NOT been proven to have strong security
- The software is released under an open source licence (MIT) that:
    - Limits ANY liability, and 
    - Provides NO warranty

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hexafid.

```bash
$ pip install hexafid
```

### Usage

As an end user:
```console
$ hexafid --version
$ hexafid --help
$ hexafid
```

As a developer:
```python
from hexafid import hexafid_core as hexafid
hexafid.encrypt(message, key, mode, iv, period, rounds)  # returns ciphertext string
hexafid.decrypt(message ,key, mode, period, rounds)  # returns plaintext string
```
NOTE: developer use of these libraries assumes that you understand the cryptographic implications of changing the parameters in the function calls.

### Documentation Home

https://hexafid.gitlab.io/hexafid

### Contributing
Merge Requests are welcome. For all changes, please:
1. open an Issue first to document the activity; 
2. label the Issue (e.g. Bug, Feature, Refactor, Suggestion, Test);
3. update or add any related tests to support your work;  
3. create an associated Merge Request to discuss changes with a maintainer.

We expect team members to have minimum knowledge as found in https://www.coursera.org/learn/crypto.

### License
[MIT License](https://hexafid.gitlab.io/hexafid/hexafid-license.html)