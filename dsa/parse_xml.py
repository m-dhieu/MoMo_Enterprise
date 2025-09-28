#--------------------------------------------------------------------------------
# Script Name: parse_xml.py
# Description: Parses the modified_sms_v2.xml file in Python
#              Converts SMS records into JSON objects (list of dictionaries)
#              Saves the parsed JSON to a file for use in API
# Author: Monica Dhieu
# Date:   2025-09-27
# Usage:  python3 parse_xml.py [input_xml_path] [output_json_path]
#--------------------------------------------------------------------------------

from lxml import etree as ET
from datetime import datetime
import re
import json
import sys
import os
from pathlib import Path

def parse_sms_date(ms_timestamp):
    """
    Converts milliseconds to a formatted datetime string: '%Y-%m-%d %H:%M:%S'.
    """
    ts = int(ms_timestamp) / 1000
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def extract_transaction_info(body):
    """
    Parses SMS text and extracts transaction details:
    amount, currency, transaction type, datetime, reference ID,
    balance after transaction, status, and full message text.
    """
    transaction = {}
    # Improve regex to:
    # match amount with commas and currency (e.g., "1,000 RWF")
    amount_match = re.search(r'([\d,]+) (\w{3})', body)
    if amount_match:
        # Remove commas before float conversion
        # Check for empty string to prevent ValueError
        amount_str = amount_match.group(1).replace(',', '')
        if amount_str:
            transaction['Amount'] = float(amount_str)
        else:
            transaction['Amount'] = None
        transaction['Currency'] = amount_match.group(2)
    if 'received' in body.lower():
        transaction['TransactionType'] = 'deposit'
    elif 'payment' in body.lower():
        transaction['TransactionType'] = 'payment'
    elif 'transferred' in body.lower():
        transaction['TransactionType'] = 'transfer'
    elif 'withdrawal' in body.lower():
        transaction['TransactionType'] = 'withdrawal'
    else:
        transaction['TransactionType'] = 'other'
    # Extract datetime from SMS body text
    dt_match = re.search(r'at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
    transaction['DateTime'] = dt_match.group(1) if dt_match else None
    # Extract reference number from SMS body text
    ref_match = re.search(r'(Financial Transaction Id:|TxId:)\s*([\d]+)', body)
    transaction['ReferenceNumber'] = ref_match.group(2) if ref_match else None
    # Extract balance after transaction and converting to float safely
    bal_match = re.search(r'new balance:?([\d,]+) (\w{3})', body.lower())
    transaction['BalanceAfterTransaction'] = float(bal_match.group(1).replace(',', '')) if bal_match else None
    transaction['Status'] = 'confirmed'  # Default
    transaction['MessageText'] = body.replace("'", "''") if body else ''
    return transaction

def extract_users(body):
    """
    Extracts user details from SMS text (sender and receiver info).
    """
    users = []

    # Improve regex to:
    # capture sender name strictly as letters and spaces only,
    # and match phone number including digits and stars, ignoring case
    sender_match = re.search(r'from ([A-Za-z\s]+) \(([*\d]+)\)', body, re.IGNORECASE)
    if sender_match:
        users.append({
            'Name': sender_match.group(1).strip(),
            'PhoneNumber': sender_match.group(2).strip(),
            'UserType': 'sender'
        })
    # Improve receiver regex to:
    # non-greedy matching to avoid trailing extra words,
    # with optional space, and parentheses around phone number included
    receiver_match = re.search(r'to ([A-Za-z\s]+?) ?\(?(\d+)\)?', body, re.IGNORECASE)
    if receiver_match:
        users.append({
            'Name': receiver_match.group(1).strip(),
            'PhoneNumber': receiver_match.group(2).strip(),
            'UserType': 'receiver'
        })
    else:
        receiver_match2 = re.search(r'to ([\w\s]+) \(([\d]+)\)', body)
        if receiver_match2:
            users.append({
                'Name': receiver_match2.group(1).strip(),
                'PhoneNumber': receiver_match2.group(2).strip(),
                'UserType': 'receiver'
            })
    return users

def load_transactions(file_path):
    """
    Parses the XML file and returns a list of transaction dicts for JSON serialization.
    """
    try:
        # Allow recovery from common XML syntax errors instead of failing
        # Enable huge_tree to handle big datasets (SMS transaction file)
        parser = ET.XMLParser(recover=True, huge_tree=True)
        tree = ET.parse(file_path, parser)
    except (ET.ParseError, FileNotFoundError) as e:
        print(f"Error reading XML file '{file_path}': {e}")
        return []

    root = tree.getroot()
    user_id_map = {}
    user_counter = 1
    transaction_counter = 1

    transactions = []

    for sms in root.findall('sms'):
        body = sms.attrib.get('body')
        date_ms = sms.attrib.get('date')
        sms_datetime = parse_sms_date(date_ms) if date_ms else None

        transaction_info = extract_transaction_info(body)
        if not transaction_info.get('DateTime'):
            transaction_info['DateTime'] = sms_datetime

        users = extract_users(body)
        for u in users:
            key = (u['Name'], u['PhoneNumber'], u['UserType'])
            if key not in user_id_map:
                user_id_map[key] = user_counter
                user_counter += 1
                u['UserID'] = user_id_map[key]
            else:
                u['UserID'] = user_id_map[key]

        transaction = {
            'TransactionID': transaction_counter,
            'TransactionType': transaction_info.get('TransactionType'),
            'Amount': transaction_info.get('Amount'),
            'Currency': transaction_info.get('Currency'),
            'DateTime': transaction_info.get('DateTime'),
            'ReferenceNumber': transaction_info.get('ReferenceNumber'),
            'BalanceAfterTransaction': transaction_info.get('BalanceAfterTransaction'),
            'Status': transaction_info.get('Status'),
            'MessageText': transaction_info.get('MessageText'),
            'Participants': users
        }
        transactions.append(transaction)
        transaction_counter += 1

    return transactions

def save_transactions_json(transactions, json_path):
    """
    Saves the transactions list to a JSON file.
    Creates directories if they don't exist.
    """
    try:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as json_file:
            json.dump(transactions, json_file, indent=4)
        print(f"Transactions saved to JSON file: {json_path}")
    except Exception as e:
        print(f"Error saving JSON to {json_path}: {e}")

# Main program flow
if __name__ == '__main__':
    # Fix path to avoid file-not-found errors
    input_xml_path = sys.argv[1] if len(sys.argv) > 1 else '../data/raw/modified_sms_v2.xml'
    output_json_path = sys.argv[2] if len(sys.argv) > 2 else '../data/processed/transactions.json'

    print(f"Loading XML data from {input_xml_path} ...")
    transactions = load_transactions(input_xml_path)

    if transactions:
        save_transactions_json(transactions, output_json_path)
        print("Parsed transactions JSON preview:")
        print(json.dumps(transactions[:3], indent=4))  # Show first 3 transactions
    else:
        print("No transactions parsed. Please check your XML file and path.")

