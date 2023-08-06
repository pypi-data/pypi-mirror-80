TokkoAuthLite
---
+ [How to install?](#installation)
+ [Using TokkoAuthLite](#usage)

# Installation

```bash
pip3 install tokko_auth_lite
sudo -H pip3 install tokko_auth_lite
```

# Usage
```python
from tokko_auth_lite.core import Token
from tokko_auth_lite.tools.testing import TokenFabrik

_jwt = TokenFabrik(permission=["companies:read_branches", "spacex:launch_rockets"])

token = Token.from_header({"Authorization": f"Bearer {_jwt}"})
print(token)
print(token.is_valid())
print(token.permissions)
print(token.has_permission("companies:read_branches", "spacex:launch_rockets"))
print(token.has_permission("spacex:launch_rockets"))
print(token.has_permission("companies:read_branches", "spacex:launch_rockets", require_all=True))
print(token.user_id)
```

# Tutorials
+ [TokenFabrik](./tokko_auth_lite/docs/ES/TUTORIALS.md)
    - [Quiero un JWT](./tokko_auth_lite/docs/ES/TUTORIALS.md#tutorial-i-dame-un-token)
    - [Uso avanzado](./tokko_auth_lite/docs/ES/TUTORIALS.md#tutorial-ii-crear-tokens-customizados)
