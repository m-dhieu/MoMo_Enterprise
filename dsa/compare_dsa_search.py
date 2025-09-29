#--------------------------------------------------------------------------------
# Script Name: compare_dsa_search.py
# Description: Compares linear search vs dictionary lookup on MoMo SMS transactions.
#              Loads parsed transaction JSON and measures performance of both lookup methods.
# Author: Thierry Gabin
# Date:   2025-09-28
# Usage:  python3 compare_dsa_search.py
#--------------------------------------------------------------------------------

import json
import time
import random

def load_transactions(json_path='../data/processed/transactions.json'):
    # load transactions from JSON file & return list of transaction dictionaries
    with open(json_path, 'r') as f:
        return json.load(f)

def linear_search(transactions, transaction_id):
    # do linear search for a transaction by ID
    for i in transactions:
        if i['TransactionID'] == transaction_id:
            return i
    return None

def build_transaction_dict(transactions):
    # build a dictionary with TransactionID as keys for fast lookups
    # return a mapping of TransactionID to transaction dict
    return {i['TransactionID']: i for i in transactions}

def dict_lookup(transaction_dict, transaction_id):
    # do a dictionary lookup for a transaction by ID
    # return the transaction dictionary if found, else None
    return transaction_dict.get(transaction_id)

def compare_search_performance(transactions, ids_to_search):
    # measure & compare time taken by linear search and dictionary lookup
    # return tuple: (linear_search_time, dict_lookup_time) in seconds
    transaction_dict = build_transaction_dict(transactions)

    # linear search time
    start_linear = time.perf_counter()
    for t in ids_to_search:
        linear_search(transactions, t)
    end_linear = time.perf_counter()
    linear_duration = end_linear - start_linear

    # dictionary lookup time
    start_dict = time.perf_counter()
    for t in ids_to_search:
        dict_lookup(transaction_dict, t)
    end_dict = time.perf_counter()
    dict_duration = end_dict - start_dict

    print(f"Linear Search took: {linear_duration:.6f} seconds.")
    print(f"Dictionary Lookup took: {dict_duration:.6f} seconds.")

    return linear_duration, dict_duration

def main():
    # load transactions from JSON file
    transactions = load_transactions()
    print(f"Loaded {len(transactions)} transactions.")

    # sample 20 transaction IDs or use all if less available
    sample_size = 20
    available_ids = [i['TransactionID'] for i in transactions]
    if len(available_ids) < sample_size:
        print("Not enough transactions to sample 20 IDs, using all available IDs.")
        ids_to_search = available_ids
    else:
        ids_to_search = random.sample(available_ids, sample_size)

    # compare search performance
    compare_search_performance(transactions, ids_to_search)

    # reflections
    print("\nReflection:")
    print("Dictionary lookup is significantly faster than linear search because dictionaries")
    print("use hash tables providing average O(1) time complexity, whereas linear search")
    print("requires O(n) time scanning the entire list.")
    print("For larger datasets, using efficient data structures like dictionaries greatly")
    print("improves performance. Further improvements could include balanced trees or")
    print("database indexing for huge datasets where sorted access is beneficial.")

if __name__ == '__main__':
    main()
