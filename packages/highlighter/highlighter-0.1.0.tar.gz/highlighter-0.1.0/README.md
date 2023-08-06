# highlighter

Easy to use PEP 508 markers.  These are the strings in requirements after a
semicolon, such as `enum34; python_version < '3.5'` means the package `enum34`
but only on some versions of python.


```py
from packaging.markers import Marker
from packaging.requirements import Requirement

from highlighter import EnvironmentMarkers

req = Requirement("enum34; python_version < '3.5'")

env = EnvironmentMarkers.for_python("3.7.5", "win32")
env.match(req.marker)  # False

# Lower-level interface, you can use Marker directly
m = Marker("python_version < '3.5'")
env.match(m)  # False

# What about extras?
req = Requirement("somepackage[foo,bar]")
m = Marker("extra == 'foo'")
env.match(m, extras=req.extras) # True
```

## Egg-info Extras

This also includes a function that can convert a requires.txt (as found in
egg-info dirs, the only kind we have in sdists) into an equivalent list of
requirements.txt lines using PEP 508 markers.

```py
from highlighter.sdist import convert_sdist_requires

convert_sdist_requires("""\
[socks]
PySocks!=1.5.7,>=1.5.6

[socks:sys_platform == "win32" and python_version == "2.7"]
win_inet_pton
""") == """\
PySocks!=1.5.7,>=1.5.6; extra == 'socks'
win_inet_pton; (sys_platform == "win32" and python_version == "2.7") and extra == 'socks'
"""
```

# License

highlighter is copyright [Tim Hatch](https://timhatch.com/), and licensed under
the MIT license.  I am providing code in this repository to you under an open
source license.  This is my personal repository; the license you receive to
my code is from me and not from my employer. See the `LICENSE` file for details.
