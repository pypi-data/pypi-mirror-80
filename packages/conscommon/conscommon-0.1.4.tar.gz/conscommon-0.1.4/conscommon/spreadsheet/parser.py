#!/usr/bin/env python3

from typing import Dict

import pandas
import numpy

from conscommon import get_logger
from conscommon.spreadsheet import SheetName

logger = get_logger("Parser")


def normalizeAgilent(sheet) -> dict:
    return normalize(sheet, ["C1", "C2", "C3", "C4"])


def normalizeMKS(sheet) -> dict:
    return normalize(sheet, ["A1", "A2", "B1", "B2", "C1", "C2"])


def normalizeMBTemp(sheet) -> dict:
    # ENABLE	IP	Rack	ADDR	Dev	Location
    return normalize(
        sheet,
        ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8"],
        device_col="Dev",
    )


def normalize(
    sheet,
    ch_names: list,
    device_col: str = "Dispositivo",
    ip_col="IP",
    enable_col="ENABLE",
) -> dict:
    """ Create a dictionary with the beaglebone IP as keys.  Aka: {ip:[devices ...] ... ipn:[devicesn ... ]} """
    ips = {}
    try:
        for n, row in sheet.iterrows():
            ip = row.get(ip_col)
            if ip not in ips:
                ips[ip] = []
            ip_devices = ips[ip]
            data = {}

            ip_devices.append(data)
            data["enable"] = row.get(enable_col, False)
            data["prefix"] = row.get(device_col)

            info = {}
            info["sector"] = row.get("Setor", "")
            info["serial_id"] = row.get("RS485 ID")
            info["rack"] = row.get("Rack")
            data["info"] = info

            channels = {}
            num = 0
            for ch_name in ch_names:
                channel = {}
                channel["num"] = num
                channel["prefix"] = row[ch_name]
                channel["enable"] = row[ch_name] != "" or row[ch_name] is None

                info = {}
                info["pressure_hi"] = row.get("HI " + ch_name)
                info["pressure_hihi"] = row.get("HIHI " + ch_name)
                if "Sensor " + ch_name in row:
                    info["sensor"] = row.get("Sensor " + ch_name)
                channel["info"] = info

                channels[ch_name] = channel
                num += 1

            data["channels"] = channels
    except Exception:
        logger.exception("Failed to update data from spreadsheet.")

    logger.info("Loaded data from sheet with {} different IPs.".format(len(ips)))
    return ips


def loadSheet(spreadsheet_xlsx_path: str, sheetName: SheetName) -> dict:
    logger.info(
        'Loading spreadsheet "{}" from url "{}"'.format(
            spreadsheet_xlsx_path, sheetName.value
        )
    )
    sheet = pandas.read_excel(spreadsheet_xlsx_path, sheet_name=sheetName.value)
    sheet = sheet.replace(numpy.nan, "", regex=True)

    if sheetName == SheetName.AGILENT:
        return normalizeAgilent(sheet)

    elif sheetName == SheetName.MKS:
        return normalizeMKS(sheet)

    elif sheetName == SheetName.MBTEMP:
        return normalizeMBTemp(sheet)

    else:
        return {}


def loadSheets(spreadsheet_xlsx_path: str) -> Dict[SheetName, dict]:
    data: Dict[SheetName, dict] = {}
    for sheetName in SheetName:
        data[sheetName] = loadSheet(spreadsheet_xlsx_path, sheetName)
    return data
