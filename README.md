# VFA
B.S.c Final project - Verification and generation tools for Automatons 

# GUI
Project's gui will follow a minimalistic design. 
Gui was pre-designed using [this site](https://designer.gravit.io/?d=UGo_UmGpW)

# PerformanceAnalysis
## DVFAs Operations RUNTIME
![Intersection runtime](https://github.com/GalBrandwine/VFA/blob/Dev/Docs/updated%20images%20from%20analysis/RUNTIME_INTERSECTION.png)

![union runtime](https://github.com/GalBrandwine/VFA/blob/Dev/Docs/updated%20images%20from%20analysis/RUNTIME_UNION.png)

![run on 6PAL runtime](https://github.com/GalBrandwine/VFA/blob/performenceAnalysis/Docs/updated%20images%20from%20analysis/RUNTIM_on_6pal.png)

## DVFA pickle size
![pickle size](https://github.com/GalBrandwine/VFA/blob/performenceAnalysis/Docs/PicleSizeAnalysis/Pickle_Size.png)
Using the **Pickle** library.
<br> 
The pickle module implements binary protocols for serializing and de-serializing a Python object structure.
<br>
<br>
“Pickling” is the process whereby a Python object hierarchy is converted into a byte stream,
and “unpickling” is the inverse operation,
whereby a byte stream (from a binary file or bytes-like object) is converted back into an object hierarchy.

### Comparison with json
**There are fundamental differences between the pickle protocols and JSON (JavaScript Object Notation):**

* JSON is a text serialization format (it outputs unicode text, 
although most of the time it is then encoded to utf-8), 
while pickle is a binary serialization format;

* JSON is human-readable, while pickle is not;

* JSON is interoperable and widely used outside of the Python ecosystem, while pickle is Python-specific;

* JSON, by default, can only represent a subset of the Python built-in types, 
and no custom classes; pickle can represent an extremely large number of Python types (many of them automatically,
by clever usage of Python’s introspection facilities; 
complex cases can be tackled by implementing specific object APIs);
Unlike pickle, deserializing untrusted JSON does not in itself create an arbitrary code execution vulnerability.

#### Pros:
The data format used by pickle is Python-specific.
<br>
This has the advantage that there are no restrictions imposed by external standards such as JSON or XDR (which can’t represent pointer sharing);
<br>
however it means that non-Python programs may not be able to reconstruct pickled Python objects.

#### Cons:
The pickle module is not secure. One should only unpickle data one trust. 

It is possible to **construct malicious pickle data which will execute arbitrary code during unpickling**.
<br>
Never unpickle data that could have come from an untrusted source, or that could have been tampered with.
<br>
Consider signing data with hmac if you need to ensure that it has not been tampered with.
Safer serialization formats such as json may be more appropriate if you are processing untrusted data.

## Prerun Preparations:
While working on Some bigger DVFAs (with 1460 states and more),<br>
One might hit RecursionError, which point that maximum recursion depth exceeded while pickling an object.

Luckily, Increasing Python stack size is easy by adding the following lines to the code:
```python
import resource
import sys
print(resource.getrlimit(resource.RLIMIT_STACK))
print(sys.getrecursionlimit())
max_rec = 0x100000
# May segfault without this line. 0x100 is a guess at the size of each stack frame.
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)
```


**A note about *RECURSIONLIMIT*:** <br>
The default value is 1000.<br>
After setting RECURSIONLIMIT to 100000, we could easily work with big DVFAs (45k states).

While setting it to 100000 worked fine,<br>
one can set it to 1000, and it will still be enough for working with DVFAs that big.

After some research,<br>
we found that the RECURSIONLIMIT upper-bound for DVFAs with 45k states require at-least **3356**
