import os
from dotenv import load_dotenv
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import ClientSecretCredential
from azure.ai.ml.entities import AmlCompute

# Load environment variables
load_dotenv()

# Azure credentials
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_SERVICE_PRINCIPAL_ID"]
client_secret = os.environ["AZURE_SERVICE_PRINCIPAL_PASSWORD"]

# Workspace configuration
workspace_name = "mlops-workspace-experiment"  # New workspace name
resource_group_name = "rg-mlops"
workspace_region = "eastus"

# Authenticate using Service Principal
service_principal = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Initialize Azure ML client
ml_client = MLClient(
    credential=service_principal,
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    workspace_name=workspace_name
)

# Define new workspace
workspace = Workspace(
    name=workspace_name,
    location=workspace_region,
    description="New Azure ML workspace created using Python SDK v2"
)

# Create workspace
print(f"Creating workspace: {workspace_name}...")

ws = ml_client.workspaces.begin_create(workspace).result()

# Display workspace details
print("\nWorkspace created successfully!")
print(f"Name: {ws.name}")
print(f"Location: {ws.location}")
print(f"Resource Group: {ws.resource_group}")
print(f"Workspace ID: {ws.id}")

# Define AML compute clusters
amlcomputes = {
    "cpu-cluster": {
        "size": "STANDARD_DS3_v2",
        "min_instances": 0,
        "max_instances": 3,
        "idle_time_before_scale_down": 240
    }
}

# Get existing compute targets
existing_computes = {
    compute.name for compute in ml_client.compute.list()
}

# Create AML compute targets
for ct_name, config in amlcomputes.items():

    if ct_name not in existing_computes:

        print(f"Creating compute cluster: {ct_name}...")

        compute_target = AmlCompute(
            name=ct_name,
            **config
        )

        # Create compute cluster and wait for completion
        compute_target = ml_client.compute.begin_create_or_update(
            compute_target
        ).result()

        print(f"Compute cluster '{ct_name}' created successfully!")
        print(f"Provisioning State: {compute_target.provisioning_state}")

    else:
        print(f"Compute cluster '{ct_name}' already exists.")

# Delete Azure ML workspace
# workspace_name = "mlops-workspace-experiment"

# print(f"Deleting workspace: {workspace_name}...")

# ml_client.workspaces.begin_delete(
#     name=workspace_name,
#     delete_dependent_resources=True
# ).result()

# print(f"Workspace '{workspace_name}' deleted successfully!")