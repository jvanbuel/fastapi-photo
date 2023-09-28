resource "azurerm_resource_group" "rg" {
  name     = "fastapi-photo"
  location = "West Europe"
}

resource "azurerm_storage_account" "photo" {
  name                     = "fastapiphoto"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
}

resource "azurerm_storage_container" "photo_raw" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.photo.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "photo_clean" {
  name                  = "clean"
  storage_account_name  = azurerm_storage_account.photo.name
  container_access_type = "private"
}


resource "azurerm_role_assignment" "photo_app2" {
  scope                = azurerm_storage_account.photo.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.photo_app2.object_id
}
