# IG-PROFILE-CLIENT
[![codecov](https://codecov.io/gh/Panchorn/ig-profile-client/branch/master/graph/badge.svg)](https://codecov.io/gh/Panchorn/ig-profile-client)
[![PyPI](https://img.shields.io/pypi/v/ig-profile-client.svg)](https://pypi.org/project/ig-profile-client/)

This library is a client to get Instagram profile data (public data).

###### I have made this for publishing a package to PyPI only!

## Usage
Install package by using pip:
```bash
pip install -U ig-profile-client
```

## Example
```python
from IgProfileClient import Client

client = Client()
profile = client.get_common_profile("username")

print(profile.__dict__)
print(profile.follower)
```

## Uninstall package
```bash
pip uninstall ig-profile-client 
```
