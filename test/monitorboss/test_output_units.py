import json
import sys
import textwrap

import pytest

from frozendict import frozendict

from pyddc.vcp_codes import VCPCodes, InputSourceNames, ColorPresetNames
from test.pyddc.vcp_dummy import DummyVCP as VCP
import pyddc
pyddc.VCP = VCP
from monitorboss import indentation, info, output


mdata0 = info.MonitorData(42, ())
mdata0json = json.dumps(mdata0.serialize())
mdata1 = info.MonitorData(43, ())
mdata1json = json.dumps(mdata1.serialize())
feature1 = info.FeatureData("", 42, ())
feature1json = json.dumps(feature1.serialize())
feature2 = info.FeatureData("", 84, ())
feature2json = json.dumps(feature2.serialize())
feature3 = info.FeatureData("", VCPCodes.input_source.value, ())
feature3json = json.dumps(feature3.serialize())
feature4 = info.FeatureData("", VCPCodes.image_color_preset.value, ())
feature4json = json.dumps(feature4.serialize())
value0 = info.ValueData(12, "", ())
value0json = json.dumps(value0.serialize())
value1 = info.ValueData(34, "", ())
value1json = json.dumps(value1.serialize())
value2 = info.ValueData(InputSourceNames.hdmi2.value, "", ())
value2json = json.dumps(value2.serialize())
value3 = info.ValueData(ColorPresetNames.ct5000k.value, "", ())
value3json = json.dumps(value3.serialize())
attributes = frozendict({"model": "CAF3", "foo": "bar", "baz": "qux", "type": "LCD"})
cmds = frozendict({"cmds_0": (feature1, feature2, feature3), "cmds_1": (feature1, feature2, feature4)})
vcps = frozendict({"vcp_0": frozendict({feature1: (value0, value1), feature2: (value0, value1), feature3: (value2,)}),
                   "vcp_1": frozendict({feature1: (value0, value1), feature2: (value0, value1), feature4: (value3,)})})
errata = frozendict({"": ("foo", "bar"), "baz": ("qux", "corge")})
caps = info.CapabilityData(attributes, cmds, vcps, errata)
capsjson = json.dumps(caps.serialize())


def test_list_mons_json():
    expected = json.dumps({"list": [{"monitor": mdata0.serialize()}, {"monitor": mdata1.serialize()}]})
    assert output.list_mons_output([mdata0, mdata1], True) == expected


def test_list_mons_human():
    expected = f"{mdata0}\n{mdata1}"
    assert output.list_mons_output([mdata0, mdata1], False) == expected


def test_get_feature_json():
    expected = json.dumps({"get": {"feature": feature1.serialize(), "values": [{"monitor": mdata0.serialize(), "value": value0.serialize()}, {"monitor": mdata1.serialize(), "value": value1.serialize(), "max_value": 100}]}})
    assert output.get_feature_output(feature1, [(mdata0, value0, None), (mdata1, value1, 100)], True) == expected


def test_get_feature_human():
    expected = f"{feature1} for {mdata0} is {value0}\n{feature1} for {mdata1} is {value1} (Maximum: 100)"
    assert output.get_feature_output(feature1, [(mdata0, value0, None), (mdata1, value1, 100)], False) == expected


def test_caps_raw_json():
    expected = json.dumps({"caps": {"type": "raw", "monitor": mdata0.serialize(), "data": "foo"}})
    assert output.caps_raw_output(mdata0, "foo", True) == expected


def test_caps_raw_human():
    expected = f"Capability string for {mdata0}:\nfoo"
    assert output.caps_raw_output(mdata0, "foo", False) == expected


def test_caps_full_json():
    expected = json.dumps({"caps": {"type": "full", "monitor": mdata0.serialize(), "data": caps.serialize()}})
    assert output.caps_full_output(mdata0, caps, True) == expected


def test_caps_full_human():
    expected = f"{mdata0}:\n{textwrap.indent(str(caps), indentation)}"
    assert output.caps_full_output(mdata0, caps, False) == expected


def test_extract_caps_summary_data():
    expected = ({'model': 'CAF3', 'type': 'LCD'}, {'vcp_0': {feature3: (value2,)}, 'vcp_1': {feature4: (value3,)}})
    assert output.extract_caps_summary_data(caps) == expected


def test_caps_summary_json():
    expected = json.dumps({"caps": {"type": "summary", "monitor": mdata0.serialize(),
                                    "data": {"model": "CAF3", "type": "LCD",
                                             "vcps": {"vcp_0": [{"feature": feature3.serialize(), "params": [value2.serialize()]}],
                                                      "vcp_1": [{"feature": feature4.serialize(), "params": [value3.serialize()]}]}}}})
    assert output.caps_summary_output(mdata0, caps, True) == expected


def test_caps_summary_human():
    expected = f'{mdata0} - model: CAF3, type: LCD\nvcp_0:\n{indentation}* {feature3}: {value2}\nvcp_1:\n{indentation}* {feature4}: {value3}\n'
    assert output.caps_summary_output(mdata0, caps, False) == expected
