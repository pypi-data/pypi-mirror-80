__author__ = 'akashjeez'

import os, sys, json, pandas, requests
import re, math, random, itertools
from datetime import datetime, timedelta


class AzuRestAPI:

	def __init__(self, token: str) -> None:
		self.token = token

	BASE_URL = 'https://management.azure.com'
	AGGREGATION = 'Average,Minimum,Maximum,Total,Count'


	def List_Azure_Subscriptions(self) -> dict:
		try:
			dataset, API_VERSION = [], '2020-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			response = requests.get(f'{self.BASE_URL}/subscriptions?api-version={API_VERSION}', headers = headers).json()
			for data in response['value']:
				dataset.append({
					'subscription_id': data.get('subscriptionId', 'TBD'),
					'subscription_name': data.get('displayName', 'TBD'),
					'tenant_id': data.get('tenantId', 'TBD'),
					'authorization_source': data.get('authorizationSource', 'TBD'),
					'state': data.get('state', 'TBD')
				})
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Resource_Groups(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/resourcegroups?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD')
					}
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Resources(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/resources?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Disks(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Compute/disks?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'pricing_tier': data.get('sku', 'TBD').get('name', 'TBD'),
						'vm_resource_id': data.get('managedBy', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update({
							'os_type': data['properties'].get('osType', 'TBD'),
							'disk_size_gb': data['properties'].get('diskSizeGB', 'TBD'),
							'disk_iops_readwrite': data['properties'].get('diskIOPSReadWrite', 'TBD'),
							'disk_mbps_readwrite': data['properties'].get('diskMBpsReadWrite', 'TBD'),
							'disk_state': data['properties'].get('diskState', 'TBD'),
							'creation_date': datetime.strptime(data['properties'].get('timeCreated')[:10], '%Y-%m-%d').strftime('%d-%b-%Y')
								if data['properties'].get('timeCreated') else 'TBD',
						})
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Snapshots(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Compute/snapshots?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'pricing_tier': data.get('sku', 'TBD').get('name', 'TBD'),
						'incremental': data.get('incremental', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update({
							'os_type': data['properties'].get('osType', 'TBD'),
							'disk_size_gb': data['properties'].get('diskSizeGB', 'TBD'),
							'disk_state': data['properties'].get('diskState', 'TBD'),
							'creation_date': datetime.strptime(data['properties'].get('timeCreated')[:10], '%Y-%m-%d').strftime('%d-%b-%Y')
								if data['properties'].get('timeCreated') else 'TBD',
						})
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Virtual_Machines(self, subscriptions: list) -> dict:
		try:
			EXCLUDE_VMs = ('va81-intranet-nm1', )
			dataset, API_VERSION = [], '2019-07-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Compute/virtualMachines?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					if data.get('name') in EXCLUDE_VMs:	continue
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'vm_status': requests.get(f"{self.BASE_URL}{data.get('id')}/instanceView?api-version=2019-07-01", headers = headers)\
							.json()['statuses'][-1].get('displayStatus', 'TBD'),
					}
					if properties := data['properties']:
						data_dump.update({
							'vm_id': properties.get('vmId', 'TBD'),
							'license_type': properties.get('licenseType', 'TBD'),
							'pricing_tier': properties['hardwareProfile'].get('vmSize', 'TBD') if 'hardwareProfile' in properties.keys() else 'TBD',
							'computer_name': properties['osProfile'].get('computerName', 'TBD') if 'osProfile' in properties.keys() else 'TBD',
							'admin_username': properties['osProfile'].get('adminUsername', 'TBD') if 'osProfile' in properties.keys() else 'TBD',
							'network_interfaces': properties['networkProfile'].get('networkInterfaces', 'TBD') if 'networkProfile' in properties.keys() else 'TBD',
							'boot_diagnostics': properties['diagnosticsProfile'].get('bootDiagnostics', 'TBD') if 'diagnosticsProfile' in properties.keys() else 'TBD',
						})
					if storage_profile := data['properties']['storageProfile']:
						data_dump.update({
							'image_reference': storage_profile.get('imageReference', 'TBD'),
							'data_disks': storage_profile.get('dataDisks', 'TBD'),
							'os_disk_name': storage_profile['osDisk'].get('name', 'TBD') if 'osDisk' in storage_profile.keys() else 'TBD',
							'os_disk_type': storage_profile['osDisk'].get('osType', 'TBD') if 'osDisk' in storage_profile.keys() else 'TBD',
							'os_disk_size_gb': storage_profile['osDisk'].get('diskSizeGB', 'TBD')  if 'osDisk' in storage_profile.keys() else 'TBD',
							'os_disk_create_option': storage_profile['osDisk'].get('createOption', 'TBD') if 'osDisk' in storage_profile.keys() else 'TBD',
							'os_disk_caching': storage_profile['osDisk'].get('caching', 'TBD') if 'osDisk' in storage_profile.keys() else 'TBD',
							'os_disk_resource_id': storage_profile['osDisk'].get('managedDisk').get('id', 'TBD')
								if 'osDisk' in storage_profile.keys() and 'managedDisk' in storage_profile['osDisk'].keys() else 'TBD',
							'os_disk_storage_account_type': storage_profile['osDisk'].get('managedDisk').get('storageAccountType', 'TBD')
								if 'osDisk' in storage_profile.keys() and 'managedDisk' in storage_profile['osDisk'].keys() else 'TBD',
						})
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					print(f" ** {data.get('id')}")
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Advisor_Recommendations(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2017-04-19'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Advisor/recommendations?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'type': data.get('type', 'TBD'),
					}
					if properties := data['properties']:
						data_dump.update({
							'resource_id': properties['resourceMetaData'].get('resourceId', 'TBD')
								if 'resourceMetaData' in properties.keys() else 'TBD',
							'category': properties.get('category', 'TBD'),
							'impact': properties.get('impact', 'TBD'),
							'impacted_field': properties.get('impactedField', 'TBD'),
							'resource_name': properties.get('impactedValue', 'TBD'),
							'problem': properties['shortDescription'].get('problem', 'TBD') 
								if 'shortDescription' in properties.keys() else 'TBD',
							'solution': properties.get('extendedProperties',' TBD'),
						})
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Container_Registries(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.ContainerRegistry/registries?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'pricing_tier': data['sku'].get('tier', 'TBD') if 'sku' in data.keys() else 'TBD',
					}
					if properties := data['properties']:
						data_dump.update({
							'login_server': properties.get('loginServer', 'TBD'),
							'creation_date': datetime.strptime(properties['timeCreated'][:10], '%Y-%m-%d').strftime('%d-%b-%Y')
								if 'timeCreated' in properties.keys() else 'TBD',
							'admin_user_enabled': properties.get('adminUserEnabled', 'TBD'),
						})
						if policies := properties['policies']:
							data_dump.update({
								'quarantine_policy_status': policies['quarantinePolicy'].get('status' ,'TBD')
									if 'quarantinePolicy' in policies.keys() else 'TBD',
								'trust_policy_type': policies['trustPolicy'].get('type', 'TBD')
									if 'trustPolicy' in policies.keys() else 'TBD',
								'retention_policy_days': policies['retentionPolicy'].get('days', 'TBD')
									if 'retentionPolicy' in policies.keys() else 'TBD',
							})
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Recovery_Service_Vaults(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2016-06-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.RecoveryServices/vaults?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Recovery_Service_Vault_Backups(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-05-13'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for vault in self.List_Azure_Recovery_Service_Vaults( subscriptions = subscriptions )['data']:
				request_url = f"{self.BASE_URL}{vault.get('resource_id')}/backupProtectedItems?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': vault.get('resource_id', 'TBD'),
						'subscription_id': vault.get('subscription_id', 'TBD'),
						'subscription_name': vault.get('subscription_name', 'TBD'),
						'resource_group_name': vault.get('resource_group_name', 'TBD'),
						'resource_name': vault.get('resource_name', 'TBD'),
						'vault_type': vault.get('type', 'TBD'),
						'vault_location': vault.get('location', 'TBD'),
						'backup_name': data.get('name', 'TBD'),
						'backup_type': data.get('type', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					print('\n', data_dump)
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_CDN_Profiles(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-12-31'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Cdn/profiles?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'sku': data.get('sku', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Application_Gateways(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/applicationGateways?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Cognitive_Service_Accounts(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2017-04-18'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.CognitiveServices/accounts?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'kind': data.get('kind', 'TBD'),
						'sku': data.get('sku', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_SQL_Virtual_Machines(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2017-03-01-preview'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.SqlVirtualMachine/sqlVirtualMachines?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if properties := data['properties']:
						data_dump.update({
							'vm_resource_id': properties.get('virtualMachineResourceId', 'TBD'),
							'sql_image_offer': properties.get('sqlImageOffer', 'TBD'),
							'sql_server_license_type': properties.get('sqlServerLicenseType', 'TBD'),
							'sql_management': properties.get('sqlManagement', 'TBD'),
							'sql_image_sku': properties.get('sqlImageSku', 'TBD')
						})
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_SQL_Databases(self, subscriptions: list) -> dict:
		try:
			EXCLUDE_DBs = ('master', 'Tech.Stone_Tech.Stone....Co.', )
			dataset, API_VERSION = [], '2019-06-01-preview'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Sql/servers?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for server in response['value']:
					response_2 = requests.get(f"{self.BASE_URL}{server.get('id')}/databases?api-version=2017-10-01-preview", headers = headers).json()
					for data in response_2['value']:
						if data.get('name') in EXCLUDE_DBs:	continue
						data_dump = {
							'db_server_resource_id': server.get('id', 'TBD'),
							'db_resource_id': data.get('id', 'TBD'),
							'subscription_id': subscription_id,
							'subscription_name': subscription['subscription_name'],
							'resource_group_name': server.get('id').split('/')[4],
							'db_server_name': server.get('name', 'TBD'),
							'db_name': data.get('name', 'TBD'),
							'db_type': data.get('type','TBD'),
							'db_location': data.get('location', 'TBD'),
							'db_sku': data.get('sku', 'TBD'),
						}
						if properties := server['properties']:
							data_dump.update({
								'admin_login': properties.get('administratorLogin', 'TBD'),
								'db_server_fqhn': properties.get('fullyQualifiedDomainName', 'TBD'),
							})
						if 'properties' in data.keys():
							data_dump.update( data.get('properties') )
						if 'tags' in data.keys():
							data_dump.update( data.get('tags') )
						dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_SQL_Elastic_Pools(self, subscriptions: list) -> dict:
		try:
			EXCLUDE_DBS = ('master', )
			dataset, API_VERSION = [], '2019-06-01-preview'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Sql/servers?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for server in response['value']:
					response_2 = requests.get(f"{self.BASE_URL}{server.get('id')}/elasticPools?api-version=2017-10-01-preview", headers = headers).json()
					for data in response_2['value']:
						if data.get('name') in EXCLUDE_DBS:	continue
						data_dump = {
							'db_server_resource_id': server.get('id', 'TBD'),
							'subscription_id': subscription_id,
							'subscription_name': subscription['subscription_name'],
							'resource_group_name': server.get('id').split('/')[4],
							'db_server_name': server.get('name', 'TBD'),
							'ep_reource_id': data.get('id', 'TBD'),
							'ep_name': data.get('name', 'TBD'),
							'ep_type': data.get('type','TBD'),
							'ep_location': data.get('location', 'TBD'),
							'ep_sku': data.get('sku', 'TBD'),
						}
						if 'properties' in data.keys():
							data_dump.update( data.get('properties') )
						if 'tags' in data.keys():
							data_dump.update( data.get('tags') )
						dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_SQL_Managed_Instances(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2018-06-01-preview'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Sql/managedInstances?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'db_server_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'database_server_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'sku': data.get('sku', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Load_Balancers(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/loadBalancers?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'sku': data.get('sku', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Log_Analytics_Workspaces(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-08-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.OperationalInsights/workspaces?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Storage_Accounts(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-06-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Storage/storageAccounts?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'kind': data.get('kind', 'TBD'),
						'pricing_tier': data['sku'].get('name', 'TBD') if 'sku' in data.keys() else 'TBD',
					}
					if properties := data['properties']:
						data_dump.update({
							'primary_endpoint_conns': properties.get('privateEndpointConnections', 'TBD'),
							'network_acls': properties.get('networkAcls', 'TBD'),
							'support_https_traffic_only': properties.get('supportsHttpsTrafficOnly', 'TBD'),
							'encryption': properties.get('encryption', 'TBD'),
							'access_tier': properties.get('accessTier', 'TBD'),
							'creation_date': datetime.strptime(properties['creationTime'][:10], '%Y-%m-%d').strftime('%d-%b-%Y')
								if 'timeCreated' in properties.keys() else 'TBD',
							'primary_endpoints': properties.get('primaryEndpoints', 'TBD'),
							'primary_location': properties.get('primaryLocation', 'TBD'),
							'primary_status': properties.get('statusOfPrimary', 'TBD'),
							'secondary_endpoints': properties.get('secondaryEndpoints', 'TBD'),
							'secondary_location': properties.get('secondaryLocation', 'TBD'),
							'secondary_status': properties.get('statusOfSecondary', 'TBD'),
						})
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_App_Services(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-08-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Web/sites?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'kind': data.get('kind', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Public_IP_Addresses(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/publicIPAddresses?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'sku': data['sku'].get('name', 'TBD') if 'sku' in data.keys() else 'TBD',
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Application_Insights(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2015-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f"{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Insights/components?api-version={API_VERSION}"
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'db_server_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'database_server_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'kind': data.get('kind', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Virtual_Networks(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/virtualNetworks?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Network_Security_Groups(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2020-05-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/networkSecurityGroups?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Security_Center_Alerts(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-01-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Security/alerts?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_App_Service_Plans(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2019-08-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Web/serverfarms?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
						'kind': data.get('kind', 'TBD'),
						'sku': data.get('sku', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					if 'tags' in data.keys():
						data_dump.update( data.get('tags') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Classic_Storage_Accounts(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2015-06-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.ClassicStorage/storageAccounts?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Classic_Virtual_Machines(self, subscriptions: list) -> dict:
		try:
			dataset, API_VERSION = [], '2015-06-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			for subscription in subscriptions:
				subscription_id = subscription['subscription_id']
				request_url = f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.ClassicCompute/virtualMachines?api-version={API_VERSION}'
				response = requests.get( request_url , headers = headers ).json()
				for data in response['value']:
					data_dump = {
						'resource_id': data.get('id', 'TBD'),
						'subscription_id': subscription_id,
						'subscription_name': subscription['subscription_name'],
						'resource_group_name': data.get('id').split('/')[4],
						'resource_name': data.get('name', 'TBD'),
						'type': data.get('type', 'TBD'),
						'location': data.get('location', 'TBD'),
					}
					if 'properties' in data.keys():
						data_dump.update( data.get('properties') )
					dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Activity_Logs(self, subscription_id: str, filter_query: str) -> dict:
		try:
			dataset, API_VERSION = [], '2015-04-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			request_url = (
				f'{self.BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.insights/eventtypes/' + 
				f'management/values?api-version={API_VERSION}&$filter={filter_query}'
			)
			response = requests.get(request_url , headers = headers).json()
			for data in response['value']:
				data_dump = {
					'subscription_id': subscription_id,
					'tenant_id': data.get('tenantId', 'TBD'),
					'event_timestamp': data.get('eventTimestamp', 'TBD'),
					'resource_id': data.get('resourceId', 'TBD'),
					'operation_id': data.get('operationId', 'TBD'),
					'resource_group_name': data.get('resourceGroupName', 'TBD'),
					'level': data.get('level', 'TBD'),
					'caller_email': data.get('caller', 'TBD'),
					'event_name': data['event'].get('value',' TBD') if 'event' in data.keys() else 'TBD',
					'auth_action': data['authorization'].get('action', 'TBD') if 'authorization' in data.keys() else 'TBD',
					'category_name': data['category'].get('value',' TBD') if 'category' in data.keys() else 'TBD',
					'operation_name': data['operationName'].get('value',' TBD') if 'operationName' in data.keys() else 'TBD',
					'resource_type': data['resourceType'].get('value', 'TBD') if 'resourceType' in data.keys() else 'TBD',
					'status': data['status'].get('value', 'TBD') if 'status' in data.keys() else 'TBD',
					'sub_status': data['subStatus'].get('value', 'TBD') if 'subStatus' in data.keys() else 'TBD',
					#'claims': data.get('claims', 'TBD'),
				}
				if 'httpRequest' in data.keys():
					data_dump.update({
						'client_requests_id': data['httpRequest'].get('clientRequestId', 'TBD'),
						'client_ip_address': data['httpRequest'].get('clientIpAddress', 'TBD'),
						'http_request_method': data['httpRequest'].get('method', 'TBD'),
					})
				dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def List_Azure_Resource_Type_Metrics(self, resource_id: str) -> dict:
		try:
			dataset, API_VERSION = [], '2018-01-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			request_url = f"{self.BASE_URL}{resource_id}/providers/Microsoft.insights/metricDefinitions?api-version={API_VERSION}"
			response = requests.get( request_url , headers = headers ).json()
			for data in response['value']:
				data_dump = {
					'resource_id': resource_id,
					'name': data.get('name', 'TBD'),
					'unit': data.get('unit',' TBD'),
					'description': data.get('displayDescription', 'TBD'),
					'primary_aggreation_types': data.get('primaryAggregationType', 'TBD'),
					'supported_aggregation_types': data.get('supportedAggregationTypes', 'TBD'),
					'metric_availabilities': data.get('metricAvailabilities', 'TBD')
				}
				print('\n', data_dump)
				dataset.append( data_dump )
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


	def Get_Azure_Resource_Metrics(self, resource_id: str, metric_name: str, timespan: str, interval: str) -> dict:
		try:
			dataset, API_VERSION = [], '2018-01-01'
			headers = {'Authorization' : f'Bearer { self.token }'}
			request_url = ( 
				f'{self.BASE_URL}{resource_id}/providers/microsoft.insights/metrics?api-version={API_VERSION}&metricnames={metric_name}' +
				f'&timespan={timespan}&interval={interval}&aggregation={self.AGGREGATION}' )
			response = requests.get( request_url , headers = headers ).json()
			for temp_1 in response['value']:
				for temp_2 in temp_1['timeseries']:
					for temp_3 in temp_2['data']:
						dataset.append({
							'resource_id': resource_id,
							'subscription_id': resource_id.split('/')[2],
							'resource_group_name': resource_id.split('/')[4],
							'resource_name': resource_id.split('/')[-1],
							'time_stamp': datetime.strptime(temp_3.get('timeStamp'), '%Y-%m-%dT%H:%M:%S%z')\
								.strftime('%d-%m-%Y %I:%M %p'),
							'total': round( float( temp_3.get('total', 0.0) ), 2 ),
							'count': round( float( temp_3.get('count', 0.0) ), 2 ),
							'average': round( float( temp_3.get('average', 0.0) ), 2 ),
							'minimum': round( float( temp_3.get('minimum', 0.0) ), 2 ),
							'maximum': round( float( temp_3.get('maximum', 0.0) ), 2 ),
						})
			return { 'count': len(dataset), 'data': dataset }
		except Exception as ex:
			return { 'data': { 'error': ex } }


#-------------------------------------------------------------------------------------------------------------------------------------------------#