#!/usr/bin/env python3

import unittest
import conscommon.data
import conscommon.data_model
import conscommon.data_model.mks as mks


class TestDataModel(unittest.TestCase):
    def setUp(self):
        conscommon.data.API_CANDIDATES = ["localhost:8080"]
        self.data_mks = conscommon.data.getMKS()
        self.data_agilent = conscommon.data.getAgilent()
        self.data_mbtemp = conscommon.data.getMBTemp()

    def test_mksDevice(self):
        for device in conscommon.data_model.getDevicesFromBeagles(
            conscommon.data_model.getBeaglesFromList(self.data_mks)
        ):
            self.assertIn(device.enable, [True, False])
            self.assertEqual(device.channels.__len__(), 6)
            self.assertNotEqual(device.info, None)

    def test_mksChannel(self):
        for device in conscommon.data_model.getDevicesFromBeagles(
            conscommon.data_model.getBeaglesFromList(self.data_mks)
        ):
            for channel in device.channels:
                self.assertNotEqual(channel.info, None)
                self.assertIn(channel.name, mks.MKS_CHANNEL_NAMES)
                self.assertIn(
                    channel.info.sensor,
                    [
                        mks.MKS_SENSOR_COLD_CATHODE,
                        mks.MKS_SENSOR_PIRANI,
                        mks.MKS_SENSOR_NOT_USED,
                    ],
                )

    def test_mbtempDevice(self):
        for device in conscommon.data_model.getDevicesFromBeagles(
            conscommon.data_model.getBeaglesFromList(self.data_mbtemp)
        ):
            self.assertIn(device.enable, [True, False])
            self.assertEqual(device.channels.__len__(), 8)

    def test_agilentDevice(self):
        for device in conscommon.data_model.getDevicesFromBeagles(
            conscommon.data_model.getBeaglesFromList(self.data_agilent)
        ):
            self.assertIn(device.enable, [True, False])
            self.assertEqual(device.channels.__len__(), 4)


if __name__ == "__main__":
    unittest.main()
