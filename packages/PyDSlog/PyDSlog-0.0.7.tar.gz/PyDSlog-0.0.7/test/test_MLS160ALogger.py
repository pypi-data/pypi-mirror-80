import unittest
import time
import PyDSlog.csv as csv
from unittest.mock import patch
from datetime import datetime


class mls160a_test_1(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename="test.csv",
                                      labeled=False, save_as_signal=False,
                                      header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=",")


    def setUp(cls):
        pass

    def test_parameters(self):

        self.assertEqual(self.s.port, "COM3")
        self.assertEqual(self.s.channels_to_use, ["ACCX","ACCY","ACCZ","GYRX","GYRY","GYRZ"])
        self.assertEqual(self.s.frequency, 500)
        self.assertEqual(self.s.block_size, 500)
        self.assertEqual(self.s.filepath, "test/")
        self.assertEqual(self.s.filename, "test.csv")
        self.assertEqual(self.s.labeled, False)
        self.assertEqual(self.s.save_as_signal, False)
        self.assertEqual(self.s.header, True)
        self.assertEqual(self.s.custom_header, None)
        self.assertEqual(self.s.add_tmp, None)
        self.assertEqual(self.s.date_format, "%d/%m/%Y,%H:%M:%S")
        self.assertEqual(self.s.baudrate, 115200)
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

        h = "ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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


class mls160a_test_2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename=None,
                                      labeled=False, save_as_signal=True,
                                      header=True, custom_header=None, add_tmp=None, date_format="%d/%m/%Y,%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=",")


    def test_header(self):
        h = "ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)

    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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


class mls160a_test_3(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename="test.csv",
                                      labeled=True, save_as_signal=False,
                                      header=True, custom_header=None, add_tmp="ms", date_format="%d/%m/%Y,%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=",")

    def test_format_csv(self):

        with patch('PyDSlog.csv.MLS160ALogger.time') as mock_ms:
            mock_ms.time.return_value = 99

            v = [[1, 2, 3, 4, 5, 6]]
            s = "99000,1,2,3,4,5,6,\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "ms,ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)

    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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


class mls160a_test_4(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename="test.csv",
                                      labeled=True, save_as_signal=False,
                                      header=True, custom_header=None, add_tmp="date", date_format="%d/%m/%Y,%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=",")

    def test_format_csv(self):

        with patch('PyDSlog.csv.MLS160ALogger.datetime') as mock_ms:
            n = datetime.now()
            mock_ms.now.return_value = n

            date_time = n.strftime("%d/%m/%Y,%H:%M:%S")

            v = [[1, 2, 3, 4, 5, 6]]
            s = date_time+",1,2,3,4,5,6,\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "date,time,ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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


class mls160a_test_4(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename="test.csv",
                                      labeled=True, save_as_signal=False,
                                      header=True, custom_header="DATE;TIME;A;B;C;D;E;F;LABEL", add_tmp="date", date_format="%d/%m/%Y;%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=";")

    def test_format_csv(self):

        with patch('PyDSlog.csv.MLS160ALogger.datetime') as mock_ms:
            n = datetime.now()
            mock_ms.now.return_value = n

            date_time = n.strftime("%d/%m/%Y;%H:%M:%S")

            v = [[1, 2, 3, 4, 5, 6]]
            s = date_time+";1;2;3;4;5;6;\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "DATE;TIME;A;B;C;D;E;F;LABEL\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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


class mls160a_test_5(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.s = csv.MLS160A_csv_saver(port="COM3", channels_to_use=["ACCX", "ACCY", "ACCZ", "GYRX", "GYRY", "GYRZ"],
                                      frequency=500, block_size=500, filepath="test/", filename="test.csv",
                                      labeled=True, save_as_signal=False,
                                      header=True, custom_header=None, add_tmp="us", date_format="%d/%m/%Y,%H:%M:%S",
                                      baudrate=115200, w_mode="w", delimiter=",")

    def test_format_csv(self):

        with patch('PyDSlog.csv.MLS160ALogger.time') as mock_ms:
            mock_ms.time.return_value = 99

            v = [[1, 2, 3, 4, 5, 6]]
            s = "99000000,1,2,3,4,5,6,\n"

            r = self.s.format_csv(v)
            self.assertEqual(r, s)

    def test_header(self):

        h = "us,ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ,label\n"

        r = self.s.generate_header()
        self.assertEqual(r, h)


    def test_start_csv(self):

        self.assertFalse(self.s.stream_thread_keepalive_flag.is_set())
        self.assertFalse(self.s.start_flag.is_set())

        with patch('PyDSlog.csv.MLS160ALogger.stream.MLS160A_stream') as mock_stream:
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
