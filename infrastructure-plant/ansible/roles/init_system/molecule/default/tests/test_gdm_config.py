from .ansible_test_infra_case import AnsibleTestInfraCase


class TestService(AnsibleTestInfraCase):

    def test_check_config_file(self):
        # Given
        config_file = self.edge_station.file("/etc/gdm/custom.conf")
        expected_str = ["AutomaticLoginEnable=True", "AutomaticLogin=aivi"]

        # Then
        assert config_file.exists
        assert config_file.is_file
        assert config_file.user == "root"
        assert all(string in config_file.content_string for string in expected_str)
