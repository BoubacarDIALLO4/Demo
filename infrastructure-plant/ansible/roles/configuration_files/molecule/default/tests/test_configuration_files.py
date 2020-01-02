from .ansible_test_infra_case import AnsibleTestInfraCase


class TestConfigurationFiles(AnsibleTestInfraCase):

    def test_configuration_files_are_put_in_configuration_directory(self):
        # Given
        barcode_seat_mapping_file = self.edge_station.file("/etc/aivi/inference/barcode_seat_mapping.csv")
        configuration_file = self.edge_station.file("/etc/aivi/inference/configuration.json")
        pipeline_file = self.edge_station.file("/etc/aivi/inference/pipeline.json")
        seat_templates_file = self.edge_station.file("/etc/aivi/inference/seat_templates.json")
        wrinkles_threshold_file = self.edge_station.file("/etc/aivi/inference/wrinkles_threshold.json")

        # Then
        assert barcode_seat_mapping_file.exists
        assert configuration_file.exists
        assert pipeline_file.exists
        assert seat_templates_file.exists
        assert wrinkles_threshold_file.exists

    def test_configuration_files_desync_are_put_in_configuration_directory(self):
        configuration_file = self.edge_station.file("/etc/aivi/desync1/configuration.json")
        pipeline_file = self.edge_station.file("/etc/aivi/desync1/pipeline.json")
        aivi_desync2 = self.edge_station.file("/etc/aivi/desync2")
        aivi_desync3 = self.edge_station.file("/etc/aivi/desync3")

        assert configuration_file.exists
        assert pipeline_file.exists
        assert aivi_desync2.exists
        assert aivi_desync3.exists
