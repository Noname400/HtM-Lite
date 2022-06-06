# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
"""

from funcP import *
from consts import *

def createParser ():
    parser = argparse.ArgumentParser(description='Hunt to Mnemonic')
    parser.add_argument ('-b', '--bip', action='store', type=str, help='ETH/BTC/combo default Mode BTC', default='BTC')
    parser.add_argument ('-dbbtc', '--databasebtc', action='store', type=str, help='File BF BTC', default='')
    parser.add_argument ('-dbeth', '--databaseeth', action='store', type=str, help='File BF ETH', default='')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-sl', '--sleep', action='store', type=int, help='pause start (sec)', default='5')
    return parser.parse_args().bip, parser.parse_args().databasebtc, parser.parse_args().databaseeth, parser.parse_args().threading, parser.parse_args().sleep

def run(*args):
    inf.bip = args[0]
    inf.db_btc = args[1]
    inf.db_eth = args[2]
    inf.th = args[3]
    inf.delay = args[4]
    total_counter = args[5]
    process_counter = args[6]
    found_counter = args[7]
    mnem_counter = args[8]


    tc = 0
    ind:int = 1
    if inf.bip == 'BTC' or inf.bip == '32': 
        inf.bf_btc = load_BF(inf.db_btc)
        process_counter.increment(1)
    elif inf.bip == 'ETH': 
        inf.bf_eth = load_BF(inf.db_eth)
        process_counter.increment(1)
        
    try:
        while True:
            mnemo = Mnemonic("english")
            words = mnemo.generate(strength=128) #world evolve cry outer garden common differ jump few diet cliff lumber
            seed = mnemo.to_seed(words, passphrase="")
            start_time = time.time()
            if inf.bip == '32': 
                total_counter.increment(b32(seed,found_counter))
                mnem_counter.increment(1)
            if inf.bip == "ETH": 
                total_counter.increment(bETH(seed, found_counter))
                mnem_counter.increment(1)
            if inf.bip == "BTC": 
                total_counter.increment(bBTC(seed,found_counter))
                mnem_counter.increment(1)
            pc = process_counter.value()
            mc = mnem_counter.value()
            fc = found_counter.value()
            st = time.time() - start_time
            ftc = tc
            tc = total_counter.value()
            tc = tc
            tc_float, tc_hash = convert_int(tc)
            btc = tc - ftc
            speed = int((btc/st))
            speed_float, speed_hash = convert_int(speed)

            if multiprocessing.current_process().name == '0':
                print(f'{yellow}> Cores:{pc} | Mnemonic:{mc} | MNEM:{tc_float} {tc_hash} | Speed:{speed_float} {speed_hash}/sec | Found:{fc}',end='\r')
            inf.count = 0
            ind += 1

                
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        exit()

if __name__ == "__main__":
    inf.bip, inf.db_btc, inf.db_eth, inf.th, inf.delay  = createParser()
    print('-'*70,end='\n')
    print(f'{green}Thank you very much: @iceland2k14 for his libraries!')
    
    if inf.bip in ('ETH', 'BTC', '32'):
        pass
    else:
        print(f'{red}[E] Wrong BIP selected')
        logger_err.error(('[E] Wrong BIP selected'))
        exit()

    if inf.th < 1:
        print(f'{red}[E] The number of processes must be greater than 0')
        logger_err.error(('[E] The number of processes must be greater than 0'))
        exit()

    if inf.th > multiprocessing.cpu_count():
        print(f'{red}[I] The specified number of processes exceeds the allowed')
        print(f'{green}[I] FIXED for the allowed number of processes')
        inf.th = multiprocessing.cpu_count()

    print('-'*70,end='\n')
    print(f'[I] Version: {inf.version}')
    logger_info.info(f'Start HtM Lite version {inf.version}')
    print(f'[I] Total kernel of CPU: {multiprocessing.cpu_count()}')
    print(f'[I] Used kernel: {inf.th}')
    print(f'[I] Mode Search: BIP-{inf.bip}')
    logger_info.info(f'[I] Mode Search: BIP-{inf.bip}')
    if inf.bip == 'ETH': print(f'[I] Bloom Filter ETH: {inf.db_eth}')
    else: print(f'[I] Bloom Filter BTC: {inf.db_btc}')
    print(f'[I] Smooth start {inf.delay} sec')
    print('-'*70,end='\n')
    
    total_counter = Counter(0)
    process_counter = Counter(0)
    found_counter = Counter(0)
    mnem_counter = Counter(0)
    
    procs = []
    try:
        for r in range(inf.th): 
            p = Process(target=run, name= str(r), args=(inf.bip, inf.db_btc, inf.db_eth, inf.th, \
                inf.delay, total_counter, process_counter, found_counter, mnem_counter,))
            procs.append(p)
            p.start()
        for proc in procs: proc.join()
    except(KeyboardInterrupt, SystemExit):
        print('\n[EXIT] Interrupted by the user.')
        logger_info.info('[EXIT] Interrupted by the user.')
        exit()