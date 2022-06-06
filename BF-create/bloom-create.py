# !/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""
version = '2.3'

from sys import argv
from os import system, path, name
from time import time
from datetime import datetime
from logging import getLogger, INFO, FileHandler, DEBUG
from logging import Formatter
from filter import BloomFilter
from secp256k1_lib import bech32_address_decode, address_to_h160, COIN_LTC

current_path = path.dirname(path.realpath(__file__))
logger_info = getLogger('INFO')
logger_info.setLevel(INFO)
handler_info = FileHandler(path.join(current_path, 'info.log'), 'w' , encoding ='utf-8')
handler_info.setFormatter(Formatter(fmt='%(message)s'))
logger_info.addHandler(handler_info)

logger_err = getLogger('ERROR')
logger_err.setLevel(DEBUG)
handler_err = FileHandler(path.join(current_path, 'error.log'), 'w' , encoding ='utf-8')
handler_err.setFormatter(Formatter(fmt='%(message)s'))
logger_err.addHandler(handler_err)

def cls():
    system('cls' if name=='nt' else 'clear')

def count_lines(file):
    return sum(1 for line in open(file, 'r'))

def date_str():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def convert(line_count,file_in,file_out):
    bech_ = 0
    base_ = 0
    eth_ = 0
    eth_0x = 0
    line_10 = 100000
    count = 0
    err= 0
    lis = []
    bloom_filter = BloomFilter(size=line_count, fp_probability=1e-12)
    print(f"[I] Start create list ...")
    st = time()
    with open(file_in, "r") as f:
        for line in f:
            res = line.strip()
            if res[:2] == '0x':
                bloom_filter.add(res.lower()[2:])
                eth_0x += 1
                #logger_info.info(res.lower()[2:])
                eth_ += 1
            elif len(res) == 40:
                bloom_filter.add(res.lower())
                #logger_info.info(res.lower())
                eth_ += 1
            elif res[:2] == 'bc' and len(res) >= 35 and len(res) <= 50:
                h160 = bech32_address_decode(res)
                bloom_filter.add(h160)
                #logger_info.info(h160)
                bech_ += 1
            elif res[:2] == 'lt' and len(res) >= 35 and len(res) <= 50:
                h160 = bech32_address_decode(res, COIN_LTC)
                bloom_filter.add(h160)
                #logger_info.info(h160)
                bech_ += 1
            elif len(res) <= 35 and res[:2] != 's-' and res[:2] != 'm-' and res[:2] != 'd-':
                h160 = address_to_h160(res)
                bloom_filter.add(h160)
                #logger_info.info(h160)
                base_ += 1
            elif res[:2] == 's-' or res[:2] == 'm-' and res[:2] == 'd-':
                logger_err.error(f'Error convert: {res}')
                err += 1
            else:
                #print(f'Error convert: {res}')
                logger_err.error(f'Error convert: {res}')
                err += 1

            count += 1
            if count == line_10:
                print(f"> error: {err} | ETH 0x: {eth_0x}| ETH/H160: {eth_} | bech32: {bech_} | base58:{base_} | total: {count}",end='\r')
                line_10 +=100000
    print('\n')
    print(f"[I] Finish create list ... ({time()-st:.2f} sec) | Total line: {len(lis)}")
    print(f"[I] Start create Bloom Filter: {date_str()} ...")
    st = time()
    with open(file_out, "wb") as fp:
        bloom_filter.save(fp)
    print(f"[I] Finish create Bloom filter ... ({time()-st:.2f} sec)")
    print(f"[END] error: {err} | ETH 0x: {eth_0x}| ETH/H160: {eth_} | bech32: {bech_} | base58:{base_} | total: {count}",end='\r')
    print('\n')

if __name__ == "__main__":
    cls()
    file_in = argv[1]
    file_out = argv[2]
    if len (argv) < 3:
        print ("[E] Error. Too few options.")
        logger_err.error("[E] Error. Too few options.")
        exit(1)

    if len (argv) > 3:
        print ("[E] Error. Too many parameters.")
        logger_err.error("[E] Error. Too many parameters.")
        exit(1)
    print(f"[I] Start line count ...")
    line_count = count_lines(file_in)
    print(f"[I] Finish line count ...")
    print('-'*70,end='\n')
    print(f'[I] Version: {version}')
    print(f'[I] File address : {file_in}')
    print(f'[I] Bloom Filter : {file_out}')
    print(f'[I] Total lines : {line_count}')
    print(f'[I] START: {date_str()}')
    print('-'*70,end='\n')
    convert(line_count,file_in,file_out)
    