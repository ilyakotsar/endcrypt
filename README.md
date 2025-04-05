# EndCrypt

Desktop application for end-to-end message encryption.

## Installation

1. Download [EndCrypt](https://github.com/ilyakotsar/endcrypt/archive/refs/heads/main.zip) and unzip it
2. Install [Python](https://www.python.org/downloads/)
3. Run install.bat
4. Run EndCrypt.bat

## Usage

1. Open “Initiate exchange”, adjust the parameters, set a password, create a configuration and send it to your interlocutor.
2. Your interlocutor should open “Accept exchange”, insert your configuration, set a password, create a configuration and send it to you.
3. Open “Encrypt / Decrypt” to encrypt and decrypt messages.

## Algorithm

1. SHAKE256 to convert a password to a private key
2. Diffie-hellman key exchange to get a shared key
3. Argon2id to get the encryption key
4. AES-256 (CBC) for text encryption

## Requirements

- [cryptography](https://github.com/pyca/cryptography)
- [Flask](https://github.com/pallets/flask)
