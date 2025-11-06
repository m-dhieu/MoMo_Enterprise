# MoMo SMS Transactions REST API Documentation

## Authentication
- Uses Basic Authentication
- Use valid username and password with each request
- Unauthorized requests return 401 status

---

## Endpoints

### GET /transactions
- Description: Retrieves a list of all transactions
- Request:
  ```
  curl -u admin:password http://localhost:8090/transactions
  ```
- Response:
  ```
  [
    {
      "TransactionID": 1,
      "TransactionType": "deposit",
      "Amount": 10000,
      "Currency": "RWF",
      "DateTime": "2025-09-27 14:00:00",
      "ReferenceNumber": "TX12345",
      "BalanceAfterTransaction": 15000,
      "Status": "confirmed",
      "MessageText": "Deposit 10000 RWF",
      "Participants": [ ... ]
    },
    ...
  ]
  ```
- Errors:
  - 401 Unauthorized: Missing/invalid credentials

---

### GET /transactions/{id}
- Description: Retrieves one transaction by ID
- Request:
  ```
  curl -u admin:password http://localhost:8090/transactions/1
  ```
- Response:
  ```
  {
    "TransactionID": 1,
    "TransactionType": "deposit",
    "Amount": 10000,
    ...
  }
  ```
- Errors:
  - 400 Bad Request: Invalid ID format
  - 404 Not Found: Transaction ID does not exist
  - 401 Unauthorized: Missing/invalid credentials

---

### POST /transactions
- Description: Adds a new transaction
- Request:
  ```
  curl -u admin:password -X POST http://localhost:8090/transactions \
  -H "Content-Type: application/json" \
  -d '{"TransactionType":"payment","Amount":500,"Currency":"RWF","DateTime":"2025-09-27 15:20:00", ... }'
  ```
- Response:
  - 201 Created: Returns created transaction JSON
- Errors:
  - 400 Bad Request: Malformed JSON
  - 401 Unauthorized: Missing/invalid credentials

---

### PUT /transactions/{id}
- Description: Updates existing transaction
- Request:
  ```
  curl -u admin:password -X PUT http://localhost:8090/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{...updated transaction JSON...}'
  ```
- Response:
  - 200 OK: Returns updated transaction JSON
- Errors:
  - 400 Bad Request: Invalid ID or JSON
  - 404 Not Found: Transaction ID does not exist
  - 401 Unauthorized: Missing/invalid credentials

---

### DELETE /transactions/{id}
- Description: Deletes a transaction
- Request:
  ```
  curl -u admin:password -X DELETE http://localhost:8090/transactions/1
  ```
- Response:
  - 200 OK: Confirmation message with deleted transaction
- Errors:
  - 400 Bad Request: Invalid ID
  - 404 Not Found: Transaction ID does not exist
  - 401 Unauthorized: Missing/invalid credentials
```
