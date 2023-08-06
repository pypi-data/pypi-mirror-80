# Integrity Check

This package is the python version of a cross-language api for runtime internal tests. 

# How to use
Install the package (pip install integrity-check)

At the top of one of your python source code files put
`from integrity_check import Integrity`

then you can do things like:

`Integrity.check(a == b, "expected {} to be same as {}", a, b)`  
or  
`Integrity.check(a == b, a, b)`  
or even just  
`Integrity.check(a == b)`

The main function is `check`, but the full list of functions is:
```
    check(condition, *msg)
    checkNotNone(test, *msg)
    checkIsBool(test, *msg)
    checkIsBoolOrNone(test, *msg)
    checkIsString(test, *msg)
    checkIsStringOrNone(test, *msg)
    checkStringNotNoneOrEmpty(test, *msg)
    checkIsValidNumber(test, *msg)
    checkIsValidNumberOrNone(test, *msg)
    checkIsFunction(test, *msg)
    checkIsFunctionOrNone(test, *msg)
```
In all cases the *msg parameters work like this:

`check*(test)` - the exception will contain a default message  
`check*(test, var1)` - the message will be just the string representaiton of var1  
`check*(test, var1, var2, ... varN)` - the message will be the string representaitons of the vars in the format "var1, var2, ..., varN"  
`check*(test, "the vars are {} {}", var1, var2)` - the message will substitute the string representations of va1, var2 into the {}  
`check*(test, var1, var2, " and {} ", var3)` - the message will be "var1, var2 and var3"  

there can be as many message parameters as you like.
Note that if a variable is a string and happens to contain {} then it will be used in subsequent substitutions. 

# Example

```
from integrity_check import Integrity

def myComplicatedFunction(aNumber, callback, aName):
    Integrity.checkIsValidNumberOrNone(aNumber)
    Integrity.checkIsFunction(callback)
    Integrity.checkStringNotNoneOrEmpty(aName)

    handle = callback(aName)
    Integrity.checkNotNone(handle, "expected valid handle, aName was {}", aName)

    diameter = someOtherFunction(handle)
    Integrity.check(diameter >= 0, "expected non-negative diameter, was {}", diameter)
```

# What are the advantages of using Integrity?

## Consistent api across languages
If you jump around from one language to another, it is nice to have a consistent way of testing your assumptions regardless of what language you are in. For example:

Python: `Integrity.check(a == b, "some text {}", a)`  
JavaScript: `Integrity.check(a == b, "some text {}", a)`  
C#: `Integrity.Check(a == b, "some text {}", a)`  

There are minor consession made to language conventions. For example, in c# the function names are capitalised.

## Delayed and safe string building
The components of the message string are only used if the integrity check fails. This means that the execution time of the check is minimised. The building of the string is guarenteed not to error.

## Compact format
If you did not use Integrity (or similar), and wrote the check out by hand, it would look something like:
```
if(a != b):
	raise ValueError("some text " + str(a))
```
note that there is potentional for the creation of the message within ValueError(~) to cause a problem, if, for example, the developer forgot to put str() around an int.



