#!/usr/bin/env python3
import requests
import logging
from typing import List, Iterable, Tuple
from conscommon import get_logger

logger = get_logger(level=logging.INFO)
TIMEFMT = "%d/%m/%Y %H:%M:%S"
API_CANDIDATES = ["10.0.38.42:26001", "10.0.38.46:26001", "10.0.38.59:26001", "localhost:8080"]


class RemoteAPI(Exception):
    pass


def checkCandidates() -> str:
    for ip in API_CANDIDATES:
        url = "http://{}".format(ip)
        try:
            if requests.get(url + "/status", timeout=2).text == "Healthy!":
                logger.info('Using remote url "{}"'.format(url))
                return url + "/devices"
        except:
            logger.warning('Remote url "{}" unavailable'.format(url))
            pass
    raise RemoteAPI("No remote API available")


_TIMEOUT = 5


def getMBTemp() -> List[dict]:
    """ MBTemp json from upstream @return dict following the data_model pattern """
    return requests.get(
        checkCandidates(), verify=False, params={"type": "mbtemp"}, timeout=_TIMEOUT
    ).json()


def getMKS() -> List[dict]:
    """ MKS json from upstream @return dict following the data_model pattern """
    return requests.get(
        checkCandidates(), verify=False, params={"type": "mks"}, timeout=_TIMEOUT
    ).json()


def getAgilent() -> List[dict]:
    """ Agilent json from upstream @return dict following the data_model pattern """
    return requests.get(
        checkCandidates(), verify=False, params={"type": "agilent"}, timeout=_TIMEOUT
    ).json()


def getDevicesDict(data: dict) -> Iterable[dict]:
    """ Device generator from json """
    for ip, beagle in data.items():
        for device in beagle:
            yield device


def getChannelsDict(data: dict) -> Iterable[Tuple[str, str, dict]]:
    """ Tuple of (device prefix, channel_name, channel_data) generator from json """
    for ip, beagle in data.items():
        for device in beagle:
            for channel_name, channel_data in device["channels"].items():
                yield device["prefix"], channel_name, channel_data


if __name__ == "__main__":
    # for ip, dev in getAgilent().items():
    data = getAgilent()
    for device, channel_name, channel_data in getChannelsDict(data):
        print(device, channel_name, channel_data["prefix"])
