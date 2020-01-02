from .ansible_test_infra_case import AnsibleTestInfraCase


class TestPylon(AnsibleTestInfraCase):

    def test_pylon_was_extracted_on_the_edge_station_for_aivid(self):
        # Given
        aivi_pylon_folder = self.edge_station.file('/opt/pylon5/')

        # Then
        assert aivi_pylon_folder.exists
        assert aivi_pylon_folder.is_directory
        assert aivi_pylon_folder.user == 'aivid'
        assert aivi_pylon_folder.group == 'aivid'
