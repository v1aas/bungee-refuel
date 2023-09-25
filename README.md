# BUNGEE-REFUEL

<details>
    <summary>
        <b>RU</b>
    </summary>
Рефуел из polygon/avax/bsc/optimism/arbitrum в сети bsc/avax/polygon/arbitrum/optimism/zksync/polygon zkevm/base посредством моста https://bungee.exchange. Скрипт имеет рандомизацию в отправке транзакций (по умолчанию от 10 до 30 секунд) и количество токенов (+1-10% от отправляемого количества). По всем вопросам - https://t.me/v1aas

## Настройка
1. Скачать python последней версии
2. В private_keys.txt загрузить приватники, 1 строка - 1 ключ
3. Перейти через командную строку в папку с проектом, установить зависимости, в в командной строке написать строку:
    
    **pip install -r requirements.txt**
4. В **config.py** установить минимальную и максимальную задержку между транзакциями, там же можно поменять rpc для блокчейнов
5. В main.py закоммотить/раскоммитить сети, в которые будет рефуел 
6. Запустить main.py
7. Для рефуела есть дефолтные минимальные значения:
   
        MATIC: 1 $MATIC
        AVAX: 0.0065 $AVAX
        BSC: 0.004 $BNB 
        ARBITRUM: 0.0025 $ETH
        OPTIMISM: 0.0027 $ETH
   После выбора сети будет предложено, отправить с такими значеиями или ввести свое. ***В разных сетях - разная минимальное количество***. В bsc, matic, avax по умолчанию указаны минимальные значения не для дорогих сетей, для arb и opt - самые дорогие!

## Возможные ошибки
1. ValueError: {'code': -32000, 'message': 'noonce to low'}

Нужно поменять rpc для блокчейна, с которого отправляется транзакции

2. ValueError: {'code': -32000, 'message': 'intrinsic gas too low'}

Не хватает газ лимита, зависит по большей части от состоянии сети, можно повысить в самом коде, на строчке 72 (arbitrum) и 74 (другие сети)

3. Минимальное количество токенов для рефула не проходит

Минимальные значения в мосте плавающуие, поэтому возможно по дефолтным значениям может не пройти. При такой проблеме посмотреть в мосте минимальное количество токенов для отправки в самую дорогую сеть.


</details>

<details>
    <summary>
        <b>EN</b>
    </summary>
    Refuel from polygon/avax/bsc/optimism/arbitrum to bsc/avax/polygon/arbitrum/optimism/zksync/polygon zkevm/base network via https://bungee.exchange bridge. The script has randomization in sending transactions (10 to 30 seconds by default) and number of tokens (+1-10% of the number of tokens sent). For any questions - https://t.me/v1aas

## Setup
1. Download python latest version
2. In private_keys.txt load private keys, 1 line - 1 key
3. Go through the command line to the project folder, install dependencies, in the command line write the line:
    
    **pip install -r requirements.txt**
4. In **config.py** set the minimum and maximum delay between transactions, there you can also change the rpc for blockchains.
5. In main.py commit/uncommit the networks to be refueled
6. Run main.py
7. There are default minimum values for refuel:
   
        MATIC: 1 $MATIC
        AVAX: 0.0065 $AVAX
        BSC: 0.004 $BNB 
        ARBITRUM: 0.0025 $ETH
        OPTIMISM: 0.0027 $ETH
   After selecting a network, you will be prompted whether to send with these values or enter your own. ***The minimum number varies from network to network***. In bsc, matic, avax default minimum values are not for expensive networks, for arb and opt - the most expensive!

## Possible errors
1. ValueError: {'code': -32000, 'message': 'noonce to low'}

Need to change the rpc for the blockchain from which the transaction is sent

2. ValueError: {'code': -32000, 'message': 'intrinsic gas too low'}

Not enough gas limit, depends mostly on the state of the network, can be increased in the code itself, on line 72 (arbitrum) and 74 (other networks).

3. Minimum number of tokens for refuel does not pass

Minimum values in the bridge are floating, so it is possible that default values may not pass. If this problem occurs, check the minimum number of tokens in the bridge to send to the most expensive network.
</details>
