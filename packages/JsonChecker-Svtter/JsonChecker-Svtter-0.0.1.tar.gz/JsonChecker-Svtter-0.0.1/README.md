# Json Checker

- STATUS: FINISHED.


Check the python dict type via json file.


## Usage



```python
from json_checker import json_checker

# compare between file and python dict
is_equal, msg = json_checker.check_from_file('example.json', {"a": 1, "b": 2})

# compare between two dicts
is_equal, msg = json_checker.structure({"a": 1, "b": 2}, {"a": 1, "b": 2})

```


## LICENCE

MIT
