import os
from unittest import TestCase

import testinfra.utils.ansible_runner


class AnsibleTestInfraCase(TestCase):

    @classmethod
    def setUpClass(cls):
        edge_station_group = "edge_stations"
        cls.edge_station = testinfra.get_host(
            f"ansible://{ edge_station_group }?ansible_inventory={os.environ.get('MOLECULE_INVENTORY_FILE')}")
