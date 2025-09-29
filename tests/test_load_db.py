#--------------------------------------------------------------------------------
# Script Name: test_load_db.py
# Description: Test load_db.py functionality
# Author: Ange Santhiana Kaze
# Date:   2025-09-29
# Usage:  python3 -m unittest test_load_db.py
#--------------------------------------------------------------------------------

import unittest
import os
import mysql.connector
from etl import load_db 
import json

class TestLoadDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up MySQL connection config 
        cls.conn = mysql.connector.connect(
            user='your_user', password='your_password',
            host='localhost', database='momo_db'
        )
        cls.cursor = cls.conn.cursor()
        # Clear the DB tables to start clean 
        cls.cursor.execute('DELETE FROM TransactionParticipant')
        cls.cursor.execute('DELETE FROM Transaction')
        cls.cursor.execute('DELETE FROM User')
        cls.cursor.execute('DELETE FROM TransactionCategory')
        cls.conn.commit()

    def test_load_single_transaction(self):
        # Prepare a minimal transaction JSON to load
        test_tx = [{
            'TransactionID': 9999,
            'TransactionType': 'deposit',
            'Amount': 100.0,
            'Currency': 'USD',
            'DateTime': '2025-09-27 12:00:00',
            'ReferenceNumber': 'TESTREF',
            'BalanceAfterTransaction': 1000.0,
            'Status': 'confirmed',
            'MessageText': 'Test deposit message',
            'Participants': [{
                'UserID': 100,
                'Name': 'John Doe',
                'PhoneNumber': '+1234567890',
                'UserType': 'sender'
            }]
        }]

        # Dump to temporary JSON file
        json_path = 'test_transactions.json'
        with open(json_path, 'w') as f:
            json.dump(test_tx, f)

        # Call load_db main logic to load this JSON
        load_db_main = getattr(load_db, 'main', None)
        if load_db_main:
            # Temporarily replace sys.argv for test
            import sys
            sys.argv = ['load_db.py', json_path]
            load_db_main()

        # Verify insertion into DB
        self.cursor.execute('SELECT COUNT(*) FROM Transaction WHERE TransactionID=9999')
        tx_count = self.cursor.fetchone()[0]
        self.assertEqual(tx_count, 1)

        self.cursor.execute('SELECT Name FROM User WHERE PhoneNumber=%s', ('+1234567890',))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'John Doe')

        # Cleanup temporary JSON file
        os.remove(json_path)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.conn.close()

if __name__ == '__main__':
    unittest.main()
