import json
import logging
import time

import requests
from .encryptor import IT600Encryptor

from .const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    PRESET_OFF,
    PRESET_PERMANENT_HOLD
)

logger = logging.getLogger("salsusshcpy")


class JSONRPCError(Exception):
    def __init__(self, code, message):
        super().__init__()
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f"JSONRPCError (code: {self.code}, message: {self.message})"


class SHCAPI:
    def __init__(self, controller_ip: str, euid: str):
        self._controller_ip = controller_ip
        self._euid = euid
        self._api_root = f"http://{self._controller_ip}:80/deviceid"
        self._encryptor = IT600Encryptor(euid)

        self._requests_session = requests.Session()
        self._requests_session.headers.update(
            {"Content-Type": "application/json"}
        )
        self._requests_session.verify = False

        import urllib3

        urllib3.disable_warnings()

    @property
    def api_url(self):
        return self._api_root

    def _get_api_result_or_fail(
        self, api_url, expected_type=None, expected_element_type=None, headers=None, timeout=30
    ):
        try:
            result = self._requests_session.get(api_url, headers=headers, timeout=timeout)
            print(result)
            if not result.ok:
                self._process_nok_result(result)

            else:
                if len(result.content) > 0:
                    result = json.loads(result.content)
                    if expected_type is not None:
                        assert result["@type"] == expected_type
                    if expected_element_type is not None:
                        for result_ in result:
                            assert result_["@type"] == expected_element_type

                    return result
                else:
                    return {}
        except requests.exceptions.SSLError as e:
            raise Exception(f"API call returned SSLError: {e}.")

    def _post_api_or_fail(self, api_url, body, timeout=30):
        response = self._requests_session.post(api_url, data=self._encryptor.encrypt(json.dumps(body)), timeout=timeout)
        response_json_string = self._encryptor.decrypt(response.content)
        result = json.loads(response_json_string)

        if not result["status"] == "success":
            self._process_nok_result(response)
        if not result["id"] is None:
            return result["id"]
        else:
            return {}

    def _process_nok_result(self, result):
        print(f"Body: {result.request.body}")
        print(f"Headers: {result.request.headers}")
        print(f"URL: {result.request.url}")

        raise ValueError(
            f"API call returned non-OK result (code {result.status_code})!: {result.content}"
        )

    def get_information(self, wait_seconds=0):
        api_url = f"{self._api_root}/read"
        data = {"requestAttr": "readall"}

        try:
            result = self._post_api_or_fail(api_url, data, wait_seconds + 5)
        except Exception as e:
            logging.error(f"Failed to get information from SALUS controller: {e}")
            return None
        return result

    def long_polling_poll(self, wait_seconds=0):
        api_url = f"{self._api_root}/read"
        data = {"requestAttr": "readall"}

        try:
            result = self._post_api_or_fail(api_url, data, wait_seconds + 5)
            time.sleep(wait_seconds + 5)
        except Exception as e:
            logging.error(f"Failed to start long polling for SALUS Controller: {e}")
            return None
        return result

    async def set_temperature(self, device, celsius: float):
        api_url = f"{self._api_root}/write"
        data = {
                "requestAttr": "write",
                "id": [
                    {
                        "data": device.data,
                        "sIT600TH": {"SetHeatingSetpoint_x100": int((round(celsius * 2) / 2) * 100)}
                    }
                ]
            }

        try:
            result = self._post_api_or_fail(api_url, data)
        except Exception as e:
            logging.error(f"Failed to set temperature for device with id: {device.unique_id}")
            return None
        return result

    async def set_climate_device_mode(self, device, mode: str):
        api_url = f"{self._api_root}/write"
        data = {
                "requestAttr": "write",
                "id": [
                    {
                        "data": device.data,
                        "sIT600TH": {"SetHoldType": 7 if mode == HVAC_MODE_OFF else 0}
                    }
                ]
            }
        try:
            result = self._post_api_or_fail(api_url, data)
        except Exception as e:
            logging.error(f"Failed to set mode for device with id: {device.unique_id}")
            return None
        return result

    async def set_climate_device_preset(self, device, preset: str):
        api_url = f"{self._api_root}/write"
        data = {
                "requestAttr": "write",
                "id": [
                    {
                        "data": device.data,
                        "sIT600TH": {
                            "SetHoldType": 7 if preset == PRESET_OFF else 2 if preset == PRESET_PERMANENT_HOLD else 0
                        }
                    }
                ],
            }
        try:
            result = self._post_api_or_fail(api_url, data)
        except Exception as e:
            logging.error(f"Failed to set preset for device with id: {device.unique_id}")
            return None
        return result

