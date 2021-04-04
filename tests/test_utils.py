from unittest import TestCase
from utils import *


class Test(TestCase):
    def test_countries_of(self):
        for cont in ["African", "Asian", "European",
                     "North_American", "Oceanian", "South_American"]:
            print(countries_of(cont))

    def test_iso_alpha_codes_of(self):
        for cont in ["AF", "AS", "EU",
                     "NAM", "OC", "SA"]:
            print(iso_alpha_codes_of(cont))

    def test_get_iso_alpha(self):
        for reg in ["Asia", "China", "EU15", "NorthAmerica", "US"]:
            print(get_iso_alpha(reg))

    def test_entity_to_entity_data(self):
        for i in REGIONS:
            for j in REGIONS:
                if i != j:
                    print(entity_to_entity_data(i, j).head())

    def test_supplier_number(self):
        print(supplier_number())
