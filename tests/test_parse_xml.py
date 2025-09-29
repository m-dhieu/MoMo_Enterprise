#--------------------------------------------------------------------------------
# Script Name: test_parse_xml.py
# Description: Test parse_xml.py functionality
# Author: Ange Santhiana Kaze
# Date:   2025-09-29
# Usage:  python3 -m unittest test_parse_xml.py
#--------------------------------------------------------------------------------

import unittest
from io import StringIO
import xml.etree.ElementTree as ET
import os
import json

# Import functions from parse_xml.py
from dsa import parse_xml

class TestParseXML(unittest.TestCase):
    
    def test_parse_sms_date(self):
        # Test conversion of milliseconds timestamp to formatted string
        ms_timestamp = '1695859200000'  # corresponds to 2023-09-28 00:00:00 UTC
        expected = '2023-09-28 00:00:00'
        self.assertEqual(parse_xml.parse_sms_date(ms_timestamp), expected)
    
    def test_extract_transaction_info(self):
        body = ("You have received 1,000 RWF at 2025-09-27 14:00:00. "
                "Financial Transaction Id: 12345. New balance: 5,000 RWF.")
        txn_info = parse_xml.extract_transaction_info(body)
        self.assertEqual(txn_info['Amount'], 1,000)
        self.assertEqual(txn_info['Currency'], 'RWF')
        self.assertEqual(txn_info['TransactionType'], 'deposit')
        self.assertEqual(txn_info['DateTime'], '2025-09-27 14:00:00')
        self.assertEqual(txn_info['ReferenceNumber'], '12345')
        self.assertEqual(txn_info['BalanceAfterTransaction'], 5,000)
        self.assertEqual(txn_info['Status'], 'confirmed')
    
    def test_extract_users(self):
        body = "Payment from John Clive (*256700000001) to Jane Smith 256700000002"
        users = parse_xml.extract_users(body)
        self.assertTrue(any(u['Name'] == 'John Clive' and u['PhoneNumber'] == '*256700000001' and u['UserType'] == 'sender' for u in users))
        self.assertTrue(any(u['Name'] == 'Jane Smith' and u['PhoneNumber'] == '256700000002' and u['UserType'] == 'receiver' for u in users))
    
    def test_load_transactions(self):
        # XML data similar to expected input
        xml_sample = """
        <smses>
            <sms protocol="0" address="0712345678" date="1695859200000" type="1"
            body="You have received 1,000 RWF at 2025-09-27 14:00:00. Financial Transaction Id: 12345. New balance: 5,000 RWF. From John Clive (*256700000001) to Jane Smith 256700000002." />
        </smses>"""
        
        # Write XML to a temporary file for parsing
        with open('test_sms.xml', 'w', encoding='utf-8') as f:
            f.write(xml_sample)
        
        transactions = parse_xml.load_transactions('test_sms.xml')
        os.remove('test_sms.xml')
        
        self.assertEqual(len(transactions), 1)
        txn = transactions[0]
        self.assertEqual(txn['TransactionID'], 1)
        self.assertEqual(txn['TransactionType'], 'deposit')
        self.assertEqual(txn['Amount'], 1,000)
        self.assertEqual(txn['Currency'], 'RWF')
        self.assertEqual(txn['DateTime'], '2025-09-27 14:00:00')
        self.assertEqual(txn['ReferenceNumber'], '12345')
        self.assertEqual(txn['BalanceAfterTransaction'], 5,000)
        self.assertEqual(txn['Status'], 'confirmed')
        self.assertIn('MessageText', txn)
        self.assertEqual(len(txn['Participants']), 2)
    
    def test_save_transactions_json(self):
        # Sample data to save
        transactions = [{'TransactionID': 1, 'Amount': 1,000, 'MessageText': 'test'}]
        file_path = 'test_transactions.json'
        
        parse_xml.save_transactions_json(transactions, file_path)
        
        self.assertTrue(os.path.exists(file_path))
        
        # Load back and verify contents
        with open(file_path, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded, transactions)
        
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
