### Hunt to Mnemonic Lite
    Программа для поиска кладов через генерацию мнемоник.
    Вы можете вносить любые изменения и распространять как угодно данный программный продукт.
    Все вопросы прошу задавать только в разделе «ВОПРОСЫ» на GitHUB, в телеграмм объяснять не буду.
    Если у Вас есть идеи по улучшению прошу озвучивать их так же в вопросах. Или по договоренности в телеграмм.
    
    Поддержка пользователей в телеграмм будет производится только по подписке на версию Hunt to Mnemonic Full
    Hunt to Mnemonic Full будет распростятся как приватное приложение на GitHub, для получения доступа обращайтесь в телеграмм.

#### Ресурсы для проверки работы:
    для проверки пользуюсь ресурсами:
    https://iancoleman.io/bip39/  
    https://kriptokurs.ru/bitcointools/tool/hash-to-address    
    https://bitcointools.site/tool/address-to-hash

#### Как это работает:
    https://learnmeabitcoin.com/technical/derivation-paths

#### Что реализовано в версии LITE:  
    Создание Mnemonic на одном языке (English).
    Генерация стандартными средствами библиотеки Mnemonic
    Генерация 128 бит (12 слов)
    Поиск происходит только по BTC
    3 варианта поиска (BIP32, ETH, BTC)
        - Режим 32 ищет только (BIP32)
        - Режим BTC ищет только (BIP44)
        - Режим ETH создан для поиска кошельков ethereum

#### Установка:
    pip install bitarray
    pip install colorama
    pip install bip32

#### Создайте BloobFilter (BF-create\bloom-create.py)
    python bloom-create.py <in file> <out file>  
        in file - текстовый файл с адресами (один адрес на одну срочку)  
        out file - файл блюм фильтра  
  
#### Ключи использования
    python -B PulsarLite.py -b BTC -dbbtc BF\btc.bf -th 3 -sl 5
  
    -b Режим поиска (BIP32, ETH, BTC)  (-b BTC)
    -dbbtc расположение файла ФлюмФильтра для BTC (-dbbtc BF/work.bf)
    -dbeth расположение файла ФлюмФильтра для ETH (-dbeth BF/eth.bf)
    -th количество процессов запущенных для поиска (-th 2)
    -sl задержка по пуску блюм фильтра (у кого много ядер, рекомендую!) (-sl 5)

файлы с адресами брать здесь  
https://gz.blockchair.com/  
  
### Вы должны помнить!!!
![LONG](https://github.com/Noname400/Hunt-to-Mnemonic/blob/main/image/longlonglongtime.jpg)

### Отказ от ответственности.
Программное обеспечение предоставлено только в целях ознакомления. За все последствия использования ПО пользователи несут личную ответственность.
Автор не несет ответственности для использования его продуктов в каких-либо корыстных целях.