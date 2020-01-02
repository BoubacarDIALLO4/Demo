import time

from testinfra.modules.service import Service

from .ansible_test_infra_case import AnsibleTestInfraCase


class TestNfsServer(AnsibleTestInfraCase):

    def test_images_folder_exports_access_should_be_set(self):
        # Given
        export_file = self.edge_station.file('/etc/exports')
        buffer_directory_to_export = '/storage/aivi/buffer'
        archive_directory_to_export = '/storage/aivi/archive'
        options = '(rw,sync,insecure,all_squash,anonuid=1010,anongid=1100)'

        # Then
        assert buffer_directory_to_export in export_file.content_string
        assert archive_directory_to_export in export_file.content_string
        assert options in export_file.content_string

    def test_nfs_service_should_be_enabled(self):
        # Given
        nfs: Service = self.edge_station.service('nfs')

        # Then
        assert nfs.is_enabled

    def test_nfs_service_should_be_active(self):
        time.sleep(3)  # Wait for service to start correctly
        assert self.edge_station.run_test('systemctl is-active nfs-server')

    def test_rpcbind_service_should_be_enabled_and_running(self):
        # Given
        rpcbind: Service = self.edge_station.service('rpcbind')

        # Then
        assert rpcbind.is_enabled
        assert rpcbind.is_running

    def test_showmount_list_exported_dir(self):
        # Given
        expected_output = '/storage/aivi/archive 192.168.10.10\n/storage/aivi/buffer  192.168.10.10'
        showmount_str = self.edge_station.check_output('/usr/sbin/showmount -e --no-headers')

        # Then
        assert showmount_str == expected_output
