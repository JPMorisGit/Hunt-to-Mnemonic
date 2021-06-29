from multiprocessing import Process, current_process
import multiprocessing
import secrets
import smtplib
from bip_utils import Bip44, Bip44Coins, Bip44Changes
from bloomfilter import BloomFilter
from mnemonic import Mnemonic
import sys
import time
from colorama import init, Fore, Back, Style
import argparse
init()


class email:
    host:str = 'smtp.timeweb.ru'
    port:int = 25
    password:str = '--'
    subject:str = '--- Find Mnemonic ---'
    to_addr:str = 'info@quadrotech.ru'
    from_addr:str = 'info@quadrotech.ru'
    des_mail = ''


class inf:
    version:str = ' Pulsar v3.5.0 multiT ETH'
    mnemonic_lang = ['english', 'chinese_simplified', 'chinese_traditional', 'french', 'italian', 'spanish', 'korean','japanese']
    #mnemonic_lang = ['english', 'chinese_simplified', 'french', 'spanish','japanese']
    #mnemonic_lang = ['english']
    count_44:int = 0
    process_count_work:int = 0 #количество процессов
    type_bip:int = 0
    dir_bf:str = ''
    process_time_work = 0.0
    mode = ''
    mode_text = ''
    key_found = 0


def createParser ():
    parser = argparse.ArgumentParser(description='Hunt to Mnemonic')
    parser.add_argument ('-b', '--bip', action='store', type=int, help='44', default='44')
    parser.add_argument ('-d', '--dir_bf', action='store', type=str, help='directories to BF', default='BF')
    parser.add_argument ('-t', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-m', '--mode', action='store', type=str, help='mode', default='s')
    parser.add_argument ('-c', '--desc', action='store', type=str, help='description', default='local')
    return parser.parse_args().bip, parser.parse_args().dir_bf, parser.parse_args().threading, parser.parse_args().mode, parser.parse_args().desc


def load_BF(bf_file):
    global bf_eth
    try:
        fp = open(inf.dir_bf+'/'+bf_file, 'rb')
    except FileNotFoundError:
        print('\n'+'File: '+ bf_file + ' not found.')
        sys.exit()
    else:
        if bf_file == 'eth.bf':
            bf_eth = BloomFilter.load(fp)
        print('Bloom Filter '+bf_file+' Loaded')


def send_email(text):
    email.subject = email.subject + ' description -> ' + email.des_mail
    BODY:str = '\r\n'.join(('From: %s' % email.from_addr, 'To: %s' % email.to_addr, 'Subject: %s' % email.subject, '', text)).encode('utf-8')
    server = smtplib.SMTP(email.host,email.port)
    server.login(email.from_addr, email.password)
    try:
        server.sendmail(email.from_addr, email.to_addr, BODY)
    except UnicodeError:
        print('\n'+'Error Encode UTF-8')
    finally:
        server.quit()


def save_rezult(text:str):
    try:
        f_rez = open('rezult.txt', 'a', encoding='utf-8')
    except FileNotFoundError:
        print('\n'+'File rezult.txt not found.')
    else:
        try:
            tf:str = text+'\n'
            f_rez.write(tf)
        except UnicodeError:
            print('\n'+'Error Encode UTF-8')
        finally:
            f_rez.close()


def work44(bf_eth):
    inf.count_44 = 0
    for mem in inf.mnemonic_lang:
        if inf.mode == 'r':
            seed_bytes:bytes = secrets.token_bytes(64)
        else:
            mnemo = Mnemonic(mem)
            mnemonic:str = mnemo.generate(strength=128)
            #print(mnemonic)
            seed_bytes:bytes = mnemo.to_seed(mnemonic, passphrase='')
        # ETH
        bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        bip_obj_acc = bip_obj_mst.Purpose().Coin().Account(0)
        bip_obj_chain = bip_obj_acc.Change(Bip44Changes.CHAIN_EXT)
        for nom in range(20):
            inf.count_44 = inf.count_44 + 1
            bip_obj_addr = bip_obj_chain.AddressIndex(nom)
            bip_addr:str = bip_obj_addr.PublicKey().ToAddress()
            if bip_addr in bf_eth:
                print('============== Find =================')
                bip44_PK = bip_obj_addr.PrivateKey().ToWif()
                res:str = bip_addr + ' | TRUE | ' + mnemonic + ' | ' + bip44_PK +' | BIP 44 / ETHEREUM'
                print(res)
                inf.key_found = inf.key_found + 1
                save_rezult(res)
                send_email(res)


def run44(bf_eth,process_count_work):
    try:
        ind:int = 1
        while ind > 0:
            start_time = time.time()
            work44(bf_eth)
            inf.process_time_work = time.time() - start_time
            if process_count_work == 1:
                print(Fore.YELLOW+'[*] Cycle: {:d} | Total key: {:d} | key/s: {:d} | Found {:d}'.format(ind, inf.count_44*(ind), int(inf.count_44/inf.process_time_work), inf.key_found),end='\r')
            if process_count_work > 1:
            	if multiprocessing.current_process().name == 'CPU/0':
            	    print(Fore.YELLOW+'[*] Cycle: {:d} | Total keys {:d} | Speed {:d} key/s | Found {:d} '.format(ind, inf.count_44*ind*process_count_work,int((inf.count_44/inf.process_time_work)*process_count_work),inf.key_found),flush=True,end='\r')
            ind +=1
    except KeyboardInterrupt:
        print('\n'+'Interrupted by user.')
        sys.exit()


if __name__ == "__main__":
    inf.type_bip, inf.dir_bf, inf.process_count_work, inf.mode, email.des_mail  = createParser()
    print('* Version: {} '.format(inf   .version))
    if inf.mode in ('s', 'r'):
        if (inf.mode == 's'):
            inf.mode_text = 'Standart'
        elif (inf.mode == 'r'):
            inf.mode_text = 'Random'
    else:
        print('Wrong mode selected')
        sys.exit()
    if inf.process_count_work < 1:
        print('The number of processes must be greater than 0')
        sys.exit()
    if inf.process_count_work > multiprocessing.cpu_count():
        print('The specified number of processes exceeds the allowed')
        print('FIXED for the allowed number of processes')
        inf.process_count_work = multiprocessing.cpu_count()
    if inf.type_bip != 44:
        inf.type_bip = 44
    print('* Total kernel of CPU: {} '.format(multiprocessing.cpu_count()))
    print('* Used kernel: {} '.format(inf.process_count_work))
    print('* Mode Search: BIP-{} {} '.format (inf.type_bip,inf.mode_text))
    print('* Dir database Bloom Filter: {} '.format (inf.dir_bf))
    print('* Languages at work: {} '.format(inf.mnemonic_lang))

#--------------------------------------------------
    if inf.type_bip == 44:
        print('---------------Load BF---------------')
        load_BF('eth.bf')
        print('-------------All BF loaded-----------',end='\n')
        procs = []
        try:
            for index in range(inf.process_count_work):
                proc = Process(target=run44, name= 'CPU/'+str(index), args = (bf_eth,inf.process_count_work, ))
                proc.start()
                procs.append(proc)
        except KeyboardInterrupt:
            print('\n'+'Interrupted by user.')
            sys.exit()
        try:
            for proc in procs:
                proc.join()
        except KeyboardInterrupt:
            print('\n'+'Interrupted by user.')
            sys.exit()
#--------------------------------------------------