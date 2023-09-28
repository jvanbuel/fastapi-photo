export STORAGE_ACCOUNT=$(terraform output -raw storage_account_name)
export AZURE_TENANT_ID=$(terraform output -raw azure_tenant_id)
export AZURE_CLIENT_ID=$(terraform output -raw azure_client_id)
export AZURE_CLIENT_SECRET=$(terraform output -raw azure_client_secret)