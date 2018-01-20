import requests

class Fork():
	def __init__(self, address):
		btc = self.btc_balance(address)
		bch = self.bch_balance(address)
		btx = self.btx_balance(address)
		superbtc = self.superbtc_balance(address)
		print('| %s | %s | %s | %s | %s |\n' % (address, btc, bch, btx, superbtc))


	def btc_balance(self, address):
		while True:
			r = requests.get('https://blockchain.info/q/addressbalance/%s' % address)
			if r.text != 'Maximum concurrent requests for this endpoint reached. Please try again shortly.':
				return 'BTC:%s' % r.text

	def bch_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/api.blockchair.com/bitcoin-cash/dashboards/address/%s' % address)
		return 'BCH:%s' % r.json()['data'][0]['sum_value_unspent']

	def btx_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/chainz.cryptoid.info/btx/api.dws?q=getbalance&a=%s' % address)
		return 'BTX:%s' % r.text

	def superbtc_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/http://block.superbtc.org/insight-api/addr/%s/?noTxList=1' % address)
		return 'SUPERBTC:%s' % r.json()['balance']

		


# example
f = open('addresses.txt', 'r')
for line in f:
	s = Fork(line)
		

