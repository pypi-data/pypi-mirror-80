# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-marshmallow-pyfields>
#
# License: 3-clause BSD, <https://github.com/smarie/python-marshmallow-pyfields/blob/master/LICENSE>

from pyfields import field, autoclass
from typing import List, Optional

from marshmallow_pyfields import get_schema


def test_doc():
    """"""

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
