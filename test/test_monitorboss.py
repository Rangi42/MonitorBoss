import pytest

from monitorboss import MonitorBossError
from pyddc import VCP
from monitorboss.impl import list_monitors, __get_monitor


def test_list_monitors():
    vcps = list_monitors()
    assert len(vcps) == 3
    for vcp in vcps:
        assert isinstance(vcp, VCP)


def test_get_monitor():
    with pytest.raises(MonitorBossError):
        __get_monitor(4)

    # TODO: is it desirable behavior that negative indexes work?
    # with pytest.raises(MonitorBossError):
    #     print(__get_monitor(-1))

    assert isinstance(__get_monitor(0), VCP)



# TODO: do we need to actually test any of these functions?
# get_vcp_capabilities
# get_attribute
