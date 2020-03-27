#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/22 10:37 AM
# author: liteng

import os
import struct
import random
import base58

from ecdsa import ecdsa
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES

PREFIX_STANDARD = 0x21
PREFIX_MULTI_SIGN = 0x12
PREFIX_CROSS_CHAIN = 0x4B
PREFIX_DEPOSIT = 0x1F


def create_urandom(count: int):
    return os.urandom(count)


def create_ecc_pair(curve_type: str):
    while True:
        ecc_key_pair = ECC.generate(curve=curve_type)
        private_key = ecc_key_pair.d.to_bytes()
        if len(private_key) == 32:
            break
    return ecc_key_pair


def create_redeem_script(public_key: bytes):
    return bytes([len(public_key)]) + public_key + bytes([0xac])


def create_did_redeem_script(public_key: bytes):
    return bytes([len(public_key)]) + public_key + bytes([0xad])


def create_program_hash(redeem_script: bytes):
    temp = sha256_hash(redeem_script, 1)
    data = ripemd160_hash(temp, 1)
    sign_type = redeem_script[len(redeem_script) - 1]
    program_hash = None
    if sign_type == 0xac:
        program_hash = bytes([33]) + data
    if sign_type == 0xae:
        program_hash = bytes([18]) + data
    return program_hash


def create_id_program_hash(redeem_script: bytes):
    temp = sha256_hash(redeem_script, 1)
    data = ripemd160_hash(temp, 1)
    # sign_type = redeem_script[len(redeem_script) - 1]
    program_hash = bytes([0x67]) + data
    return program_hash


def create_address(program_hash: bytes):
    data = program_hash
    double_value = sha256_hash(data, 2)
    flag = double_value[0:4]
    data = data + flag
    encoded = base58.b58encode(data)
    return encoded.decode()


def create_deposit_address(program_hash: bytes):
    if program_hash[0] != PREFIX_STANDARD:
        return None

    prefix = PREFIX_DEPOSIT.to_bytes(1, byteorder="big", signed=False)
    deposit_hash = prefix + program_hash[1:]
    deposit_encoded = create_address(deposit_hash)
    return deposit_encoded


def create_cross_chain_address(genesis_hash: bytes):
    reverse_hash = genesis_hash[::-1]
    r = b""
    r += struct.pack("<B", len(reverse_hash))
    r += reverse_hash
    r += struct.pack("<B", 0xAF)
    once_hash = sha256_hash(r, 1)
    r_hash = ripemd160_hash(once_hash, 1)
    program_hash = PREFIX_CROSS_CHAIN.to_bytes(1, byteorder="big") + r_hash
    cross_address = create_address(program_hash)

    return cross_address


def address_to_program_hash(address: str):
    if len(address) != 34:
        return None

    decoded = base58.b58decode(bytes(address.encode()))
    program_hash = decoded.hex()[:42]
    address2 = create_address(bytes.fromhex(program_hash))
    if address2 != address:
        return None

    return bytes.fromhex(program_hash)


def encode_point(ecc_public_key, is_compressed: bool):
    public_key_x = ecc_public_key._point._x
    public_key_y = ecc_public_key._point._y

    if public_key_x is None or public_key_y is None:
        infinity = []
        for i in range(1):
            infinity.append(0x00)
        return infinity
    encoded_data = []
    if is_compressed:
        for i in range(33):
            encoded_data.append(0x00)
    else:
        for i in range(65):
            encoded_data.append(0x00)
        y_bytes = public_key_y.to_bytes()
        for i in range(65 - len(y_bytes), 65):
            encoded_data[i] = y_bytes[i - 65 + len(y_bytes)]

    x_bytes = public_key_x.to_bytes()
    x_len = len(x_bytes)
    for i in range(33 - x_len, 33):
        encoded_data[i] = x_bytes[i - 33 + x_len]

    if is_compressed:
        if public_key_y % 2 == 0:
            encoded_data[0] = 0x02
        else:
            encoded_data[0] = 0x03
    else:
        encoded_data[0] = 0x04
    return bytes(encoded_data)


def encrypt_private_key(master_key, private_key, public_key, iv):
    decrypted_private_key = list()
    for i in range(96):
        decrypted_private_key.append(bytes(0x00))
    public_key_bytes = encode_point(public_key, False)

    for i in range(64):
        decrypted_private_key[i] = public_key_bytes[i + 1]
    for i in range(len(private_key)):
        decrypted_private_key[64 + i] = private_key[i]
    decrypted_private_key_bytes = bytes(decrypted_private_key)
    encrypted_private_key = aes_encrypt(decrypted_private_key_bytes, master_key, iv)
    return encrypted_private_key


def sha256_hash(data_bytes, times: int):
    if times == 0:
        return data_bytes
    hash_value = SHA256.new(data_bytes)
    hash_value_bytes = hash_value.digest()
    times = times - 1
    return sha256_hash(hash_value_bytes, times)


def ripemd160_hash(data_bytes, times: int):
    if times == 0:
        return data_bytes
    hash_value = RIPEMD160.new(data_bytes)
    hash_value_bytes = hash_value.digest()
    times = times - 1
    return ripemd160_hash(hash_value_bytes, times)


def get_ecc_by_private_key(private_key_str: str):
    return ECC.construct(curve='P-256', d=int(private_key_str, 16))


def aes_encrypt(plaintext, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cbc_buffer = cbc_cipher.encrypt(plaintext)
    return cbc_buffer


def aes_decrypt(cipher_text, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    plaintext = cbc_cipher.decrypt(cipher_text)
    return plaintext


def ecdsa_sign(private_key: bytes, data: bytes):
    data_hash = sha256_hash(data, 1)

    g = ecdsa.generator_256
    n = g.order()

    randrange = random.SystemRandom().randrange
    secret = int.from_bytes(private_key, byteorder="big", signed=False)
    digest = int.from_bytes(data_hash, byteorder="big", signed=False)
    pub_key = ecdsa.Public_key(g, g * secret)
    pri_key = ecdsa.Private_key(pub_key, secret)

    signature = pri_key.sign(digest, randrange(1, n))
    r = signature.r.to_bytes(32, byteorder="big", signed=False)
    s = signature.s.to_bytes(32, byteorder="big", signed=False)
    b = r + s

    return b


def ecdsa_verify(private_key: bytes, data: bytes, signature: bytes):
    if len(signature) != 64:
        return False

    r = int.from_bytes(signature[:32], byteorder="big", signed=False)
    s = int.from_bytes(signature[32:], byteorder="big", signed=False)
    data_hash = sha256_hash(data, 1)
    g = ecdsa.generator_256

    secret = int.from_bytes(private_key, byteorder="big", signed=False)
    digest = int.from_bytes(data_hash, byteorder="big", signed=False)
    pub_key = ecdsa.Public_key(g, g * secret)
    sig = ecdsa.Signature(r, s)
    b = pub_key.verifies(digest, sig)

    return b
