import unittest
import time
import PyDSlog.csv as csv
from unittest.mock import patch
from datetime import datetime


class mqtt_test_1(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=500, filename="test.csv", labeled=False, save_as_signal=False,
                                    header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                   w_mode="w", delimiter=",")
        
    def setUp(cls):
        pass

    def test_parameters(self):
        self.assertEqual(self.s.mqtt_port, 7883)
        self.assertEqual(self.s.mqtt_ip, "127.0.0.1")
        self.assertEqual(self.s.topic, "pydslog/0/in/")
        self.assertEqual(self.s.json_index, "payload")
        self.assertEqual(self.s.channels_to_use, ["VAL1","VAL2","VAL3","VAL4","VAL6","VAL5"])
        self.assertEqual(self.s.filepath, "test/")
        self.assertEqual(self.s.filename, "test.csv")
        self.assertEqual(self.s.labeled, False)
        self.assertEqual(self.s.save_as_signal, False)
        self.assertEqual(self.s.header, True)
        self.assertEqual(self.s.custom_header, None)
        self.assertEqual(self.s.mode, "w")
        self.assertEqual(self.s.delimiter, ",")

        self.assertEqual(self.s.generation_status, {0:"start", 1:"pause", 2:"stop", 3:"error"})
        self.assertEqual(self.s.status, 1)
        self.assertEqual(self.s.error_str, "")
        self.assertEqual(self.s.run_label, "")
        self.assertEqual(self.s.values_count, 0)

        self.assertEqual(self.s.serial_con, None)

    def test_format_csv(self):

        v = [[1, 2, 3, 4, 5, 6]]
        s = "1,2,3,4,5,6\n"

        r = self.s.format_csv(v)
        self.assertEqual(r, s)

    def test_header(self):

        h = "VAL1,VAL2,VAL3,VAL4,VAL6,VAL5\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 2, 3, 4, 5, 6]]

            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


class mqtt_test_2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=None, filename="test.csv", labeled=False, save_as_signal=True,
                                    header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                   w_mode="w", delimiter=",")


    def test_header(self):
        h = "VAL1,VAL2,VAL3,VAL4,VAL6,VAL5\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)

    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6]]

            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


class mqtt_test_3(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=500, filename="test.csv", labeled=True, save_as_signal=False,
                                    header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                   w_mode="w", delimiter=",")

    def test_header(self):

        h = "VAL1,VAL2,VAL3,VAL4,VAL6,VAL5,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)

    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 2, 3, 4, 5, 6]]

            self.s.set_label(str(0))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "0")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.s.set_label(str(1))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "1")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


class mqtt_test_4(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=500, filename="test.csv", labeled=True, save_as_signal=False,
                                    header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                   w_mode="w", delimiter=",")

    def test_header(self):

        h = "VAL1,VAL2,VAL3,VAL4,VAL6,VAL5,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 2, 3, 4, 5, 6]]

            self.s.set_label(str(0))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "0")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.s.set_label(str(1))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "1")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


class mqtt_test_4(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=500, filename="test.csv", labeled=True, save_as_signal=False,
                                    header=True, custom_header="DATE;TIME;A;B;C;D;E;F;LABEL", add_tmp=None, date_format="%d/%m/%Y;%H:%M:%S",
                                   w_mode="w", delimiter=";")

    def test_format_csv(self):

            v = [[1, 2, 3, 4, 5, 6]]
            s = "1;2;3;4;5;6;\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "DATE;TIME;A;B;C;D;E;F;LABEL\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 2, 3, 4, 5, 6]]

            self.s.set_label(str(0))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "0")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.s.set_label(str(1))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "1")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


class mqtt_test_5(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MQTT_csv_saver(channels_to_use=["VAL1", "VAL2", "VAL3", "VAL4", "VAL6", "VAL5"], filepath="test/",
                                   mqtt_port=7883, mqtt_ip="127.0.0.1", mqtt_topic="pydslog/0/in/", json_index="payload",
                                   frequency=500, filename="test.csv", labeled=True, save_as_signal=False,
                                    header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                   w_mode="w", delimiter=",")


    def test_format_csv(self):

            v = [[1, 2, 3, 4, 5, 6]]
            s = "1,2,3,4,5,6,\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "VAL1,VAL2,VAL3,VAL4,VAL6,VAL5,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MQTTLogger.stream.MQTT_stream') as mock_stream:
            mock_stream.return_value.read.return_value = [[1, 2, 3, 4, 5, 6]]

            self.s.set_label(str(0))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "0")
            self.s.pause()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 1)
            self.assertEqual(self.s.error_str, "")
            self.s.set_label(str(1))
            self.s.start()
            time.sleep(0.1)
            self.assertEqual(self.s.status, 0)
            self.assertEqual(self.s.error_str, "")
            self.assertEqual(self.s.run_label, "1")
            self.s.stop()
            self.assertEqual(self.s.status, 2)
            self.assertEqual(self.s.error_str, "")

            self.assertFalse(self.s.thread_read_stream.is_alive())
            self.assertFalse(self.s.thread_do_csv.is_alive())


if __name__ == '__main__':
    unittest.main()
