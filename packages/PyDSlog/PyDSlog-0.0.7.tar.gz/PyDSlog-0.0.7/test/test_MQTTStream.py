import unittest
import json
import PyDSlog.stream as stream
from unittest.mock import patch

values = json.dumps({"payload":{"value1":[-1, -97, -96, -95, -93, -92], "value2":[-100, -99, -94, -92, -89, -88], "value3":[-98, -95, -92, -91, -89, -87], "value4":[-9, -95, -92, -91, -89, -87]}})

class mqtt_stream_test_1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = stream.MQTT_stream(topic="pydslog/0/in/", channels_to_use=["value1", "value2", "value3", "value4"], mqtt_ip="127.0.0.1", mqtt_port=7883)

    def setUp(cls):
        pass

    def test_parameters(self):
        self.assertEqual(self.s.mqtt_port, 7883)
        self.assertEqual(self.s.channels_to_use, ["value1", "value2", "value3", "value4"])
        self.assertEqual(self.s.topic, "pydslog/0/in/")
        self.assertEqual(self.s.mqtt_ip, "127.0.0.1")

class mqtt_stream_test_2(unittest.TestCase):

    def test_read(self):

        with patch('PyDSlog.stream.MQTTStream.queue.Queue') as mock_queue:
            mock_queue.return_value.get.return_value = values

            s = stream.MQTT_stream(topic="pydslog/0/in/", channels_to_use=["value1", "value2", "value3", "value4"],
                               mqtt_ip="127.0.0.1", mqtt_port=7883)
            v = s.read(transpose=False)
            self.assertEqual(v, [[-1, -97, -96, -95, -93, -92], [-100, -99, -94, -92, -89, -88], [-98, -95, -92, -91, -89, -87], [-9, -95, -92, -91, -89, -87]])

            v = s.read(transpose=True)
            self.assertEqual(v, [[-1, -100, -98, -9], [-97, -99, -95, -95], [-96, -94, -92, -92], [-95, -92, -91, -91], [-93, -89, -89, -89], [-92, -88, -87, -87]])


if __name__ == '__main__':
    unittest.main()