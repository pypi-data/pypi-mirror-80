# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-marshmallow-pyfields>
#
# License: 3-clause BSD, <https://github.com/smarie/python-marshmallow-pyfields/blob/master/LICENSE>
import marshmallow
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

    # check that the schema is correct
    city_schema = CitySchema()
    assert city_schema.fields.keys() == {'name', 'buildings'}

    name_schema = city_schema.fields['name']
    assert isinstance(name_schema, marshmallow.fields.String)

    # this is surprising but actually the behaviour of marshmallow_dataclass,
    # see https://github.com/lovasoa/marshmallow_dataclass/issues/102
    assert not name_schema.required
    assert name_schema.default is None
    assert name_schema.allow_none

    buildings_schema = city_schema.fields['buildings']
    assert isinstance(buildings_schema, marshmallow.fields.List)
    assert not buildings_schema.required
    assert buildings_schema.default == []
    assert not buildings_schema.allow_none

    #
    city = city_schema.load(
        {"name": "Paris", "buildings": [{"name": "Eiffel Tower", "height": 324}]}
    )
    assert repr(city) == "City(name='Paris', buildings=[Building(height=324.0, name='Eiffel Tower')])"

    city_dict = city_schema.dump(city)
    assert city_dict == {'name': 'Paris', 'buildings': [{'name': 'Eiffel Tower', 'height': 324.0}]}

    cities = CitySchema(many=True).load([
        {"name": "Paris"},
        {"name": "Paris", "buildings": [{"name": "Eiffel Tower", "height": 324}]},
        {}
    ])
    assert len(cities) == 3
    assert cities[0].name == cities[1].name
    assert cities[0].buildings == []
    # the strange but current behaviour of marshmallow_dataclass is to think that Optional[] type means default=None
    assert cities[2].name is None
