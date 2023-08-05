# RandKey

This lib can be used to generate random keys that can be used for a password salt, a cdk for your program, or maybe a scurity key for your fist website!

Usage (Python):

```Python
# Import the lib
from RandKey import GenKey

# Generate the key and store it in a variable
GeneratedKey = GenKey(size=32) # The defult size is 64

# Print out the key
print(GeneratedKey)
```
