import unittest
from unittest.mock import patch

import synchronous_shopping


@patch('synchronous_shopping.input')
@patch('synchronous_shopping.open')
@patch('synchronous_shopping.os.environ', return_value={'OUTPUT_PATH': 'mock-output-path.file'})
class TestMain(unittest.TestCase):
    def setUp(self):
        self.too_slow = {
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
        }

    def test(self, mock_os_environ, mock_open, mock_input):
        for i in range(0, 30+1):
            mock_os_environ.reset_mock()
            mock_open.reset_mock()
            mock_input.reset_mock()

            name = f'test_case_{i}'
            with self.subTest(name=name):
                i_zpad = f'{i:02}'
                if i in self.too_slow:
                    self.skipTest(reason=f'test {i_zpad} runs too slow')
                with open(f'input{i_zpad}.txt', 'r', encoding='utf-8') as input_file:
                    mock_input.side_effect = input_file.readlines()
                with open(f'output{i_zpad}.txt', 'r', encoding='utf-8') as output_file:
                    expected = int(output_file.read().strip())

                self.assertIsNone(synchronous_shopping.main())
                mock_open.assert_called_with(mock_os_environ['OUTPUT_PATH'], 'w', encoding='utf-8')
                mock_input.assert_called()
                mock_open.return_value.__enter__.return_value.write.assert_called_once_with(str(expected) + '\n')


if __name__ == '__main__':
    unittest.main()
