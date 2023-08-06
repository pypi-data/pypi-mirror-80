from enum import Enum#


class SALUSInformation:
    class UpdateState(Enum):
        NO_UPDATE_AVAILABLE = 0
        UPDATE_AVAILABLE = 1

    def __init__(self, api, raw_information):
        self._api = api
        self._raw_information = raw_information

    @property
    def gateway(self):
        return next(filter(lambda x: not x["data"]["DeviceType"] == 300, self._raw_information))

    @property
    def version(self):
        return self.gateway.get("sOTA", {}).get("OTAFirmwareVersion_d", "n/a")

    @property
    def update_state(self) -> UpdateState:
        return self.UpdateState(self.gateway.get("sOTA", {}).get("OTAFirmwareVersion_d", 0))

    @property
    def gateway_raw(self):
        return None

    @property
    def other_devices_raw(self):
        return list(
            filter(
                lambda x: not x["data"]["DeviceType"] == 200 and not x["data"]["DeviceType"] == 300,
                self._raw_information
            )
        )

    def summary(self):
        print(f"Information:")
        print(f"  SW Version         : {self.version}")
        print(f"  State              : {self.update_state}")
