from .ansible_test_infra_case import AnsibleTestInfraCase

import yaml


class TestArtifact(AnsibleTestInfraCase):
    def setUp(self):
        # molecule test root dir =  infrastructure/ansible/roles/extract_archives/molecule/default
        self.app_version = yaml.load(open('../../defaults/main.yml', 'r').read()).get('app_version')

    def test_artifact_was_extracted_on_the_edge_station_for_aivid(self):
        # Given
        aivi_version_app_directory = self.edge_station.file(f'/opt/aivi/{self.app_version}/')

        # Then
        assert aivi_version_app_directory.exists
        assert aivi_version_app_directory.is_directory
        assert aivi_version_app_directory.user == 'aivid'
        assert aivi_version_app_directory.group == 'aivid'

    def test_aivi_current_directory_has_been_updated_with_new_version(self):
        # Given
        aivi_current_app_directory = self.edge_station.file(f'/opt/aivi/current/')

        # Then
        assert aivi_current_app_directory.exists
        assert aivi_current_app_directory.is_directory
        assert aivi_current_app_directory.user == 'aivid'
        assert aivi_current_app_directory.group == 'aivid'
