import unittest
import PyDSlog.stream as stream
from unittest.mock import patch


def generate_return(n):
    a = bytearray(b'M\x04\xd0\xff\xea\x00\x00\x01\x01\x01\x00\xf9R\x00\x00\x00\x00\x16')
    for i in range(0, n):
        a += b'M\x04\xd0\xff\xea\x00\x00\x01\x01\x01\x00\xf9R\x00\x00\x00\x00\x16'
    return a


def generate_values(transpose):
    l2 = [1232, -22, 0, 257, 256, -1710, 0, 0]

    if transpose:
        l = [[0 for b in range(8)] for i in range(100)]
        for i in range(0, 100):
            for n in range(0, 8):
                l[i][n] = l2[n]
    else:
        l = [[0 for a in range(100)] for i in range(8)]
        for i in range(0, 100):
            for n in range(0, 8):
                l[n][i] = l2[n]

    return (l)

class arduino_stream_test_1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = stream.Arduino_stream(sz_block=100, channels_to_use=["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"], frequency=500, port="COM14", baudrate=115200)

    def setUp(cls):
        pass

    def test_parameters(self):
        self.assertEqual(self.s.port, "COM14")
        self.assertEqual(self.s.channels, ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
        self.assertEqual(self.s.frequency, 500)
        self.assertEqual(self.s.sz_block, 100)

    def test_start(self):

        with patch('PyDSlog.stream.IO5640Stream.serial.Serial') as mock_serial:

            self.s.connect()
            self.s.start()
            a = str(mock_serial.mock_calls[1])
            a = a[25:-3]
            #print(a)
            self.assertEqual(a, str("A\\xff\\xf4\\x01\\xe1"))


    def test_read(self):
        with patch('PyDSlog.stream.IO5640Stream.serial.Serial') as mock_serial:
            mock_serial.return_value.read.return_value = generate_return(100)

            self.s.connect()
            self.s.start()

            v = self.s.read(transpose=True)
            self.assertEqual(v, generate_values(1))
            self.assertEqual(len(v[0]), 8)
            self.assertEqual(len(v), 100)

            v = self.s.read(transpose=False)
            self.assertEqual(v, generate_values(0))
            self.assertEqual(len(v[0]), 100)
            self.assertEqual(len(v), 8)


if __name__ == '__main__':
    unittest.main()