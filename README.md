# mnemonic-colider-2 HASH160
Brute Force Bitcoin address
Программа создана в первую очередь для изучения языка PYTHON! 

В чем разница от первой версии?  
в этой версии ведется поиск по HASH160, то есть мы убираем одно конвертирование (hash160 в адрес)  
это позволяет объединить все в один файл, так как хеш одинаковый
так же добавлен поиск ключей в несжатом формате

### Смотрите бонус внизу описания!  

Что реализовано:  
#### создание BIP39 Mnemonic для 9 языков. Возможно использовать все сразу или какие-то отдельно 
english, chinese_simplified, chinese_traditional, french, italian, spanish, czech, korean, japanese (список языков редактируйте в файле)  
  
#### Планы:  
[ ] Клиент-сервер  
[ ] ini файлы для настройки клиента и сервера  
[ ] оформить описание ;-)  
  
#### Создан поиск по 11 базам данных (BloomFilter).  
по организации BIP-32 база данных  '32.bf'  
по организации BIP-44 база данных  '44.bf'  
по организации BIP-49 база данных  '49.bf'  
 
  
### по режимам Случайный, Стандартный  

## Установка:  
Зависимости: Python 3.7 и выше  
sudo apt-get install libgmp-dev  
sudo apt-get install libmpfr-dev  
sudo apt-get install libmpc-dev  

sudo pip3 install simplebloomfilter  
sudo pip3 install bitarray==1.9.2  
sudo pip3 install mnemonic  
sudo pip3 install bip-utils==1.6.0  
sudo pip3 install --user gmpy2==2.1.0b5  
sudo pip3 install ecdsa[gmpy2]  
  
  
или  
pip install -r requirements.txt  
или  
python -m pip install -r requirements.txt
  
создайте BloobFilter (BF create\Cbloom.py)
пример:
python Cbloom.py <in file> <outfile>  
  in file - текстовый файл с адресами (один адрес на одну срочку)  
  out file - файл блюм фильтра  
  
## Добавлен режим работы  
#### Стандартный (-m s):  
Mnemonic->check valid->seed  
работает с языками 'english', 'chinese_simplified', 'chinese_traditional', 'french', 'italian', 'spanish','czech','korean','japanese'  
#### Случайный (-m r):  
Генерирует SEED 64 байта без проверок  

  
## Многопоточная версия  
  python mainMT.py -b <BIP 32 или 44> -d <директория с файлами блюм фильтра> -t <количество ядер> -m <режим работы> -c <описание сервера>  
  python mainMT.py -b 32 -d BF -t 2 -m s -c Local_win  
  python mainMT.py -b 44 -d BF -t 3 -m r -c Local_win  
  python mainMT.py -b 49 -d BF -t 2 -m s -c Local_win  
  python mainMT.py -b 84 -d BF -t 2 -m s -c Local_win  
    
## Не забудьте настроить параметры своей почты для отправки найденных мнемоник  
    host:str = 'smtp.mail.ru'  
    port:int = 25  
    password:str = 'adfgvfdvbfdsgbdf'  
    to_addr:str = 'info@mail.ru'  
    from_addr:str = 'info@mail.ru'  
  
  
  
файлы с адресами брать здесь  
https://gz.blockchair.com/  
  
или на моем ресурсе  
https://drive.google.com/drive/folders/1i7OxFbJ2x-xnqd1ANStF_eIKutAxdfoL?usp=sharing  
  [*] Update file BTC (35M address)  
  

    * Version:  Pulsar v3.3.0 multiT  
    * Total kernel of CPU: 6  
    * Used kernel: 2  
    * Mode Search: BIP-32 Стандартный  
    * Dir database Bloom Filter: BF  
    ---------------Load BF---------------  
    Bloom Filter btc.bf Loaded  
    -------------All BF loaded-----------  
    [*] cycle: 1 | total key: 1260 | key/s: 372 in process cpu0 | Found 0  
    [*] cycle: 1 | total key: 1260 | key/s: 376 in process cpu1 | Found 0  
  
------------------------------------------------------------  
    * Version:  Pulsar v3.3.0 multiT  
    * Total kernel of CPU: 6  
    * Used kernel: 2  
    * Mode Search: BIP-44 Энтропия  
    * Dir database Bloom Filter: BF  
    ---------------Load BF---------------  
    Bloom Filter ltc.bf Loaded  
    Bloom Filter dash.bf Loaded  
    Bloom Filter eth.bf Loaded  
    Bloom Filter doge.bf Loaded  
    Bloom Filter cash.bf Loaded  
    Bloom Filter sv.bf Loaded  
    Bloom Filter btc.bf Loaded  
    -------------All BF loaded-----------  
    [*] cycle: 1 | total key: 1260 | key/s: 880 in process cpu0 | Found 0  
    [*] cycle: 2 | total key: 2520 | key/s: 909 in process cpu0 | Found 0  
    [*] cycle: 1 | total key: 1260 | key/s: 922 in process cpu1 | Found 0  
    

exe файл завернут:  
  pyinstaller --runtime-tmpdir .\temp --onefile --clean --name pulsarMT --add-data "mnemonic;mnemonic" --add-data "rezult.txt;." mainMT.py  

### БОНУС!  
  на облачных серверах ORACLE можно арендовать БЕСПЛАТНО 2 сервера навсегда. Скорось там не большая но для тестов хватит.

### Благодарность за мою работу:  
Bitcoin: bc1qnnamfvhrms5sldh83tsesmud8erqm95qttuvw5  
Ethereum: 0xAda9515891532dbA75145c27569e7D5704DBe87f  
