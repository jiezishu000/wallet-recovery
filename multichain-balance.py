#!/usr/bin/env python3
"""
Multi-Chain Wallet Balance Checker v1.0
========================================
Check your crypto wallet balance across 8+ blockchains with one command.
Supports: Ethereum, BSC, Polygon, Arbitrum, Base, Optimism, Avalanche, Solana

Usage:
  python3 multichain-balance.py 0xYourWalletAddress
  python3 multichain-balance.py BvXqSW5Fwc6LMTyJopbRkQPLYDQFV9hEfR5sMthq73m8

If this tool saved you time or money, consider supporting development:
  TRC20 (USDT): TEwbbfoUtQTTfQFFD6fbLcnSD7tdrdpRx6
  EVM (USDT):   0xa66c92bcb095533ed878fc30a4cbd24dc8edde93
  Solana:       BvXqSW5Fwc6LMTyJopbRkQPLYDQFV9hEfR5sMthq73m8
"""

import requests, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

def query_rpc(url, payload, timeout=10):
    try:
        r = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=timeout)
        if r.status_code == 200:
            j = r.json()
            if 'result' in j:
                return j['result']
    except:
        pass
    return None

def get_erc20_balance(wallet, rpc, token_addr, decimals):
    data = '0x70a08231' + wallet[2:].zfill(64).lower()
    result = query_rpc(rpc, {'jsonrpc':'2.0','method':'eth_call','params':[{'to': token_addr, 'data': data},'latest'],'id':1})
    if result and result != '0x':
        return int(result, 16) / (10 ** decimals)
    return 0

def get_sol_balance(wallet):
    result = query_rpc('https://solana-rpc.publicnode.com',
                       {'jsonrpc':'2.0','method':'getBalance','params':[wallet],'id':1})
    if result:
        return result.get('value', 0) / 1e9
    return 0

# Chain configs: (name, rpc_url, native_symbol, usdt_config, usdc_config)
# Each token config is: (address, decimals)
CHAINS = [
    ('Ethereum',  'https://ethereum-rpc.publicnode.com', 'ETH',
     ('0xdAC17F958D2ee523a2206206994597C13D831ec7', 6),
     ('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 6)),
    ('BSC',       'https://bsc-rpc.publicnode.com', 'BNB',
     ('0x55d398326f99059fF775485246999027B3197955', 18),
     ('0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d', 18)),
    ('Polygon',   'https://polygon-mainnet.g.alchemy.com/v2/demo', 'MATIC',
     ('0xc2132D05D31c914a87C6611C10748AEb04B58e8F', 6),
     ('0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', 6)),
    ('Arbitrum',  'https://arbitrum-rpc.publicnode.com', 'ETH',
     ('0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', 6),
     ('0xaf88d065e77c8cC2239327C5EDb3A432268e5831', 6)),
    ('Base',      'https://base-rpc.publicnode.com', 'ETH',
     None,
     ('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', 6)),
    ('Optimism',  'https://optimism-rpc.publicnode.com', 'ETH',
     ('0x94b008aA00579c1307B0EF2c499aD98a8ce58e58', 6),
     ('0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85', 6)),
    ('Avalanche', 'https://avalanche-c-chain-rpc.publicnode.com', 'AVAX',
     ('0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7', 6),
     ('0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E', 6)),
]

def check_chain(name, rpc, native_symbol, usdt_cfg, usdc_cfg, wallet):
    result = []
    # Native balance
    bal = query_rpc(rpc, {'jsonrpc':'2.0','method':'eth_getBalance','params':[wallet,'latest'],'id':1})
    if bal:
        native_val = int(bal, 16) / 1e18
        if native_val > 0:
            result.append('  %-12s: %.6f %s' % (name, native_val, native_symbol))
    # USDT
    if usdt_cfg:
        usdt = get_erc20_balance(wallet, rpc, usdt_cfg[0], usdt_cfg[1])
        if usdt > 0:
            result.append('  %-12s: %.2f USDT' % (name, usdt))
    # USDC
    if usdc_cfg:
        usdc = get_erc20_balance(wallet, rpc, usdc_cfg[0], usdc_cfg[1])
        if usdc > 0:
            result.append('  %-12s: %.2f USDC' % (name, usdc))
    return result

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 multichain-balance.py <wallet_address>')
        print('  EVM:  0x...')
        print('  Solana: <base58 address>')
        sys.exit(1)

    wallet = sys.argv[1].strip()
    print('=' * 56)
    print('  Multi-Chain Balance Checker v1.0')
    print('  Wallet: %s' % wallet)
    print('=' * 56)

    is_solana = not wallet.startswith('0x')

    if is_solana:
        sol = get_sol_balance(wallet)
        print()
        print('  Solana')
        if sol > 0:
            print('    Balance: %.6f SOL' % sol)
            print('    (~$%.2f at ~$140/SOL)' % (sol * 140))
        else:
            print('    0 SOL')
    else:
        print()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(check_chain, name, rpc, sym, usdt, usdc, wallet): name
                       for name, rpc, sym, usdt, usdc in CHAINS}
            for f in as_completed(futures):
                for line in f.result():
                    print(line)

    print()
    print('-' * 56)
    print('  If this tool saved you time or money, consider donating:')
    print('  TRC20 (USDT): TEwbbfoUtQTTfQFFD6fbLcnSD7tdrdpRx6')
    print('  EVM (USDT):   0xa66c92bcb095533ed878fc30a4cbd24dc8edde93')
    print('=' * 56)

if __name__ == '__main__':
    main()
