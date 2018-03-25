import requests
from multiprocessing import Pool
import argparse
import os.path
import base58
import sys

class Fork():
	def __init__(self, filename, threads):
		if not os.path.isfile(filename):
			exit('File not found')
		f = open(filename, 'r')	
		if not threads:
			threads = 10
		self.banner()
		with Pool(int(threads)) as p:           
			p.map(self.make_all, f)

	def banner(self):
		print('                     ,.=ctE55ttt553tzs.,')
		print('                 ,,c5;z==!!::::  .::7:==it3>.,')
		print('              ,xC;z!::::::    ::::::::::::!=c33x,')
		print('            ,czz!:::::  ::;;..===:..:::   ::::!ct3.')
		print('          ,C;/.:: :  ;=c!:::::::::::::::..      !tt3.')
		print('         /z/.:   :;z!:::::J  :E3.  E:::::::..     !ct3.')
		print('       ,E;F   ::;t::::::::J  :E3.  E::.     ::.       tL')
		print('      ;E7.    :c::::F******   **.  *==c;..    ::     Jttk')
		print('     .EJ.    ;::::::L                   "\:.   ::.    Jttl')
		print('     [:.    :::::::::773.    JE773zs.     I:. ::::.    It3L')
		print('    ;:[     L:::::::::::L    |t::!::J     |::::::::    :Et3')
		print('    [:L    !::::::::::::L    |t::;z2F    .Et:::.:::.  ::[13')
		print('    E:.    !::::::::::::L               =Et::::::::!  ::|13')
		print('    E:.    (::::::::::::L    .......       \:::::::!  ::|i3')
		print('    [:L    !::::      ::L    |3t::::!3.     ]::::::.  ::[13')
		print('    !:(     .:::::    ::L    |t::::::3L     |:::::; ::::EE3')
		print('     E3.    :::::::::;z5.    Jz;;;z=F.     :E:::::.::::II3[')
		print('     Jt1.    :::::::[                    ;z5::::;.::::;3t3')
		print('      \z1.::::::::::l......   ..   ;.=ct5::::::/.::::;Et3L')
		print('       \t3.:::::::::::::::J  :E3.  Et::::::::;!:::::;5E3L')
		print('        "cz\.:::::::::::::J   E3.  E:::::::z!     ;Zz37`')
		print('          \z3.       ::;:::::::::::::::;=\'      ./355F')
		print('            \z3x.         ::~=======\'         ,c253F')
		print('              "tz3=.   BITCOIN FORK CHECKER  .c5t32^')
		print('                 "=zz3==...         ...=t3z13P^')
		print('                     `*=zjzczIIII3zzztE3>*^`')
		print('                                             ')
		print('                      by github.com/foozzi')

	def make_all(self, address):
		address = address.strip()
		bch = self.bch_balance(address)
		btg = self.btg_balance(address)
		# btx = self.btx_balance(address)
		superbtc = self.superbtc_balance(address)
		b2x = self.b2x_balance(address)
		# lbtc = self.lbtc_balance(address)
		bcx = self.bcx_balance(address)
		print('| %s | %s | %s | %s | %s | %s |\n' % (address, bch, btg, superbtc, b2x, bcx))

	# bitcoin cash
	def bch_balance(self, address):
		r = requests.get('https://bitcoincash.blockexplorer.com/api/addr/%s/?noTxList=1' % address)
		balance = r.json()['balance']
		return 'BCH:%s' % str(balance)

	# bitcore (error: Max retries exceeded with url) soon...
	# def btx_balance(self, address):
	# 	r = requests.get('https://insight.bitcore.cc/api/addr/%s/?noTxList=1' % address)
	# 	return 'BTX:%s' % str(r.json()['balance'])

	# superbtc
	def superbtc_balance(self, address):
		r = requests.get('http://block.superbtc.org/insight-api/addr/%s/?noTxList=1' % address)
		return 'SUPERBTC:%s' % r.json()['balance']

	# segwit2x
	def b2x_balance(self, address):
		r = requests.get('https://explorer.b2x-segwit.io/b2x-insight-api/addr/%s/?noTxList=1' % address)
		return 'B2X:%s' % r.json()['balance']

	# lbtc.io (http://explorer.lbtc.io/ is not work now)
	# def lbtc_balance(self, address):
	# 	r = requests.get('http://api.lbtc.io/search3?param=%s' % address)
	# 	balance = int(r.json()['result']) / 100000000
	# 	return 'LBTC:%s' % str(balance)

	# bitcoin gold	
	def btg_balance(self, address):
		decoded = base58.b58decode_check(address)
		if decoded[0] == 0:
			decoded = bytearray(decoded)
			decoded[0] = 38
			address_btg = base58.b58encode_check(bytes(decoded))
			r = requests.get('https://btgexplorer.com/api/addr/%s/?noTxList=1' % address_btg)
			return 'BTG:%s' % str(r.json()['balance'])
		else:
			return 'BTG:None'

	# bitcoinX 
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
