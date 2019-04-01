#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/29 3:41 PM
# author: liteng

import os
import json
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES


def create_ecc_pair(curve_type: str):
    ecc_key_pair = ECC.generate(curve=curve_type)
    return ecc_key_pair


def encode_point(is_compressed, ecc_publick_key):
    public_key_x = ecc_publick_key._point._x
    public_key_y = ecc_publick_key._point._y

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


def save_to_json(k, first_time: bool):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    path = os.path.join(path, "datas/keystore.json")
    if os.path.exists(path) and not first_time:
        with open(path, "r") as f:
            load_dict = json.load(f)
            length = len(load_dict)
            load_dict["Addr #" + str(length)] = k.to_dict()
        with open(path, "w") as f:
            json.dump(load_dict, f, indent=4)
    else:
        with open(path, "w") as f:
            json.dump({"Addr #" + "0": k.to_dict()}, f, indent=4)


def save_to_dat(k, index: int):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    dest_path = os.path.join(path, "datas/general")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with open(os.path.join(dest_path, "keystore_" + str(index) + ".dat"), "w") as f:
        json.dump(k.keystore_dat, f, sort_keys=False, indent=4, separators=(',', ':'))


def aes_encrypt(plaintext, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cbc_buffer = cbc_cipher.encrypt(plaintext)
    return cbc_buffer


def aes_decrypt(ciphertext, key, iv):
    cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    plaintext = cbc_cipher.decrypt(ciphertext)
    return plaintext


def encrypt_private_key(master_key, private_key, public_key, iv):
    decrypted_private_key = []
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



