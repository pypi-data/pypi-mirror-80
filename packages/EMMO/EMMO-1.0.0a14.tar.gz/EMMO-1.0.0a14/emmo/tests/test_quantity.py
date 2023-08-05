#!/usr/bin/env python3
import os
import sys

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import World  # noqa: E402, F401

import owlready2  # noqa: E402, F401
from emmo.quantity import (
    isquantity, get_units, Quantity, physics_dimension_of_quantity,
    physics_dimension_of_unit)  # noqa: E402, F401


world = World()
emmo = world.get_ontology()
emmo.load()

o = emmo
w = o.world

assert not isquantity(emmo.Item)
assert isquantity(emmo.Length)
#assert set(get_units(emmo.Energy)) == {
#    emmo.Joule, emmo.ElectronVolt, emmo.NewtonMetre}

print(get_units(emmo.Length))
