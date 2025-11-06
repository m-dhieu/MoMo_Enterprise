#--------------------------------------------------------------------------------
# Script Name: load_db.py
# Description: Loads parsed transaction JSON data into MySQL database
# Author: Monica Dhieu
# Date:   2025-09-27
# Usage:  python3 load_db.py [input_json_path]
#--------------------------------------------------------------------------------

import mysql.connector
from mysql.connector import errorcode
import json
import sys

# Connection credentials
DB_CONFIG = {
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'momo_db',
    'raise_on_warnings': True
}

def connect_db():
    """Connects to MySQL database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: check your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        sys.exit(1)

def load_json(json_path):
    """Loads transactions JSON file"""
    with open(json_path, 'r') as f:
        return json.load(f)

def get_or_create_category(cursor, category_name):
    """Fetchees CategoryID or creates if not exists"""
    cursor.execute("SELECT CategoryID FROM TransactionCategory WHERE CategoryName = %s", (category_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    # Insert new transaction category
    cursor.execute(
        "INSERT INTO TransactionCategory (CategoryName) VALUES (%s)", (category_name,)
    )
    return cursor.lastrowid

def get_or_create_user(cursor, user):
    """Fetches UserID or inserts new user by PhoneNumber"""
    cursor.execute("SELECT UserID FROM User WHERE PhoneNumber = %s", (user['PhoneNumber'],))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(
        "INSERT INTO User (PhoneNumber, Name, UserType) VALUES (%s, %s, %s)",
        (user['PhoneNumber'], user.get('Name',''), user['UserType'])
    )
    return cursor.lastrowid

def insert_transaction(cursor, transaction, category_id):
    """Inserts a transaction"""
    cursor.execute(
        """INSERT INTO Transaction 
        (TransactionType, Amount, Currency, DateTime, ReferenceNumber, BalanceAfterTransaction, Status, MessageText, CategoryID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (transaction['TransactionType'], transaction['Amount'], transaction['Currency'], transaction['DateTime'],
         transaction.get('ReferenceNumber'), transaction['BalanceAfterTransaction'],
         transaction['Status'], transaction['MessageText'], category_id)
    )
    return cursor.lastrowid

def insert_participants(cursor, transaction_id, participants):
    """Inserts transaction participants with role"""
    for p in participants:
        user_id = get_or_create_user(cursor, p)
        cursor.execute(
            "INSERT INTO TransactionParticipant (TransactionID, UserID, Role) VALUES (%s, %s, %s)",
            (transaction_id, user_id, p['UserType'])
        )

def main():
    # Fix path to avoid file-not-found errors
    input_json = sys.argv[1] if len(sys.argv) > 1 else '../data/processed/transactions.json'
    transactions = load_json(input_json)

    conn = connect_db()
    cursor = conn.cursor()

    for tx in transactions:
        category_id = get_or_create_category(cursor, tx['TransactionType'])
        transaction_id = insert_transaction(cursor, tx, category_id)
        insert_participants(cursor, transaction_id, tx.get('Participants', []))
        conn.commit()

    cursor.close()
    conn.close()
    print("Finished loading transactions into MySQL database.")

if __name__ == '__main__':
    main()

