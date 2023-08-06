# marshmallow-pyfields

*Automatic generation of `marshmallow` schemas from classes using `pyfields`.*

[![Python versions](https://img.shields.io/pypi/pyversions/marshmallow-pyfields.svg)](https://pypi.python.org/pypi/marshmallow-pyfields/) [![Build Status](https://travis-ci.org/smarie/python-marshmallow-pyfields.svg?branch=master)](https://travis-ci.org/smarie/python-marshmallow-pyfields) [![Tests Status](https://smarie.github.io/python-marshmallow-pyfields/junit/junit-badge.svg?dummy=8484744)](https://smarie.github.io/python-marshmallow-pyfields/junit/report.html) [![codecov](https://codecov.io/gh/smarie/python-marshmallow-pyfields/branch/master/graph/badge.svg)](https://codecov.io/gh/smarie/python-marshmallow-pyfields)

[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://smarie.github.io/python-marshmallow-pyfields/) [![PyPI](https://img.shields.io/pypi/v/marshmallow-pyfields.svg)](https://pypi.python.org/pypi/marshmallow-pyfields/) [![Downloads](https://pepy.tech/badge/marshmallow-pyfields)](https://pepy.tech/project/marshmallow-pyfields) [![Downloads per week](https://pepy.tech/badge/marshmallow-pyfields/week)](https://pepy.tech/project/marshmallow-pyfields) [![GitHub stars](https://img.shields.io/github/stars/smarie/python-marshmallow-pyfields.svg)](https://github.com/smarie/python-marshmallow-pyfields/stargazers)


`marshmallow-pyfields` extends [`marshmallow-dataclass`](https://github.com/lovasoa/marshmallow_dataclass) to help you generate marshmallow schemas for your classes using `pyfields`. 


## Installing

```bash
> pip install marshmallow-pyfields
```

## Usage

Usage is the same than `marshmallow-dataclass`:

```python
from pyfields import field, autoclass
from typing import List, Optional

from marshmallow_pyfields import get_schema

@autoclass
class Building:
    # field metadata is used to instantiate the marshmallow field
    height: float = field(validators={"should be positive": lambda x: x >= 0})
    name: str = "anonymous"

@autoclass
class City:
    name: Optional[str]
    buildings: List[Building] = []

CitySchema = get_schema(City)

city = CitySchema().load(
    {"name": "Paris", "buildings": [{"name": "Eiffel Tower", "height": 324}]}
)
assert repr(city) == "City(name='Paris', buildings=[Building(height=324.0, name='Eiffel Tower')])"

city_dict = CitySchema().dump(city)
assert city_dict == {'name': 'Paris', 'buildings': [{'name': 'Eiffel Tower', 'height': 324.0}]}
```


## Main features / benefits

 * Generate `marshmallow` schemas from classes using `pyfields`, so as to benefit from the whole `marshmallow` ecosystem.

## See Also

 - [marshmallow](https://marshmallow.readthedocs.io/en/stable/) of course
 - [marshmallow-dataclass](https://github.com/lovasoa/marshmallow_dataclass)
 - the great [marshmallow ecosystem](https://github.com/marshmallow-code/marshmallow/wiki/Ecosystem)

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/smarie/python-marshmallow-pyfields](https://github.com/smarie/python-marshmallow-pyfields)
