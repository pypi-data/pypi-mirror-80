import pytest
from zigpy.zdo.types import ZDOCmd

import zigpy_znp.types as t
import zigpy_znp.commands as c

from ..conftest import FORMED_DEVICES

pytestmark = [pytest.mark.timeout(1), pytest.mark.asyncio]


@pytest.mark.parametrize("device", FORMED_DEVICES)
async def test_on_zdo_relays_message_callback(device, make_application, mocker):
    app, znp_server = make_application(server_cls=device)
    await app.startup(auto_form=False)

    device = mocker.Mock()
    mocker.patch.object(app, "get_device", return_value=device)

    znp_server.send(c.ZDO.SrcRtgInd.Callback(DstAddr=0x1234, Relays=[0x5678, 0xABCD]))
    assert device.relays == [0x5678, 0xABCD]

    await app.shutdown()


@pytest.mark.parametrize("device", FORMED_DEVICES)
async def test_on_zdo_device_announce(device, make_application, mocker):
    app, znp_server = make_application(server_cls=device)
    await app.startup(auto_form=False)

    mocker.patch.object(app, "handle_message")

    device = app.add_device(ieee=t.EUI64(range(8)), nwk=0xFA9E)

    znp_server.send(
        c.ZDO.EndDeviceAnnceInd.Callback(
            Src=0x0001,
            NWK=device.nwk,
            IEEE=device.ieee,
            Capabilities=c.zdo.MACCapabilities.Router,
        )
    )

    app.handle_message.called_once_with(cluster=ZDOCmd.Device_annce)

    await app.shutdown()


@pytest.mark.parametrize("device", FORMED_DEVICES)
async def test_on_zdo_device_leave_callback(device, make_application, mocker):
    app, znp_server = make_application(server_cls=device)
    await app.startup(auto_form=False)

    mocker.patch.object(app, "handle_leave")

    nwk = 0x1234
    ieee = t.EUI64(range(8))

    znp_server.send(
        c.ZDO.LeaveInd.Callback(
            NWK=nwk, IEEE=ieee, Request=False, Remove=False, Rejoin=False
        )
    )
    app.handle_leave.assert_called_once_with(nwk=nwk, ieee=ieee)

    await app.shutdown()


@pytest.mark.parametrize("device", FORMED_DEVICES)
async def test_on_af_message_callback(device, make_application, mocker):
    app, znp_server = make_application(server_cls=device)
    await app.startup(auto_form=False)

    device = mocker.Mock()
    mocker.patch.object(
        app,
        "get_device",
        side_effect=[device, device, device, KeyError("No such device")],
    )
    mocker.patch.object(app, "handle_message")

    af_message = c.AF.IncomingMsg.Callback(
        GroupId=1,
        ClusterId=2,
        SrcAddr=0xABCD,
        SrcEndpoint=4,
        DstEndpoint=1,  # ZHA endpoint
        WasBroadcast=False,
        LQI=19,
        SecurityUse=False,
        TimeStamp=0,
        TSN=0,
        Data=b"test",
        MacSrcAddr=0x0000,
        MsgResultRadius=1,
    )

    # Normal message
    znp_server.send(af_message)
    app.get_device.assert_called_once_with(nwk=0xABCD)
    device.radio_details.assert_called_once_with(lqi=19, rssi=None)
    app.handle_message.assert_called_once_with(
        sender=device, profile=260, cluster=2, src_ep=4, dst_ep=1, message=b"test"
    )

    # ZLL message
    device.reset_mock()
    app.handle_message.reset_mock()
    app.get_device.reset_mock()

    znp_server.send(af_message.replace(DstEndpoint=2))
    app.get_device.assert_called_once_with(nwk=0xABCD)
    device.radio_details.assert_called_once_with(lqi=19, rssi=None)
    app.handle_message.assert_called_once_with(
        sender=device, profile=49246, cluster=2, src_ep=4, dst_ep=2, message=b"test"
    )

    # Message on an unknown endpoint (is this possible?)
    device.reset_mock()
    app.handle_message.reset_mock()
    app.get_device.reset_mock()

    znp_server.send(af_message.replace(DstEndpoint=3))
    app.get_device.assert_called_once_with(nwk=0xABCD)
    device.radio_details.assert_called_once_with(lqi=19, rssi=None)
    app.handle_message.assert_called_once_with(
        sender=device, profile=260, cluster=2, src_ep=4, dst_ep=3, message=b"test"
    )

    # Message from an unknown device
    device.reset_mock()
    app.handle_message.reset_mock()
    app.get_device.reset_mock()

    znp_server.send(af_message)
    app.get_device.assert_called_once_with(nwk=0xABCD)
    assert device.radio_details.call_count == 0
    assert app.handle_message.call_count == 0

    await app.shutdown()
