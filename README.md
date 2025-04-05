# EndCrypt

Desktop application for end-to-end message encryption.

## Installation

1. Download [EndCrypt](https://github.com/ilyakotsar/endcrypt/archive/refs/heads/main.zip) and unzip it
2. Install [Python](https://www.python.org/)
3. Run install.bat
4. Run EndCrypt.bat

## Usage

1. Open “Initiate exchange”, adjust the parameters, set a password, create a configuration and send it to your interlocutor.
2. Your interlocutor should open “Accept exchange”, insert your configuration, set a password, create a configuration and send it to you.
3. Open “Encrypt / Decrypt” to encrypt and decrypt messages.

## Algorithms

Diffie-hellman key exchange, Argon2id, AES-256 (CBC), SHAKE256 to convert password to private key.

## Requirements

- [cryptography](https://github.com/pyca/cryptography)
- [Flask](https://github.com/pallets/flask)
