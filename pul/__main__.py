"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("rg-insights-01")

# Create an Azure resource (Storage Account)
account = storage.StorageAccount(
    "sainsightspul01",
    resource_group_name=resource_group.name,
    sku={
        "name": storage.SkuName.STANDARD_LRS,
    },
    kind=storage.Kind.STORAGE_V2,
    
)

storage.BlobContainer(
    "sainsightspul01-container-private",
    resource_group_name=resource_group.name,
    account_name=account.name,
    public_access=storage.PublicAccess.NONE,
)

storage.BlobContainer(
    "sainsightspul01-container-public",
    resource_group_name=resource_group.name,
    account_name=account.name,
    public_access=storage.PublicAccess.CONTAINER,
)

# Export the primary key of the Storage Account
primary_key = (
    pulumi.Output.all(resource_group.name, account.name)
    .apply(
        lambda args: storage.list_storage_account_keys(
            resource_group_name=args[0], account_name=args[1]
        )
    )
    .apply(lambda accountKeys: accountKeys.keys[0].value)
)

pulumi.export("primary_storage_key", primary_key)
