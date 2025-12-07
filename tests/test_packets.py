""" Tests for the packet decoding functionality."""

import pytest

from ooni_bluetooth.packets import Packet, PacketNotify, TemperatureUnit


# 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
# 15 00 0e 00 11 00 0b 00 15 00 55 03 3c 7e a8 04 91 c6 26 00 00 00
# |---| |---| |---| |---| |---|  ^-- battery
#   |     |     |     |     ^-- temp_p2
#   |     |     |     ^-- temp_p1
#   |     |     ^-- ambient_b
#   |     ^-- ambient_a
#   ^-- unknown

# byte_0: 21 | a: 14 b: 17 p1: 11 | p2: 21 Battery: 85%

@pytest.mark.parametrize(
    "data,result",
    [
        (
            "00000e0011000b00150055033c7ea80491c626000000",
            PacketNotify(
                battery=85,
                ambient_a=14,
                ambient_b=17,
                probe_p1=11,
                probe_p2=21,
                probe_p1_connected=False,
                probe_p2_connected=False,
                eco_mode=False,
                temperature_unit=TemperatureUnit.FARENHEIT,
            ),
        ),
        (
            "0000000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=False,
                temperature_unit=TemperatureUnit.FARENHEIT,
                probe_p1_connected=False,
                probe_p2_connected=False,
            ),
        ),
        (
            "0100000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=False,
                temperature_unit=TemperatureUnit.CELCIUS,
                probe_p1_connected=False,
                probe_p2_connected=False,
            ),
        ),
        (
            "8000000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=True,
                temperature_unit=TemperatureUnit.FARENHEIT,
                probe_p1_connected=False,
                probe_p2_connected=False,
            ),
        ),
        (
            "9000000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=True,
                temperature_unit=TemperatureUnit.CELCIUS,
                probe_p1_connected=False,
                probe_p2_connected=False,
            ),
        ),
        (
            "0400000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=False,
                temperature_unit=TemperatureUnit.FARENHEIT,
                probe_p1_connected=True,
                probe_p2_connected=False,
            ),
        ),
        (
            "0800000000000000000000033c7ea80491c626000000",
            PacketNotify(
                battery=0,
                ambient_a=0,
                ambient_b=0,
                probe_p1=0,
                probe_p2=0,
                eco_mode=False,
                temperature_unit=TemperatureUnit.FARENHEIT,
                probe_p1_connected=False,
                probe_p2_connected=True,
            ),
        ),
        # (
        #     "0600000000000000000000033c7ea80491c626000000",
        #     PacketNotify(
        #         battery=0,
        #         ambient_a=0,
        #         ambient_b=0,
        #         probe_p1=0,
        #         probe_p2=0,
        #         eco_mode=False,
        #         temperature_unit=TemperatureUnit.FARENHEIT,
        #         probe_p1_connected=True,
        #         probe_p2_connected=True,
        #     ),
        # ),
    ],
)
def test_decode_packet(data: str, result: Packet):
    packet = PacketNotify.decode(bytes.fromhex(data))
    assert packet == result
