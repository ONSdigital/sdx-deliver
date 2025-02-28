import json
import unittest
from unittest.mock import patch, MagicMock

from app import gnupg, CONFIG
from app.encrypt import encrypt_output


class TestInit(unittest.TestCase):

    def setUp(self):
        with open('tests/unit/test_key.txt', 'r') as file:
            test_key = file.read()
        gpg = gnupg.GPG()
        gpg.import_keys(test_key)
        CONFIG.ENCRYPTION_KEY = test_key
        CONFIG.GPG = gpg

    def test_encrypt(self):
        with self.assertLogs('app.encrypt', level='INFO') as actual:
            test_data = b'{data to be encrypted}'
            encrypt_output(test_data)
            log_str = actual.output[0]
            log_json = json.loads(log_str[17:])
            self.assertEqual('Successfully encrypted output', log_json['message'])

    @patch('app.encrypt.CONFIG')
    def test_encrypt_bad(self, mock_encrypt):
        with self.assertLogs('app.encrypt', level='ERROR') as actual:
            mock_encrypted = MagicMock()
            mock_encrypted.ok = False
            mock_encrypt.GPG.encrypt.return_value = mock_encrypted
            test_data = b'{data to be encrypted}'
            encrypt_output(test_data)
            log_str = actual.output[0]
            log_json = json.loads(log_str[18:])
            self.assertEqual('Failed to encrypt output', log_json['message'])
