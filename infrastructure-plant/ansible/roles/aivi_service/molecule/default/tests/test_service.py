from time import sleep

from .ansible_test_infra_case import AnsibleTestInfraCase


class TestService(AnsibleTestInfraCase):

    def test_aivi_unit_is_a_service_unit_file(self):
        # Given
        aivi_unit_file = self.edge_station.file("/etc/systemd/system/aivi.service")
        expected_service_file_sections = ["[Unit]", "[Service]", "[Install]"]

        # Then
        assert aivi_unit_file.exists
        assert aivi_unit_file.is_file
        assert aivi_unit_file.user == "root"
        assert all(section in aivi_unit_file.content_string for section in expected_service_file_sections)

    def test_aivi_inference_unit_is_a_service_unit_file(self):
        # Given
        aivi_unit_file = self.edge_station.file("/etc/systemd/system/aivi-inference.service")
        expected_service_file_sections = ["[Unit]", "[Service]", "[Install]", "User=aivid", "Group=aivi_storage",
                                          "UMask=0002"]

        # Then
        assert aivi_unit_file.exists
        assert aivi_unit_file.is_file
        assert aivi_unit_file.user == "root"
        assert aivi_unit_file.group == "root"
        assert all(section in aivi_unit_file.content_string for section in expected_service_file_sections)

    def test_desync_aivi_unit_is_a_service_unit_file(self):
        # Given
        desync_aivi_unit_file = self.edge_station.file("/etc/systemd/system/aivi-desync1.service")
        expected_service_file_sections = ["[Unit]", "[Service]", "[Install]"]

        # Then
        assert desync_aivi_unit_file.exists
        assert desync_aivi_unit_file.is_file
        assert desync_aivi_unit_file.user == "root"
        assert all(section in desync_aivi_unit_file.content_string for section in expected_service_file_sections)

    def test_basler_configurator_unit_is_a_service_unit_file(self):
        # Given
        aivi_unit_file = self.edge_station.file("/etc/systemd/system/basler-configurator.service")
        expected_service_file_sections = ["[Unit]", "[Service]", "[Install]"]

        # Then
        assert aivi_unit_file.exists
        assert aivi_unit_file.is_file
        assert aivi_unit_file.user == "root"
        assert all(section in aivi_unit_file.content_string for section in expected_service_file_sections)

    def test_firefox_unit_is_a_service_unit_file(self):
        # Given
        firefox_unit_file = self.edge_station.file("/etc/systemd/system/firefox.service")
        expected_service_file_sections = ["[Unit]", "[Service]", "[Install]"]

        # Then
        assert firefox_unit_file.exists
        assert firefox_unit_file.is_file
        assert firefox_unit_file.user == "root"
        assert all(section in firefox_unit_file.content_string for section in expected_service_file_sections)

    def test_aivi_is_running_and_enabled(self):
        aivi = self.edge_station.service("aivi")
        assert aivi.is_running
        assert aivi.is_enabled

    def test_basler_configurator_is_not_running_and_not_enabled(self):
        basler_configurator = self.edge_station.service("basler-configurator")
        assert not basler_configurator.is_running
        assert not basler_configurator.is_enabled

    def test_aivi_user_can_stop_and_start_aivi_inference(self):
        # aivi should be running before and after this test
        aivi_inference = self.edge_station.service("aivi-inference")
        with self.edge_station.sudo("aivi"):
            # Stop aivi
            cmd = self.edge_station.run("sudo systemctl stop aivi-inference.service")
            assert cmd.rc == 0
            sleep(1)
            assert not aivi_inference.is_running

            # Start aivi
            cmd = self.edge_station.run("sudo systemctl start aivi-inference.service")
            assert cmd.rc == 0
            sleep(1)
            assert aivi_inference.is_running

    def test_aivi_inference_stops_basler_service(self):
        # aivi should be running before and after this test
        aivi_inference = self.edge_station.service("aivi-inference")
        basler = self.edge_station.service("basler-configurator")
        with self.edge_station.sudo("aivi"):
            # Stop aivi
            cmd = self.edge_station.run("sudo systemctl start basler-configurator.service")
            assert cmd.rc == 0
            sleep(1)
            assert basler.is_running

            cmd = self.edge_station.run("sudo systemctl start aivi-inference.service")
            assert cmd.rc == 0
            sleep(1)

            assert aivi_inference.is_running
            assert not basler.is_running

    def test_aivi_user_can_stop_and_start_all_aivi(self):
        # aivi should be running before and after this test
        aivi_inference = self.edge_station.service("aivi-inference")
        aivi_desync = self.edge_station.service("aivi-desync1")
        aivi_desync2 = self.edge_station.service("aivi-desync2")
        with self.edge_station.sudo("aivi"):
            # Stop aivi
            cmd = self.edge_station.run("sudo systemctl stop aivi.service")
            assert cmd.rc == 0
            sleep(1)
            assert not aivi_inference.is_running
            assert not aivi_desync.is_running
            assert not aivi_desync2.is_running

            # Start aivi
            cmd = self.edge_station.run("sudo systemctl start aivi.service")
            assert cmd.rc == 0
            sleep(1)
            assert aivi_inference.is_running
            assert aivi_desync.is_running
            assert aivi_desync2.is_running

    def test_aivi_user_can_stop_and_start_basler_confgurator(self):
        """aivi service should be running before and after this test
        aivi user is not a sudo user, but init_system role has changed the sudoers file to allow aivi to run
        sudo commands to manage aivi and basler-configurator services"""
        basler_configurator = self.edge_station.service("basler-configurator")
        with self.edge_station.sudo("aivi"):
            # Stop aivi and start basler configurator
            cmd = self.edge_station.run("sudo systemctl stop aivi.service")
            assert cmd.rc == 0
            # sleep(1) # time for aivi to stop
            cmd = self.edge_station.run("sudo systemctl start basler-configurator.service")
            assert cmd.rc == 0
            # sleep(1)
            assert basler_configurator.is_running

            # Stop basler configurator and start aivi
            cmd = self.edge_station.run("sudo systemctl stop basler-configurator.service")
            assert cmd.rc == 0
            # sleep(1)
            cmd = self.edge_station.run("sudo systemctl start aivi.service")
            # sleep(1)
            assert cmd.rc == 0
            assert not basler_configurator.is_running
