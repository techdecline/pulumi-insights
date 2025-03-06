provider "azurerm" {
    features {
      
    }
    resource_provider_registrations = "none"
    subscription_id = "a1bb21f8-fca2-4832-8b35-4fc83f310690"
}
resource "azurerm_storage_account" "sa" {
  name                = "sainsightstf01"
  resource_group_name = data.azurerm_resource_group.rg-insights.name
  location            = data.azurerm_resource_group.rg-insights.location
  account_kind = "BlobStorage"
#   account_kind = "StorageV2"
  account_replication_type = "LRS"
  account_tier = "Standard"
  tags = {
    environment = "dev"
  }
}

resource "azurerm_storage_container" "container-private" {
  storage_account_id = azurerm_storage_account.sa.id
  name        = "sainsightstf01-container-private"
  container_access_type = "private"
}

resource "azurerm_storage_container" "container-public" {
  storage_account_id = azurerm_storage_account.sa.id
  name        = "sainsightstf01-container-public"
  container_access_type = "container"
}

data "azurerm_resource_group" "rg-insights" {
  name     = "rg-insights"
}