output "storage_account_name" {
  value = azurerm_storage_account.photo.name

}

output "azure_client_id" {
  value = azuread_application.photo_app2.application_id

}

output "azure_client_secret" {
  sensitive = true
  value     = azuread_application_password.client_secret.value
}

output "azure_tenant_id" {
  value = data.azurerm_client_config.current.tenant_id
}
