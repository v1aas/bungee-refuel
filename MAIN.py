from web3 import Web3
from custom_logger import logger
import json
import random
import time

POLYGON_RPC = 'https://polygon.llamarpc.com'
AVAX_RPC = 'https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc'
BUNGEE_CONTRACT_POLYGON = '0xAC313d7491910516E06FBfC2A0b5BB49bb072D91'
BUNGEE_CONTRACT_AVAX = '0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB'
CHAIN_ID = {
    'bsc': 56,
    'avax': 43114,
    'fantom': 250,
    'polygon': 137
    }

def get_bungee_abi():
    with open('bungee_abi.txt', 'r') as file:
        return json.loads(file.readline().strip())

def get_private_keys():
    with open('private_keys.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def refuel(network, private_keys, amount):
    if network == 'polygon':
        rpc = POLYGON_RPC
        contract_address = BUNGEE_CONTRACT_POLYGON
        target_chain_id = 137
    elif network == 'avax':
        rpc = AVAX_RPC
        contract_address = BUNGEE_CONTRACT_AVAX
        target_chain_id = 43114
    else:
        logger.error("Такой сети нет")
        return
    
    web3 = Web3(Web3.HTTPProvider(rpc))
    contract = web3.eth.contract(address=contract_address, abi=get_bungee_abi())
    
    for count, private_key in enumerate(private_keys, start=1):
        wallet = web3.eth.account.from_key(private_key).address
        logger.success(f'{count}/{len(private_keys)} Найден кошелек: {wallet}')
        for chain, chain_id in CHAIN_ID.items():
            if chain == network:
                continue
            logger.info(f'Начинаю рефуел из {network} в {chain}')
            transaction = create_transaction(contract, wallet, chain_id, target_chain_id, web3, amount)
            send_transaction(transaction, private_key, web3)
            sleep = random.randint(10,30)
            logger.info(f'Сплю {sleep} секунд перед следующей транзакцией')
            time.sleep(sleep)

def create_transaction(contract, wallet, chain_id, target_chain_id ,web3, amount):
    amount *= (1 + random.uniform(0, 0.1))
    return contract.functions.depositNativeToken(chain_id, wallet).build_transaction({
        'gas': 68694,
        'gasPrice': web3.eth.gas_price,
        'value': Web3.to_wei(amount, 'ether'),
        'nonce': web3.eth.get_transaction_count(wallet),
        'chainId': target_chain_id})

def send_transaction(transaction, private_key, web3):
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    logger.info(f'Транзакция отправлена. Хеш: {transaction_hash.hex()}')
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    
    if receipt.status == 1:
        logger.success("Транзакция успешно выполнена")
    else:
        logger.error("Транзакция не удалась")

def main():
    private_keys = get_private_keys()

    while True:
        print("Для выхода введи 0")
        network = input("Из какой сети будет рефуел? \n 1 - polygon \n 2 - avax \n")
        if network == '0':
            break
        elif network == '1':
            network = 'polygon'
            default_amount = 1
        elif network == '2':
            network = 'avax'
            default_amount = 0.0065
        else:
            print("Неправильный ввод. Доступны команды: 0, 1, 2")
            continue

        amount = input("Сколько нативного токена рефулить? \n По умолчанию для матика отправляется 1 $MATIC\n"
                       + "Для авакса 0.0065 $AVAX \n" + 
                       "Оставь строку пустой или напиши своё количество: ")
        amount = float(amount) if amount else default_amount

        refuel(network, private_keys, amount)
        logger.success("Скрипт завершил работу")
        time.sleep(600)
        break

if __name__ == "__main__":
    main()