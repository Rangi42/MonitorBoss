from pathlib import Path

import pytest

from monitorboss import config
from monitorboss.config import Config

pytest_plugins = "pytester"  # used by the functions in test_config_units.py

TEST_TOML_CONTENTS = """
[monitor_names]
0 = "foo"
1 = ["bar", "baz"]
# 2 has no alias

[feature_aliases]
16 = ['lum', 'luminance', 'brightness']
18 = ['cnt', 'contrast']
20 = ['clr', 'color', 'clrpreset']
96 = ['src', 'source', 'input']
214 = ['pwr', 'power', 'powermode']

[value_aliases.input_source]
27 = ["usbc", "usb-c"] # 27 seems to be the "standard non-standard" ID for USB-C among manufacturers
17 = "hdmi"

[value_aliases.image_luminance]
25 = "night"
75 = ["day", "bright"]

[settings]
wait_get = 0
wait_set = 0
wait_internal = 0""".strip()


@pytest.fixture(scope='module')
def test_conf_file(tmp_path_factory) -> Path:
    file = tmp_path_factory.mktemp("conf") / "mb_conf.toml"
    file.write_text(TEST_TOML_CONTENTS)
    return file


@pytest.fixture(scope='module')
def test_cfg(test_conf_file) -> Config:
    return config.get_config(test_conf_file.as_posix())
