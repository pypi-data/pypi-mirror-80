# TacitPy

> Tacit Python programming.

## Example

```py
from tacit import *

add5 = add(5)
print('6 + 5 =', add5(6))
	#=> 11

@Curry("int -> int -> float")
def f(x, y):
	return (6.5 + x) * y

# or
f = Curry(lambda x, y: (6 + x) * y)

a = (f(3) * add(2))(5)
b = f(3, 2 + 5)

print('a == b  #=>', a == b)
	#=> true
```

