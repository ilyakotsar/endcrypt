import base64
import os
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from flask import Flask, request, render_template


def generate_dh_p(g: int, key_size: int) -> int:
    parameters = dh.generate_parameters(g, key_size)
    numbers = parameters.parameter_numbers()
    p = numbers.p
    return p


def generate_salt_b64() -> str:
    salt = os.urandom(32)
    salt_b64 = base64.b64encode(salt).decode()
    return salt_b64


def get_private_key(password: str, p: int) -> int:
    digest_size = p.bit_length() // 8
    digest = hashes.Hash(hashes.SHAKE256(digest_size))
    digest.update(password.encode())
    hash = digest.finalize()
    private_key = int.from_bytes(hash)
    return private_key


def get_public_key(g: int, private_key: int, p: int) -> int:
    public_key = pow(g, private_key, p)
    return public_key


def get_shared_key(inter_public_key: int, private_key: int, p: int) -> int:
    shared_key = pow(inter_public_key, private_key, p)
    return shared_key


def get_encryption_key(
        salt_b64: str,
        iterations: int,
        memory: int,
        parallelism: int,
        shared_key: int,
    ) -> bytes:
    salt = base64.b64decode(salt_b64)
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=iterations,
        lanes=parallelism,
        memory_cost=memory * 1024,
    )
    key = kdf.derive(str(shared_key).encode())
    return key


def encrypt_text(plaintext: str, key: bytes) -> tuple[str, str]:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    iv_b64 = base64.b64encode(iv).decode()
    ciphertext_b64 = base64.b64encode(ciphertext).decode()
    return iv_b64, ciphertext_b64


def decrypt_text(iv_b64: str, ciphertext_b64: str, key: bytes) -> str:
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext.decode()


app = Flask(__name__)


@app.get('/')
def home():
    return render_template('home.html')


@app.route('/1', methods=['GET', 'POST'])
def initiate_exchange():
    if request.method == 'POST':
        key_size = int(request.form['key_size'])
        g = int(request.form['g'])
        iterations = request.form['iterations']
        memory = request.form['memory']
        parallelism = request.form['parallelism']
        password = request.form['password']
        p = generate_dh_p(g, key_size)
        private_key = get_private_key(password, p)
        public_key = get_public_key(g, private_key, p)
        salt = generate_salt_b64()
        conf_list = ['A', salt, iterations, memory, parallelism]
        conf_list.extend([str(g), str(p), str(public_key)])
        conf = '_'.join(conf_list)
        context = {
            'key_size': key_size,
            'g': g,
            'iterations': iterations,
            'memory': memory,
            'parallelism': parallelism,
            'password': password,
            'conf': conf,
        }
        return render_template('initiate_exchange.html', **context)
    context = {
        'key_size': 2048,
        'g': 2,
        'iterations': 30,
        'memory': 120,
        'parallelism': 6,
    }
    return render_template('initiate_exchange.html', **context)


@app.route('/2', methods=['GET', 'POST'])
def accept_exchange():
    if request.method == 'POST':
        conf_a = request.form['conf_a']
        password = request.form['password']
        conf_a_list = conf_a.split('_')
        g = int(conf_a_list[5])
        p = int(conf_a_list[6])
        private_key = get_private_key(password, p)
        public_key = get_public_key(g, private_key, p)
        conf_a_list[0] = 'B'
        conf_a_list[7] = str(public_key)
        conf_b = '_'.join(conf_a_list)
        context = {
            'conf_a': conf_a,
            'password': password,
            'conf_b': conf_b,
        }
        return render_template('accept_exchange.html', **context)
    return render_template('accept_exchange.html')


@app.route('/3', methods=['GET', 'POST'])
def encrypt_decrypt():
    if request.method == 'POST':
        conf = request.form['conf']
        password = request.form['password']
        input_text = request.form['input_text']
        operation = request.form['operation']
        conf_list = conf.split('_')
        salt = conf_list[1]
        iterations = int(conf_list[2])
        memory = int(conf_list[3])
        parallelism = int(conf_list[4])
        p = int(conf_list[6])
        inter_public_key = int(conf_list[7])
        private_key = get_private_key(password, p)
        shared_key = get_shared_key(inter_public_key, private_key, p)
        key = get_encryption_key(salt, iterations, memory, parallelism, shared_key)
        if operation == 'encrypt':
            iv, ciphertext = encrypt_text(input_text, key)
            if conf_list[0] == 'A':
                user = 'B'
            else:
                user = 'A'
            output_text = '_'.join([user, iv, ciphertext])
        elif operation == 'decrypt':
            input_text_list = input_text.split('_')
            iv = input_text_list[1]
            ciphertext = input_text_list[2]
            output_text = decrypt_text(iv, ciphertext, key)
        context = {
            'conf': conf,
            'password': password,
            'input_text': input_text,
            'operation': operation,
            'output_text': output_text,
        }
        return render_template('encrypt_decrypt.html', **context)
    return render_template('encrypt_decrypt.html', operation='encrypt')
