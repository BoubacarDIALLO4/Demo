from .ansible_test_infra_case import AnsibleTestInfraCase


class TestLocaleLanguage(AnsibleTestInfraCase):

    def test_language_is_set_to_a_valid_one_such_as_canadian(self):
        # Given
        locale_configuration = self.edge_station.file('/etc/locale.conf').content_string

        # Then
        assert "LANG=en_US.UTF-8" in locale_configuration
        assert "LC_ALL=en_US.UTF-8" in locale_configuration
