#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

from consts import *

def convert_int(num:int):
    dict_suffix = {0:'Key', 1:'KKey', 2:'MKey', 3:'GKey', 4:'TKey', 5:'PKey', 6:'EKeys'}
    num *= 1.0
    idx = 0
    for ii in range(len(dict_suffix)-1):
        if int(num/1000) > 0:
            idx += 1
            num /= 1000
    return ('%.2f'%num), dict_suffix[idx]
    
def load_BF(load):
    try:
        fp = open(load, 'rb')
    except FileNotFoundError:
        print(f'{red}[E] File: {load} not found.')
        logger_err.error(f'[E] File: {load} not found.')
        sys.exit()
    else:
        n_int = int(multiprocessing.current_process().name)
        time.sleep(inf.delay*n_int)
        return BloomFilter.load(fp)

def b32(seed, fc):
    co = 0
    bip = BIP32.from_seed(seed)
    for path in inf.l32:
        for num in range(10):
            patchs = f"{path}{num}"
            pvk = bip.get_privkey_from_path(patchs)
            pvk_int = int(pvk.hex(),16)
            bip_h160_c = privatekey_to_h160(0, True, pvk_int)
            bip_h160_uc = privatekey_to_h160(0, False, pvk_int)
            #----------------------------------------------------------------    
            if bip_h160_c.hex() in inf.bf_btc or bip_h160_uc.hex() in inf.bf_btc:
                addr_c = hash_to_address(0,False,bip_h160_c)
                addr_uc = hash_to_address(0,True,bip_h160_uc)
                print(f'\n[F][Mode 32] Found address: seed:{hex(seed)} | PVK compress:{btc_pvk_to_wif(pvk_int,True)} - {addr_c} | PVK uncompress:{btc_pvk_to_wif(pvk_int,False)} - {addr_uc}')
                logger_found.info(f'[F][Mode 32] Found address: seed:{hex(seed)} | PVK compress:{btc_pvk_to_wif(pvk_int,True)} - {addr_c} | PVK uncompress:{btc_pvk_to_wif(pvk_int,False)} - {addr_uc}')
                fc.increment(1)
            co += 2
    return co

def bETH(seed, fc):
    co = 0
    bip = BIP32.from_seed(seed)
    for nom2 in range(1):#accaunt
        for nom3 in range(2):#in/out
            for nom in range(20):
                patchs = f"m/44'/60'/{nom2}'/{nom3}/{nom}"
                pvk = bip.get_privkey_from_path(patchs)
                pvk_int = int(pvk.hex(),16)
                addr = privatekey_to_ETH_address(pvk_int)
                if addr in inf.bf_eth:
                    print(f'\n[F][Mode ETH] Found address: {seed.hex()} | PVK compress:{btc_pvk_to_wif(pvk_int,True)} - addr:0x{addr}')
                    logger_found.info(f'[F][Mode ETH] Found address: {seed.hex()} | PVK compress:{btc_pvk_to_wif(pvk_int,True)} - addr:0x{addr}')
                    fc.increment(1)
                co += 1
    return co

def bBTC(seed, fc):
    co = 0
    bip = BIP32.from_seed(seed)
    for nom3 in range(2):
        for nom in range(10):
            patchs = f"m/44'/0'/0'/{nom3}/{nom}"
            pvk = bip.get_privkey_from_path(patchs)
            pvk_int = int(pvk.hex(),16)
            bip_h160_c = privatekey_to_h160(0, True, pvk_int)
            bip_h160_uc = privatekey_to_h160(0, False, pvk_int)
            if bip_h160_c.hex() in inf.bf_btc or bip_h160_uc.hex() in inf.bf_btc:
                addr_c = hash_to_address(0,False,bip_h160_c)
                addr_uc = hash_to_address(0,True,bip_h160_uc)
                print(f'\n[F][Mode BTC] Found address: seed:{hex(seed)} | PVK compress:{btc_pvk_to_wif(pvk_int,True)} - {addr_c} | PVK uncompress:{btc_pvk_to_wif(pvk_int,False)} - {addr_uc}')
                logger_found.info(f'[F][Mode BTC] Found address: seed:{hex(seed)} |  PVK compress:{btc_pvk_to_wif(pvk_int,True)} - {addr_c} | PVK uncompress:{btc_pvk_to_wif(pvk_int,False)} - {addr_uc}')
                fc.increment(1)
            co += 2
    return co