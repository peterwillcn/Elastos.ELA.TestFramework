#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/29 3:41 PM
# author: liteng

import os
import json
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


def create_ecc_pair(curve_type: str):
    while True:
        ecc_key_pair = ECC.generate(curve=curve_type)
        private_key = ecc_key_pair.d.to_bytes()
        if len(private_key) == 32:
            break
    return ecc_key_pair


def encode_point(is_compressed, ecc_public_key):
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


def encode_point2(is_compressed, public_key_point):
    public_key_x = public_key_point.x()
    public_key_y = public_key_point.y()

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
        y_bytes = public_key_y.to_bytes(32, byteorder="big")
        for i in range(65 - len(y_bytes), 65):
            encoded_data[i] = y_bytes[i - 65 + len(y_bytes)]

    x_bytes = public_key_x.to_bytes(32, byteorder="big")
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


def save_to_json(k, prefix: str, dest_path: str, first_time: bool):

    if os.path.exists(dest_path) and not first_time:
        with open(dest_path, "r") as f:
            load_dict = json.load(f)
            load_dict[prefix] = k.to_dict()
        with open(dest_path, "w", buffering=1) as f:
            json.dump(load_dict, f, indent=4)
    else:
        with open(dest_path, "w",buffering=1) as f:
            json.dump({prefix: k.to_dict()}, f, indent=4)


def save_to_dat(keystore_dat: dict, dat_file_path: str):
    with open(dat_file_path, "w", buffering=1) as f:
        json.dump(keystore_dat, f, sort_keys=False, indent=4, separators=(',', ':'))


def aes_encrypt(plaintext, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cbc_buffer = cbc_cipher.encrypt(plaintext)
    return cbc_buffer


def aes_decrypt(ciphertext, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    plaintext = cbc_cipher.decrypt(ciphertext)
    return plaintext


def encrypt_private_key(master_key, private_key, public_key, iv):
    decrypted_private_key = list()
    for i in range(96):
        decrypted_private_key.append(bytes(0x00))
    public_key_bytes = encode_point(False, public_key)

    for i in range(64):
        decrypted_private_key[i] = public_key_bytes[i + 1]
    for i in range(len(private_key)):
        decrypted_private_key[64 + i] = private_key[i]
    # print("@@@ de: ", decrypted_private_key)
    decrypted_private_key_bytes = bytes(decrypted_private_key)
    # print("@@@ be: ", decrypted_private_key_bytes)
    encrypted_private_key = aes_encrypt(decrypted_private_key_bytes, master_key, iv)
    return encrypted_private_key


def create_urandom(count: int):
    return os.urandom(count)


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


def program_hash_to_address(program_hash):
    data = program_hash
    double_value = sha256_hash(data, 2)
    flag = double_value[0:4]
    data = data + flag
    encoded = base58.b58encode(data)
    return encoded.decode()


def address_to_program_hash(address: str):
    if len(address) != 34:
        return None

    decoded = base58.b58decode(bytes(address.encode()))
    program_hash = decoded.hex()[:42]
    address2 = program_hash_to_address(bytes.fromhex(program_hash))
    if address2 != address:
        return None

    return bytes.fromhex(program_hash)


def gen_deposit_address(program_hash: bytes):
    if program_hash[0] != PREFIX_STANDARD:
        return None

    prefix = PREFIX_DEPOSIT.to_bytes(1, byteorder="big", signed=False)
    deposit_hash = prefix + program_hash[1:]
    deposit_encoded = program_hash_to_address(deposit_hash)
    return deposit_encoded


def gen_cross_chain_address(genesis_hash: bytes):
    reverse_hash = genesis_hash[::-1]
    r = b""
    r += struct.pack("<B", len(reverse_hash))
    r += reverse_hash
    r += struct.pack("<B", 0xAF)
    once_hash = sha256_hash(r, 1)
    r_hash = ripemd160_hash(once_hash, 1)
    program_hash = PREFIX_CROSS_CHAIN.to_bytes(1, byteorder="big") + r_hash
    cross_address = program_hash_to_address(program_hash)

    return cross_address


if __name__ == '__main__':

    genesis_hash = bytes.fromhex("56be936978c261b2e649d58dbfaf3f23d4a868274f5522cd2adb4308a955c4a3")
    gen_cross_chain_address(genesis_hash)

    a = "0000000000000000000000"
    address = program_hash_to_address(bytes.fromhex(a))
    # program_hash = bytes.fromhex("218cb669c4c446b82bb12dfab4eee3555c5d52260f")
    # deposit_address = gen_deposit_address(program_hash)
    # print("deposit address",  deposit_address)
    #
    # program = address_to_program_hash(deposit_address)
    # print("program1: ", program_hash.hex())
    # print("program2: ", program.hex())
