from testinfra.modules.file import File

from .ansible_test_infra_case import AnsibleTestInfraCase


class TestFilesTree(AnsibleTestInfraCase):

    def test_directories_user_and_permissions(self):
        # Given
        params_list = [
            ('/opt/aivi', 'aivid', 'aivid', 0o755),
            ('/opt/aivi/bin', 'aivid', 'aivid', 0o755),
            ('/etc/aivi', 'aivid', 'aivid', 0o755),
            ('/storage/aivi', 'aivid', 'aivi_storage', 0o775),
            ('/storage/aivi/buffer', 'aivid', 'aivi_storage', 0o775),
            ('/storage/aivi/archive', 'aivid', 'aivi_storage', 0o775),
        ]
        # Then
        for directory_path, user, group, mode in params_list:
            directory = self.edge_station.file(directory_path)
            with self.subTest():
                _assert_directory_user_and_permissions(directory, user, group, mode)


def _assert_directory_user_and_permissions(directory: File, owner: str, group: str, mode: int):
    assert directory.exists
    assert directory.is_directory
    assert directory.user == owner
    assert directory.group == group
    assert directory.mode == mode
