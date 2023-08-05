import pathlib

import pytest

from prtg_pyprobe.communication.communication_http_api import PRTGHTTPApi
from prtg_pyprobe.sensors import (
    sensor_ping,
    sensor_port,
    sensor_http,
    sensor_probehealth,
)
from prtg_pyprobe.sensors.helpers import (
    SensorDefinition,
    SensorDefinitionGroup,
    SensorData,
)
from prtg_pyprobe.utils.config import (
    IPDNSValidator,
    PortRangeValidator,
    NotEmptyValidator,
    GUIDValidator,
    BaseIntervalValidator,
    DirectoryWriteableValidator,
    ProbeConfig,
)
from prtg_pyprobe.utils.sensor_loader import load_sensor_modules, create_sensor_objects


@pytest.fixture()
def list_sensor_modules():
    print(pathlib.Path().absolute())
    return load_sensor_modules(sensor_path="../prtg_pyprobe/sensors")


@pytest.fixture()
def list_sensor_objects():
    print(pathlib.Path().absolute())
    return create_sensor_objects(sensor_path="../prtg_pyprobe/sensors")


@pytest.fixture()
def ip_dns_validator():
    return IPDNSValidator()


@pytest.fixture()
def port_range_validator():
    return PortRangeValidator()


@pytest.fixture()
def not_empty_validator():
    return NotEmptyValidator()


@pytest.fixture()
def guid_validator():
    return GUIDValidator()


@pytest.fixture()
def base_interval_validator():
    return BaseIntervalValidator()


@pytest.fixture()
def directory_writeable_validator():
    return DirectoryWriteableValidator()


@pytest.fixture()
def probe_config():
    return ProbeConfig(path="config.yml")


@pytest.fixture()
def probe_config_dict():
    probe_cfg_dict = {
        "disable_ssl_verification": True,
        "log_file_location": "./pyprobe.log",
        "log_level": "INFO",
        "probe_access_key": "miniprobe",
        "probe_access_key_hashed": "cd7b773e2ce4205e9f5907b157f3d26495c5b373",
        "probe_base_interval": "60",
        "probe_gid": "1BFB9273-08D7-43AF-B535-18E4A767BA34",
        "probe_name": "Python Mini Probe",
        "probe_protocol_version": "1",
        "prtg_server_ip_dns": "test.prtg.com",
        "prtg_server_port": "443",
    }
    return probe_cfg_dict


@pytest.fixture()
def prtg_api(probe_config_dict):
    return PRTGHTTPApi(probe_config=probe_config_dict)


@pytest.fixture()
def sensor_definition():
    definition = SensorDefinition(
        name="Testsensor",
        kind="testkind",
        description="This is a Test",
        sensor_help="Test Help",
        tag="testsensor",
        default="1",
    )
    return definition


@pytest.fixture()
def sensor_definition_group():
    definition_group = SensorDefinitionGroup(name="testgroup", caption="TestCaption")
    return definition_group


@pytest.fixture()
def sensor_data():
    sensor_data = SensorData(sensor_id="1234")
    return sensor_data


@pytest.fixture()
def ping_sensor():
    return sensor_ping.Sensor()


@pytest.fixture()
def port_sensor():
    return sensor_port.Sensor()


@pytest.fixture()
def http_sensor():
    return sensor_http.Sensor()


@pytest.fixture()
def probehealth_sensor():
    return sensor_probehealth.Sensor()


@pytest.fixture()
def mock_sensor():
    class MockSensor:
        @staticmethod
        async def mock_work(task_data, q):
            data = {"test": "dict"}
            await q.put(data)

    return MockSensor
