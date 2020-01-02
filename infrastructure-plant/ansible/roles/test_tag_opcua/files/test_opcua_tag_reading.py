import logging

from aivi.tools.file import load_data_from_json_file
from opcua import Client


def main(server_url, tag_id):
    client = Client(server_url)
    client.connect()

    node = client.get_node(tag_id)
    print(node)
    print(node.get_value())
    client.disconnect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    configuration_filepath = '/etc/aivi/configuration.json'
    data = load_data_from_json_file(configuration_filepath)
    server_url = data['opcua_server_url']
    tag_id = data['opcua_tag_id']
    main(server_url, tag_id)
