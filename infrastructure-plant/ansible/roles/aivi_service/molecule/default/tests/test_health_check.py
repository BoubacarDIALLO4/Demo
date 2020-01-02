
from .ansible_test_infra_case import AnsibleTestInfraCase


class TestHealthCheck(AnsibleTestInfraCase):

    def test_health_check_is_OK(self):
        # Given
        response = self.edge_station.ansible("uri", "url=http://localhost:5000/aivi/health method=GET", check=False)

        # Then
        assert response['status'] == 200
