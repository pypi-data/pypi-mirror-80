import csv
import io

from afancontrol.exec import exec_shell_command
from afancontrol.pwmfan.base import BaseFanSpeed, FanValue

# TODO maybe switch to `python3-pyghmi`? although it looks like the current version
# in Stretch is broken in py3: https://opendev.org/x/pyghmi/commit/2e12f5ce15e11e46a1c11ee3b00b94cb8bd7feb9  # noqa


class FreeIPMIFanSpeed(BaseFanSpeed):
    __slots__ = ("_name", "_ipmi_sensors_bin", "_ipmi_sensors_extra_args")

    def __init__(
        self, name: str, *, ipmi_sensors_bin="ipmi-sensors", ipmi_sensors_extra_args=""
    ) -> None:
        self._name = name
        self._ipmi_sensors_bin = ipmi_sensors_bin
        self._ipmi_sensors_extra_args = ipmi_sensors_extra_args

    def get_speed(self) -> FanValue:
        out = self._call_ipmi_sensors()
        reader = csv.DictReader(io.StringIO(out))
        for row in reader:
            if row["Name"] == self._name:
                assert row["Units"] == "RPM"
                # assert row["Event"] == "'OK'"
                return FanValue(int(float(row["Reading"])))
        raise RuntimeError(
            "ipmi-sensors output doesn't contain %r fan:\n%s" % (self._name, out)
        )

    def _call_ipmi_sensors(self) -> str:
        shell_command = "%s %s --sensor-types Fan --comma-separated-output" % (
            self._ipmi_sensors_bin,
            self._ipmi_sensors_extra_args,
        )
        return exec_shell_command(shell_command, timeout=2)
