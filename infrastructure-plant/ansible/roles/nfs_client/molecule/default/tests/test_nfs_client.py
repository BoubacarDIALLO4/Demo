from testinfra.modules.service import Service

from .ansible_test_infra_case import AnsibleTestInfraCase


class TestNfsServer(AnsibleTestInfraCase):

    def test_rpcbind_service_should_be_enabled_and_running(self):
        # Given
        rpcbind: Service = self.central_station.service('rpcbind')

        # Then
        assert rpcbind.is_enabled
        assert rpcbind.is_running

    def test_nfs_client_service_should_be_enabled(self):
        # Given
        nfs: Service = self.central_station.service('nfs-client.target')

        # Then
        assert nfs.is_enabled

    def test_nfs_service_should_be_active(self):
        assert self.central_station.run_test('systemctl is-active nfs-client.target')

    def test_result_directory_is_mounted(self):
        # Given
        expected_options = ['hard', 'vers=4.1', 'rw', 'relatime']

        # Then
        for result_dir_type in ['buffer', 'archive']:
            mounted_dir = self.central_station.mount_point(f'/storage/{result_dir_type}/edge_station')
            mount_options = mounted_dir.options
            expected_device = f'192.168.10.20:/storage/aivi/{result_dir_type}'
            with self.subTest():
                assert mounted_dir.exists
                assert mounted_dir.device == expected_device
                assert all([option in mount_options for option in expected_options])

    def test_result_directory_has_expected_owner_and_permissions(self):
        # Given
        expected_dir_uid = 1002
        expected_dir_gid = 1100
        expected_dir_permissions = 0o775

        # Then
        for result_dir_type in ['buffer', 'archive']:
            mounted_dir = self.central_station.file(f'/storage/{result_dir_type}/edge_station')
            with self.subTest():
                assert mounted_dir.exists
                assert mounted_dir.is_directory
                assert mounted_dir.uid == expected_dir_uid
                assert mounted_dir.gid == expected_dir_gid
                assert mounted_dir.mode == expected_dir_permissions
