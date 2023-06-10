# BUNGEE-REFUEL
Рефуел из polygon/avax/bsc в сети bsc, ~~fantom~~, avax, polygon посредством моста https://bungee.exchange/

UPD:
fantom закоммитил, тк сеть сейчас переживает не лучшие времена, там мало ликвидности. Если он нужен, то его нужно раскомитить в коде.
Также если возникает непредвиденные ошибки, по типу "noonce to low", то поменяйте rpc для блокчейна (обычно этим шалит полигон).

Скрипт имеет рандомизацию в отправке транзакций (до 30 сек) и количество токенов (+1-10% от количества)

По всем вопросам - https://t.me/v1aas

## Настройка
1. Скачать python последней версии
2. В private_keys.txt загрузить приватники, 1 строка - 1 ключ
3. Перейти через командную строку в папку с проектом, установить зависимости, в в командной строке написать строку:
    
    **pip install -r requirements.txt**
4. Запустить main.py

## Как добавить другие сети?
**Изменить следующую функцию**
### refuel(network, private_keys, amount)
Эта функция используется для выполнения "рефуелинга" (пополнения счета) из сети Polygon/Avax в другие сети блокчейна. Она принимает 3 аргумента:
* network - сеть из которой будет рефуел
* private_key - является приватным ключом кошелька пользователя
* amount - указывает количество токенов для отправки. Если amount не указан, по умолчанию отправляется **1 $MATIC**/**0.0065 $AVAX**/**0.004 $BNB**
