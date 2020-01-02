from .ansible_test_infra_case import AnsibleTestInfraCase


class TestUsbguard(AnsibleTestInfraCase):

    def test_usbguard_is_installed(self):
        usbguard = self.edge_station.package("usbguard")
        assert usbguard.is_installed

    def test_usbguard_service_is_running(self):
        usbguard = self.edge_station.service("usbguard")
        assert usbguard.is_running
        assert usbguard.is_enabled

    def test_usbguard_conf_file(self):
        rule = self.edge_station.file("/etc/usbguard/aivi-rules.conf")
        conf = self.edge_station.file("/etc/usbguard/usbguard-daemon.conf")

        assert rule.exists
        assert conf.exists
        assert rule.user == 'root'
        assert conf.user == 'root'
        assert rule.mode == 0o600
        assert conf.mode == 0o600
