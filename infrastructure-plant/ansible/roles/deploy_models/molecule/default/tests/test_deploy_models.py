from testinfra.modules.file import File

from .ansible_test_infra_case import AnsibleTestInfraCase


class TestConfigurationFiles(AnsibleTestInfraCase):

    def test_model_files_are_put_in_model_directory_with_correct_permissions(self):
        # Given
        model1_file = self.edge_station.file("/opt/aivi/models/test_model1.pb")
        model2_file = self.edge_station.file("/opt/aivi/models/test_model2.csv")

        # Then
        _assert_file_user_and_permissions(model1_file, "aivid", "aivid", 0o644)
        _assert_file_user_and_permissions(model2_file, "aivid", "aivid", 0o644)


def _assert_file_user_and_permissions(file: File, owner: str, group: str, mode: int):
    assert file.exists
    assert file.is_file
    assert file.user == owner
    assert file.group == group
    assert file.mode == mode
