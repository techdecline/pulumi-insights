# Create a resource group for our storage account and blob container
az group create --name rg-insights --location germanywestcentral

# Create the storage account and set its default action for network access to 'AllowAccess' (so we can access the Blob container)
az storage account create --resource-group rg-insights --name sainsightsazcli02 --sku Standard_LRS --kind StorageV2 --location germanywestcentral --default-action Allow

# Set the storage account key so we can use it later
storageAccountName=$(az storage account show --name sainsightsazcli02 --query name -o tsv)
storageAccountKey=$(az storage account keys list --account-name $storageAccountName --query [0].value -o tsv)
export AZURE_STORAGE_ACCOUNT=$storageAccountName
export AZURE_STORAGE_ACCESS_KEY=$storageAccountKey

# Create the blob container
az storage container create --name blobcontainer --account-name $storageAccountName