import requests
from multiprocessing import Pool
import argparse
import os.path

class Fork():
	def __init__(self, filename, threads):
		if not os.path.isfile(filename):
			exit('File not found')
		f = open(filename, 'r')	
		if not threads:
			threads = 10

		with Pool(int(threads)) as p:           
			p.map(self.make_all, f)

	def make_all(self, address):
		btc = self.btc_balance(fg)
		bch = self.bch_balance(fg)
		btx = self.btx_balance(fg)
		superbtc = self.superbtc_balance(fg)
		b2x = self.b2x_balance(fg)
		lbtc = self.lbtc_balance(fg)
		bcx = self.bcx_balance(fg)
		print('| %s | %s | %s | %s | %s | %s | %s | %s |\n' % (fg, btc, bch, btx, superbtc, b2x, lbtc, bcx))

	def btc_balance(self, address):
		r = requests.get('https://blockchain.info/q/addressbalance/%s' % address)
		balance = int(r.text) / 100000000
		return 'BTC:%s' % str(balance)

	def bch_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/api.blockchair.com/bitcoin-cash/dashboards/address/%s' % address)
		balance = int(r.json()['data'][0]['sum_value_unspent']) / 100000000
		return 'BCH:%s' % str(balance)

	def btx_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/chainz.cryptoid.info/btx/api.dws?q=getbalance&a=%s' % address)
		return 'BTX:%s' % r.text

	def superbtc_balance(self, address):
		r = requests.get('https://galvanize-cors-proxy.herokuapp.com/http://block.superbtc.org/insight-api/addr/%s/?noTxList=1' % address)
		return 'SUPERBTC:%s' % r.json()['balance']

	def b2x_balance(self, address):
		r = requests.get('https://explorer.b2x-segwit.io/b2x-insight-api/addr/%s/?noTxList=1' % address)
		return 'B2X:%s' % r.json()['balance']

	# lbtc.io
	def lbtc_balance(self, address):
		r = requests.get('http://api.lbtc.io/search3?param=%s' % address)
		balance = int(r.json()['result']) / 100000000
		return 'LBTC:%s' % str(balance)

	# https://bcx.info
	def bcx_balance(self, address):
		r = requests.get('https://bcx.info/insight-api/addr/%s/?noTxList=1' % address)
		if r.text != 'Invalid address: Address has mismatched network type.. Code:1':
			return 'BCX:%s' % r.json()['balance']
		else :
			return 'BCX:0'

		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("filepath", help="set file path wtih addresses")
	parser.add_argument("-t", "--threads", help="set number threads (default 10)", required=False)
	args = parser.parse_args()
	Fork(args.filepath, args.threads)
