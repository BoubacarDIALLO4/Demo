from .ansible_test_infra_case import AnsibleTestInfraCase


class TestFirewalld(AnsibleTestInfraCase):

    def test_nfs_is_allowed_by_firewall(self):
        # Given
        list_services_command = self.edge_station.check_output("sudo firewall-cmd --list-services")
        allowed_services = list_services_command.split(' ')

        # Then
        assert 'nfs' in allowed_services
