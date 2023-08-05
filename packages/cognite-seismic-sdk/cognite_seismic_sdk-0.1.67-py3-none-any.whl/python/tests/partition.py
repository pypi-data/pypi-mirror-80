import pytest
from cognite.seismic import CogniteSeismicClient


def get_client() -> CogniteSeismicClient:
    return CogniteSeismicClient(api_key=None, base_url="localhost", port=50052, insecure=True)


def test_search_partitions():
    client = get_client()
    assert len(list(client.partition.search(name="test"))) > 0


def test_list_partitions():
    client = get_client()
    assert len(list(client.partition.list())) > 0
