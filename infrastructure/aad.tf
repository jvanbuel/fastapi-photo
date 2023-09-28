resource "azuread_application" "photo_app2" {
  display_name = "fastapi-photo-app2"
  owners       = [data.azurerm_client_config.current.object_id]
}

resource "azuread_application" "photo_app" {
  //TODO: delete after getting API developer role in AD
  display_name = "fastapi-photo-app"
}

resource "azuread_application_password" "client_secret" {
  application_object_id = azuread_application.photo_app2.object_id
}


resource "azuread_service_principal" "photo_app2" {
  application_id               = azuread_application.photo_app2.application_id
  app_role_assignment_required = false
}
