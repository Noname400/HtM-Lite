# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
@testWords: world evolve cry outer garden common differ jump few diet cliff lumber
"""


from secp256k1_lib import privatekey_to_ETH_address, privatekey_to_h160, hash_to_address, btc_pvk_to_wif
from bip32 import BIP32
from colorama import Back, Fore, Style, init
from mnemonic import Mnemonic
from multiprocessing import Lock, Process, Value
import logging
from logging import Formatter
import argparse, ctypes, datetime
import multiprocessing
import os, sys, time
from filter import BloomFilter
init(autoreset = True)

yellow = Fore.YELLOW+Style.BRIGHT
red = Fore.RED+Style.BRIGHT
clear = Style.RESET_ALL
green = Fore.GREEN+Style.BRIGHT

current_path = os.path.dirname(os.path.realpath(__file__))
logger_found = logging.getLogger('FOUND')
logger_found.setLevel(logging.INFO)
handler_found = logging.FileHandler(os.path.join(current_path, 'found.log'), 'a' , encoding ='utf-8')
handler_found.setFormatter(Formatter(fmt='[%(asctime)s:] %(message)s'))
logger_found.addHandler(handler_found)

logger_info = logging.getLogger('INFO')
logger_info.setLevel(logging.INFO)
handler_info = logging.FileHandler(os.path.join(current_path, 'info.log'), 'a' , encoding ='utf-8')
handler_info.setFormatter(Formatter(fmt='[%(asctime)s:] %(message)s'))
logger_info.addHandler(handler_info)

logger_err = logging.getLogger('ERROR')
logger_err.setLevel(logging.DEBUG)
handler_err = logging.FileHandler(os.path.join(current_path, 'error.log'), 'w' , encoding ='utf-8')
handler_err.setFormatter(Formatter(fmt='[%(asctime)s:] %(message)s'))
logger_err.addHandler(handler_err)

class Counter:
    def __init__(self, initval=0):
        self.val = Value(ctypes.c_longlong, initval)
        self.lock = Lock()
    def increment(self, nom):
        with self.lock:
            self.val.value += nom
    def decrement(self, nom):
        with self.lock:
            self.val.value -= nom
    def zero(self):
        with self.lock:
            self.val.value = 0
    def value(self):
        with self.lock:
            return self.val.value

class inf:
    version:str = '* Pulsar Lite v1.6.1 *'
    #general
    th:int = 1 #number of processes
    db_btc:str = ''
    bf_btc:BloomFilter
    db_eth:str = ''
    bf_eth:BloomFilter
    l32:list = ["m/0'/0'/", "m/44'/0'/0'/", "m/0'/0/"]
    bip:str = 'BTC'
    count:int = 1
    count_nem = 0
    dt_now:str = ''
    delay:int = 5
    work_time:float = 0.0