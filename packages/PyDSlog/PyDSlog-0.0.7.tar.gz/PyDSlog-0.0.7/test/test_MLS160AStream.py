import unittest
import PyDSlog.stream as stream
from unittest.mock import patch


def generate_return(n):
    a = bytearray(b'M`\xffd\x02\x08\xbe\x06\x00\n\x00\xff\xff\xc2')
    for i in range(0, n):
        a += b'M`\xffd\x02\x08\xbe\x06\x00\n\x00\xff\xff\xc2'
    return a


def generate_values(transpose):
    l2 = [-160, 612, -16888, 6, 10, -1]

    if transpose:
        l = [[0 for b in range(6)] for i in range(100)]
        for i in range(0, 100):
            for n in range(0, 6):
                l[i][n] = l2[n]
    else:
        l = [[0 for a in range(100)] for i in range(6)]
        for i in range(0, 100):
            for n in range(0, 6):
                l[n][i] = l2[n]

    return (l)

class io5640_test_1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = stream.MLS160A_stream(sz_block=100, channels_to_use=["ACCX","ACCY","ACCZ","GYRX","GYRY","GYRZ"], frequency=500, port="COM14", baudrate=115200)

    def setUp(cls):
        pass

    def test_parameters(self):
        self.assertEqual(self.s.port, "COM14")
        self.assertEqual(self.s.channels, ["ACCX","ACCY","ACCZ","GYRX","GYRY","GYRZ"])
        self.assertEqual(self.s.frequency, 500)
        self.assertEqual(self.s.sz_block, 100)

    def test_start(self):

        with patch('PyDSlog.stream.MLS160AStream.serial.Serial') as mock_serial:

            self.s.connect()
            self.s.start()
            a = str(mock_serial.mock_calls[1])
            a = a[25:-3]
            self.assertEqual(a, str("A?\\xf4\\x01l"))

    def test_read(self):
        with patch('PyDSlog.stream.MLS160AStream.serial.Serial') as mock_serial:
            mock_serial.return_value.read.return_value = generate_return(100)

            self.s.connect()
            self.s.start()

            v = self.s.read(transpose=True)
            self.assertEqual(v, generate_values(1))
            self.assertEqual(len(v[0]), 6)
            self.assertEqual(len(v), 100)

            v = self.s.read(transpose=False)
            self.assertEqual(v, generate_values(0))
            self.assertEqual(len(v[0]), 100)
            self.assertEqual(len(v), 6)


if __name__ == '__main__':
    unittest.main()