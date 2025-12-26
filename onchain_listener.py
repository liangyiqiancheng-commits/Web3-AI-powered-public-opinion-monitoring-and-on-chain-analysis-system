from web3 import Web3
import json
import time

# 连接到以太坊主网 (这里用的是公开节点)
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_API_KEY"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

class WhaleWatcher:
    def __init__(self, min_value_eth=100):
        self.min_value = min_value_eth
        self.target_contracts = [
            "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", # Uniswap V2
            "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT
        ]
    
    def monitor_blocks(self):
        """
        实时监听新区块，过滤大额交易
        """
        if not w3.is_connected():
            print("Connection lost. Retrying...")
            return

        latest_block = w3.eth.block_number
        print(f"Scanning block: {latest_block}")
        
        # 模拟获取交易数据
        # TODO: Optimize with async/await for high-frequency trading
        block = w3.eth.get_block(latest_block, full_transactions=True)
        
        for tx in block.transactions:
            if self._is_whale_movement(tx):
                self._alert_user(tx)

    def _is_whale_movement(self, tx):
        # 简单的过滤逻辑
        value_eth = w3.from_wei(tx['value'], 'ether')
        return value_eth >= self.min_value

    def _alert_user(self, tx):
        alert = {
            "timestamp": time.time(),
            "from": tx['from'],
            "to": tx['to'],
            "value": str(w3.from_wei(tx['value'], 'ether')) + " ETH",
            "hash": tx['hash'].hex()
        }
        print(f"🚨 WHALE ALERT: {json.dumps(alert, indent=2)}")

if __name__ == "__main__":
    watcher = WhaleWatcher()
    # watcher.monitor_blocks() # Commented out to save API calls
