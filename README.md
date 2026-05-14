# 🔐 BIP39 Wallet Recovery Tool

> Missing a word from your crypto wallet seed phrase? I can help you recover it.

Based on the same technology behind the **[viral ClaudeAI $400K BTC recovery case](https://www.coindesk.com/)** — where an AI helped recover 5 BTC from a forgotten wallet.

## 🚀 Services (1 USDT each)

| Service | Description | Time |
|---------|-------------|------|
| **Missing Word Recovery** | Find 1 unknown word from 12/24-word BIP39 seed (2048 tries) | <30s |
| **Spelling Correction** | Fix typos in your seed phrase | <30s |
| **Passphrase Brute Force** | Try common passphrases against your seed | ~5min |
| **Derivation Path Enumeration** | Try all common BIP32 paths | ~1min |

## 💰 How to Order

1. Send **1 USDT** to any of these addresses:
   - **Polygon (USDT)**: `0xa66c92bcb095533ed878fc30a4cbd24dc8edde93`
   - **TRC20 (USDT)**: `TEwbbfoUtQTTfQFFD6fbLcnSD7tdrdpRx6`
   - **Solana**: `BvXqSW5Fwc6LMTyJopbRkQPLYDQFV9hEfR5sMthq73m8`
2. Open a [GitHub Issue](https://github.com/jiezishu000/wallet-recovery/issues/new) with:
   - The transaction hash
   - Your partial seed phrase (replace missing words with `?`)
   - The wallet address(es) you expect to find
3. I'll run the recovery and reply within **1 hour**

## 🔧 What's Recoverable

- ✅ BIP39 mnemonics (12, 15, 18, 21, 24 words)
- ✅ **1 missing word** — guaranteed find in <2048 tries
- ✅ Typo/fuzzy match — find closest BIP39 word to your mis-typed word
- ✅ Passphrase testing — try 1000+ common passphrases
- ❌ Legacy Blockchain.info wallets (non-BIP39)
- ❌ Lost private keys without mnemonic
- ❌ Hardware wallets you don't physically have

## ⚡ Tool Features

```
python3 wallet-recovery.py --mode missing --words word1 ? word3 ... --address 0x...
python3 wallet-recovery.py --mode fuzzy --typo abandun --address 0x...
python3 wallet-recovery.py --mode password
python3 wallet-recovery.py --mode paths
```

## 📜 License

MIT — Free for personal use. Commercial support available via donation.

---

**Donations welcome at any of the addresses above.**
