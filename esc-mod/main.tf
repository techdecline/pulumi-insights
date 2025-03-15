provider "azurerm" {
    features {
      
    }
    resource_provider_registrations = "none"
    subscription_id = "a1bb21f8-fca2-4832-8b35-4fc83f310690"
}
resource "azurerm_storage_account" "sa" {
  name                = "saesc01"
  resource_group_name = data.azurerm_resource_group.rg-insights.name
  location            = data.azurerm_resource_group.rg-insights.location
#   account_kind = "BlobStorage"
  account_kind = "StorageV2"
  account_replication_type = "LRS"
  account_tier = "Standard"
  tags = {
    environment = "dev"
  }
}

data "azurerm_resource_group" "rg-insights" {
  name     = "rg-insights"
}

output "storage_account_id" {
  value = azurerm_storage_account.sa.id
}

output "dummy" {
  value = "foobar"
}