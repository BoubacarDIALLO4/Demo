from .ansible_test_infra_case import AnsibleTestInfraCase


class TestAiviUsers(AnsibleTestInfraCase):

    def test_aivi_user_is_properly_setup(self):
        # Given
        aivi_user = self.edge_station.user("aivi")
        default_password = "!!"

        # Then
        assert aivi_user.exists
        assert aivi_user.password != default_password
        assert aivi_user.home == "/home/aivi"

    def test_aivi_daemon_user_exists(self):
        # Given
        aivi_daemon_user = self.edge_station.user("aivid")
        expected_group = "aivi_storage"

        # Then
        assert aivi_daemon_user.exists
        assert not self.edge_station.file(aivi_daemon_user.home).exists
        assert expected_group in aivi_daemon_user.groups

    def test_nfs_user_exists(self):
        # Given
        nfs_user = self.edge_station.user("nfsuser")
        expected_uid = 1010
        expected_group = "aivi_storage"

        # Then
        assert nfs_user.exists
        assert nfs_user.uid == expected_uid
        assert expected_group in nfs_user.groups
        assert not self.edge_station.file(nfs_user.home).exists

    def test_storage_group_exists(self):
        # Given
        group = self.edge_station.group("aivi_storage")
        expected_gid = 1100

        # Then
        assert group.exists
        assert group.gid == expected_gid
