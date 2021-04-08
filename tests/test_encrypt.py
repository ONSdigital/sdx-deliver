import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from app import gnupg, CONFIG
from app.encrypt import encrypt_output


class TestInit(unittest.TestCase):

    def setUp(self):
        with open('../test_key.txt', 'r') as file:
            test_key = file.read()
        gpg = gnupg.GPG()
        gpg.import_keys(test_key)
        CONFIG.ENCRYPTION_KEY = test_key
        CONFIG.GPG = gpg

    def test_encrypt(self):
        with self.assertLogs('app.encrypt', level='INFO') as actual:
            test_data = b'{data to be encrypted}'
            encrypt_output(test_data)
        self.assertEqual(actual.output[0], 'INFO:app.encrypt:{"event": "Successfully encrypted output", "level": '
                                           '"info", "logger": "app.encrypt"}')

    @patch.object(CONFIG.GPG, 'encrypt')
    def test_encrypt_bad(self, mock_encrypt):
        with self.assertLogs('app.encrypt', level='ERROR') as actual:
            mock_encrypt.return_type.ok = False
            test_data = b'{data to be encrypted}'
            encrypt_output(test_data)
        self.assertEqual(actual.output[0], 'ERROR:app.encrypt:{"event": "Failed to encrypt output", "level": '
                                           '"error", "logger": "app.encrypt"}')
