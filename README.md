# CTFFI

Foreign Function Interface for calling [FaCT](https://github.com/PLSysSec/FACT) code from Python, built on CFFI.

Compatible with Python 2 and 3.

# Example

In this example, we'll use two files, one to build a Python extension module containing the
FaCT code, and the other to execute it.

First, you will need to run `hello_build.py`, immediately below. Replace `/path/to/fact.byte`
with the full path to the `fact.byte` executable.

```python
#!/usr/bin/python
#
# (C) 2018 Riad S. Wahby <rsw@cs.stanford.edu> and the FaCT authors
#
# Simple example: compile hello world FaCT code

import ctffi

if __name__ == "__main__":
    ffibuilder = ctffi.CTFFI("/path/to/fact.byte")
    ffibuilder.set_fact_source("_hello_world", r"""
export
void conditional_swap(secret mut uint32 x, secret mut uint32 y, secret bool cond) {
  if (cond) {
    secret uint32 tmp = x;
    x = y;
    y = tmp;
  }
}
""")
    ffibuilder.compile(verbose=True)
```

Once you've invoked the above once, you can then call it from other code, e.g.:

```python
#!/usr/bin/python
#
# (C) 2018 Riad S. Wahby <rsw@cs.stanford.edu> and the FaCT authors
#
# Simple example: invoke hello world FaCT code from Python

from __future__ import print_function
from _hello_world import lib, ffi

if __name__ == "__main__":
    foo = ffi.new("uint32_t *", 1)
    bar = ffi.new("uint32_t *", 2)
    print("Values before swap:\nfoo: %d, bar: %d\n" % (foo[0], bar[0]))

    print("Swapping with condition = True.\n")
    lib.conditional_swap(foo, bar, True)
    print("Values after swap:\nfoo: %d, bar: %d\n" % (foo[0], bar[0]))

    print("Swapping with condition = False.\n")
    lib.conditional_swap(foo, bar, False)
    print("Values after swap:\nfoo: %d, bar: %d\n" % (foo[0], bar[0]))

    print("Swapping with condition = True.\n")
    lib.conditional_swap(foo, bar, True)
    print("Values after swap:\nfoo: %d, bar: %d\n" % (foo[0], bar[0]))
```

# License

   Copyright (C) 2018 Riad S. Wahby <rsw@cs.stanford.edu> and the FaCT authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
