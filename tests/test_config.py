import pytest
from net_report import config
from tests import configs

def test_valid_config():
    assert config.valid_config(configs.valid)
    assert config.verify_config(configs.valid) == []

missing = {
    "missing_groups": configs.missing_groups,
    "missing_hosts": configs.missing_hosts,
    "missing_settings": configs.missing_settings,
}
@pytest.mark.parametrize("config_in", missing.values(), ids = missing.keys())
def test_missing_sections(config_in):
    assert not config.valid_config(config_in)

def test_extra_section():
    assert not config.valid_config(configs.extra_section)

@pytest.mark.parametrize(
    ("config_in", "return_on_first", "expected"),
    (
        pytest.param(configs.groups_not_list, False, 1, id="groups not list"),
        pytest.param(configs.group_not_str, False, 1, id="group not string"),
    )
)
def test_verify_groups(config_in, return_on_first, expected):
    assert len(config._verify_groups(config_in["groups"], return_on_first)) == expected

@pytest.mark.parametrize(
    ("config_in", "return_on_first", "expected"),
    (
        pytest.param(configs.hosts_not_list, False, 1, id="hosts not list"),
        pytest.param(configs.host_missing_fields, False, 2, id="multiple hosts missing fields"),
        pytest.param(configs.host_missing_fields, True, 1, id="first host missing fields"),
    )
)
def test_verify_hosts(config_in, return_on_first, expected):
    assert len(config._verify_hosts(config_in["hosts"], return_on_first)) == expected

@pytest.mark.parametrize(
    ("config_in", "return_on_first", "expected"),
    (
        pytest.param(configs.settings_not_list, False, 1, id="settings not list"),
        pytest.param(configs.settings_wrong_fields, False, 1, id="wrong settings fields"),
    )
)
def test_verify_settings(config_in, return_on_first, expected):
    assert len(config._verify_settings(config_in["settings"], return_on_first)) == expected

