from web3 import Web3
from custom_logger import logger
from config import RPC_LIST, CONTRACT_LIST, MAX_TIME, MIN_TIME
import json
import random
import time

CHAIN_ID = {
    #'bsc': 56,
    #'avax': 43114,
    #'polygon': 137,
    'arbitrum': 42161,
    #'optimism': 10,
    'zksync': 324,
    #'polygon_zkevm': 1101,
    #'base': 8453
    }

def get_bungee_abi():
    with open('bungee_abi.txt', 'r') as file:
        return json.loads(file.readline().strip())
    

def get_private_keys():
    with open('private_keys.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def refuel(network, private_keys, amount):
    if network == 'polygon':
        rpc = RPC_LIST['polygon']
        contract_address = CONTRACT_LIST['contract_polygon']
        target_chain_id = 137
    elif network == 'avax':
        rpc = RPC_LIST['avax']
        contract_address = CONTRACT_LIST['contract_avax']
        target_chain_id = 43114
    elif network == 'bsc':
        rpc = RPC_LIST['bsc']
        contract_address = CONTRACT_LIST['contract_bsc']
        target_chain_id = 56
    elif network == 'arbitrum':
        rpc = RPC_LIST['arbitrum']
        contract_address = CONTRACT_LIST['contract_arbitrum']
        target_chain_id = 42161
    elif network == 'optimism':
        rpc = RPC_LIST['optimism']
        contract_address = CONTRACT_LIST['contract_optimism']
        target_chain_id = 10
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
            sleep = random.randint(MIN_TIME, MAX_TIME)
            logger.info(f'Сплю {sleep} секунд перед следующей транзакцией')
            time.sleep(sleep)

def create_transaction(contract, wallet, chain_id, target_chain_id ,web3, amount):
    amount *= (1 + random.uniform(0, 0.1))
    if target_chain_id == 42161:
        gas = 730223
    else:
        gas = 30000
    return contract.functions.depositNativeToken(chain_id, wallet).build_transaction({
        'gas': gas,
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
        network = input("Из какой сети будет рефуел?" + 
                        "\n 1 - polygon \n 2 - avax \n 3 - bsc \n 4 - arbitrum \n 5 - optimism \n" + 
                        "Введи число: ")
        if network == '0':
            break
        elif network == '1':
            network = 'polygon'
            default_amount = 1
        elif network == '2':
            network = 'avax'
            default_amount = 0.0065
        elif network == '3':
            network = 'bsc'
            default_amount = 0.004
        elif network == '4':
            network = 'arbitrum'
            default_amount = 0.0025
        elif network == '5':
            network = 'optimism'
            default_amount = 0.0027
        else:
            print("Неправильный ввод. Доступны команды: 0, 1, 2, 3, 4, 5")
            continue

        amount = input("\n" + "Сколько нативного токена рефулить? По умолчанию отправляется: \n" +  
                        "MATIC: 1 $MATIC\n" +
                        "AVAX: 0.0065 $AVAX\n" +
                        "BSC: 0.004 $BNB \n" +
                        "ARBITRUM: 0.0025 $ETH \n" +
                        "OPTIMISM: 0.0027 $ETH \n" + 
                        "Оставь строку пустой или введи своё количество: ")
        amount = float(amount) if amount else default_amount

        refuel(network, private_keys, amount)
        logger.success("Скрипт завершил работу")
        break

if __name__ == "__main__":
    main()
    