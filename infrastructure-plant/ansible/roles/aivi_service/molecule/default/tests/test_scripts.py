from .ansible_test_infra_case import AnsibleTestInfraCase


class TestScripts(AnsibleTestInfraCase):

    def test_aivi_script_starts_aivi_and_firefox(self):
        """aivi service should be running before and after this test"""
        # Given
        aivi = self.edge_station.service("aivi")
        firefox = self.edge_station.service("firefox")
        self.edge_station.run("sudo systemctl stop aivi.service")
        self.edge_station.run("sudo systemctl stop firefox.service")
        assert not aivi.is_running
        assert not firefox.is_running

        with self.edge_station.sudo("aivi"):
            # When
            cmd = self.edge_station.run("/bin/bash /opt/aivi/bin/aivi.sh")

            # Then
            assert cmd.rc == 0
            assert aivi.is_running

    def test_basler_configurator_script_stops_aivi_inference_and_starts_firefox(self):
        """aivi service should be running before and after this test"""
        # Given
        aivi_inference = self.edge_station.service("aivi-inference")
        basler_configurator = self.edge_station.service("basler-configurator")
        self.edge_station.run("sudo systemctl stop firefox.service")
        assert aivi_inference.is_running
        assert not basler_configurator.is_running

        with self.edge_station.sudo("aivi"):
            # When
            cmd = self.edge_station.run("/bin/bash /opt/aivi/bin/basler-configurator.sh")

            # Then
            assert cmd.rc == 0
            assert not aivi_inference.is_running
            assert basler_configurator.is_running

            # Back to initial situation
            cmd = self.edge_station.run("/bin/bash /opt/aivi/bin/aivi.sh")  # Stop basler-configurator and start aivi
            assert cmd.rc == 0
            assert aivi_inference.is_running
