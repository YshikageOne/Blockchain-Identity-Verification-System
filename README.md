# Blockchain Identity Verification System

A simple application that uses blockchain technology to securely store and verify identity information.

## Features

- Store identity information on a secure blockchain
- Generate cryptographic keys for identity verification
- Two verification methods: simple lookup and secure challenge-response
- Blockchain data is saved between application sessions
- View and validate the blockchain with an explorer interface

## Requirements

- Python 3.8+
- Required packages: `pycryptodome`, `tkcalendar`

## Installation

```bash
# Install required packages
pip install pycryptodome tkcalendar

# Run the application
python main.py
```

## How to Use

### Register an Identity

1. Go to the "Register Identity" tab
2. Fill in your information
3. Click "Register Identity"
4. Save your private key when prompted

### Verify an Identity

1. Go to the "Verify Identity" tab
2. Enter the Identity ID
3. Choose verification method:
   - Simple Verification: Just checks if ID exists
   - Challenge-Response: Requires private key for security
4. Click "Verify Identity"

### View the Blockchain

1. Go to the "Blockchain Explorer" tab
2. Browse all identity records
3. Use "Validate Blockchain Integrity" to check if data is intact

## How It Works

- The system creates a chain of blocks to store identity data
- Each block is cryptographically linked to the previous one
- RSA encryption is used for secure identity verification
- All data is saved to disk when the application closes

## Project Files

- `main.py` - Program entry point
- `UI.py` - User interface code
- `MainFunctions.py` - Core functionality
- `Blockchain.py` - Blockchain implementation
- `Block.py` - Individual block structure
- `IdentityManager.py` - Cryptographic functions

## License

MIT License
