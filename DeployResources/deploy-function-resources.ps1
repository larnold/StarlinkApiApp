# Script creates the following Azure resources using Azure CLI commands:
# Resource Group, Storage Account, Function App, App Service Plan (Consumption Plan), 
# Application Insights (and an Action Group and Smart Detector Alert Rule used with Application Insights)

# Resource Names and Location
$ResourceGroupName = 'starlink-api_group'
$StorageAccountName = 'starlinkapistorage'
$FunctionAppName = 'starlinkapifunc'
$Location = 'australiaeast' # To see a list of all locations use: az account list-locations

# Create resource group 
az group create --name $ResourceGroupName --location $Location

# Create general-purpose storage account
#az storage account create --name $StorageAccountName --location $Location --resource-group $ResourceGroupName --sku Standard_LRS

# Create function app
az functionapp create --resource-group $ResourceGroupName --consumption-plan-location $Location --runtime python --runtime-version 3.11 --functions-version 4 --name $FunctionAppName --os-type linux  --storage-account $StorageAccountName

# Enable Managed Identity for the Function App:
az functionapp identity assign --name starlinkapifunc --resource-group starlink-api_group

# Retrieve the principal ID and enable the "Access Policy" under the Key Vault for Create/Update/Delete:

# Deploy/publish app
# func azure functionapp publish starlinkapifunc 
