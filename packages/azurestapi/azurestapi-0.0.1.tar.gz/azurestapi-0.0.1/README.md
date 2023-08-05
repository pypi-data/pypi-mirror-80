# azurestapi

A Python Package to List Azure Resources for Different Azure Services!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install akashjeez.

```bash
pip install azurestapi
```

## Usage

```python

from azurestapi import AzuRestAPI
from datetime import datetime, timedelta

## Below Start & End Date is used for Metrics for Azure Servies Such as VM's CPU Percentage, App Service's Requests Count etc.
start_date = (datetime.now() - timedelta(days = 30)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

## Returns List of Attributes and Methods of this Package / Module.
print( dir( AzuRestAPI ) )

## Get the Token from https://docs.microsoft.com/en-us/rest/api/azure/
## Refer MSAL from https://docs.microsoft.com/en-us/azure/active-directory/develop/migrate-python-adal-msal
azure_object = AzuRestAPI( token = token )

## List All Azure Subscriptions for Logged in Account.
subscriptions = azure_object.List_Azure_Subscriptions()
subscriptions = azure_object.List_Azure_Subscriptions()['data']
print( subscriptions )

## For Dev/Tesing Subscription, Pass the Subscription ID and Name in Below Subscription.
subscriptions = [ {'subscription_id': '', 'subscription_name': ''} ]

## List Resource Groups and Resources under Resource Groups Across All Subscritions.
print( azure_object.List_Azure_Resource_Groups( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Resources( subscriptions = subscriptions ) )

## Azure Compute -> Virtual Machines, Disks, Snapshots Across All Subscritions.
print( azure_object.List_Azure_Virtual_Machines( subscriptions = subscriptions ) ) 
print( azure_object.List_Azure_Disks( subscriptions = subscriptions) )
print( azure_object.List_Azure_Snapshots( subscriptions = subscriptions) )

## List Azure Advisor Recommendations Across All Subscritions.
print( azure_object.List_Azure_Advisor_Recommendations( subscriptions = subscriptions ) )

## List Azure Containerization Across All Subscritions.
print( azure_object.List_Azure_Container_Registries( subscriptions = subscriptions ) )

## Azure Storage & Backups Across All Subscritions.
print( azure_object.List_Azure_Storage_Accounts( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Recovery_Service_Vaults( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Recovery_Service_Vault_Backups( subscriptions = subscriptions ) )

## Azure Classic Virtual Machines, Storage Accounts, Disks etc.
print( azure_object.List_Azure_Classic_Virtual_Machines( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Classic_Storage_Accounts( subscriptions = subscriptions ) )
print( azure_object.Get_Classic_VM_CPU_Utilization( subscriptions = subscriptions, 
	start_date = start_date, end_date = end_date ) )

## Azure PaaS -> Web App Servies, App Service Plans.
print( azure_object.List_Azure_App_Services( subscriptions = subscriptions ) )
print( azure_object.List_Azure_App_Service_Plans( subscriptions = subscriptions ) )

## Azure Databases -> SQL Databases, SQL Managed Instances, SQL VM.
print( azure_object.List_Azure_SQL_Virtual_Machines( subscriptions = subscriptions ) )
print( azure_object.List_Azure_SQL_Databases( subscriptions = subscriptions ) )
print( azure_object.List_Azure_SQL_Elastic_Pools( subscriptions = subscriptions ) )
print( azure_object.List_Azure_SQL_Managed_Instances( subscriptions ) )

## Azure Networking
print( azure_object.List_Azure_Public_IP_Addresses( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Virtual_Networks( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Network_Security_Groups( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Load_Balancers( subscriptions = subscriptions ) )
print( azure_object.List_Azure_CDN_Profiles( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Application_Gateways( subscriptions = subscriptions ) )

## Azure Metrics, Monitor, and Activity Logs.
resource_id = '/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP_NAME/providers/Microsoft.Web/sites/APP_SERVICE_NAME'
subscription_id = resource_id.split('/')[2]
print( azure_object.List_Azure_Resource_Type_Metrics( resource_id = resource_id ) )
print( azure_object.List_Azure_Activity_Logs( subscription_id = subscription_id,
	filter_query = f"eventTimestamp ge '{start_date}' and eventTimestamp le '{end_date}'" ) )
print( azure_object.Get_Azure_Resource_Metrics( resource_id = resource_id, metric_name = 'Requests', 
	timespan = f'{start_date}/{end_date}', interval = 'PT12H' ) )
print( azure_object.List_Azure_Log_Analytics_Workspaces( subscriptions = subscriptions ) )
print( azure_object.List_Azure_Application_Insights( subscriptions = subscriptions ) )

## Azure - AI/ML
print( azure_object.List_Azure_Cognitive_Service_Accounts( subscriptions = subscriptions ) )

## Azure Security Center
print( azure_object.List_Azure_Security_Center_Alerts( subscriptions = subscriptions ) )

```


## Contributing
Pull Requests are Welcome. For Major Changes, Please Open an issue First to Discuss What You Would like to Change.

Please Make Sure to Update Tests as Appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)