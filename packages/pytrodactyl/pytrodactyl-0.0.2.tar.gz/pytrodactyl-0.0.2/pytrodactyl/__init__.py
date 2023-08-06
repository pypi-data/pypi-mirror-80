import requests
import json
import sys


class Application:
	def __init__(self, url, api_key):
		self.url = url
		self.api_key = api_key
		self.headers = {
		  'Accept': 'Application/vnd.pterodactyl.v1+json',
		  'Content-Type': 'application/json',
		  'Authorization': f'Bearer {self.api_key}'
		}
		#response = requests.get(url=self.url + "/api/application/servers", headers=self.headers)
		#if response.status_code != 200:
		#	print(response.json())
		#	sys.exit()

	def _api_request(self, url):
		response = requests.get(url=url, headers=self.headers)
		return response.json()

	def _meta_data(self):
		meta_data = self._api_request(url=f"{self.url}/api/application/servers")
		x = meta_data['meta']['pagination']['total_pages']
		return int(x)

	def show_all_servers(self):
		b = []
		for i in range(self._meta_data()):
			b.append(self._api_request(url=f"{self.url}/api/application/servers?page={i}"))
		return b
	
	def show_servers(self):
		servers = self._api_request(url=f"{self.url}/api/application/servers")
		return servers

	def get_server(self, id):
		servers = self.show_all_servers()
		for i in range(self._meta_data()):
			for x in servers[i]['data']:
				if str(id) in str(x['attributes']['identifier']):
					return x

	#def server_util(self, id):
	#	servers = self._api_request(url=f"{self.url}/client/servers/{id}/utilization")
	#	print(servers)

	def get_user(self, username):
		users = self._api_request(url=f"{self.url}/api/application/users?filter%5Busername%5D={username}")
		return users
