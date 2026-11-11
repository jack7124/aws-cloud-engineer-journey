# Week 08 — Infrastructure as Code with Terraform

## Overview

This lab uses Terraform to define and deploy AWS networking infrastructure as code. Instead of manually creating resources in the AWS Console, `main.tf` describes the desired infrastructure:

- A VPC named `training-vpc-tf` with CIDR `10.1.0.0/16`
- Two public subnets and two private subnets across two Availability Zones
- An internet gateway and associated routing
- A single NAT gateway for outbound internet access from the private subnets

Terraform uses a declarative approach: the configuration describes the desired result, and Terraform determines the operations needed to reach it.

## terraform plan

`terraform plan` previews the changes Terraform proposes without creating, modifying, or deleting infrastructure.

By default, Terraform checks the current AWS resources tracked in its state and compares them with the configuration. It then shows which resources would be created, updated, replaced, or destroyed.

Common symbols include:

- `+` — Create a resource
- `~` — Update a resource in place
- `-` — Destroy a resource
- `-/+` — Replace a resource by destroying and recreating it

Reviewing the plan helps catch unexpected changes before they affect AWS.

## terraform apply

`terraform apply` performs the changes needed to make the infrastructure match the configuration.

Without a saved plan file, it generates a new plan and asks for confirmation. After entering `yes`, Terraform calls the AWS APIs, handles resource dependencies, and records the results in state.

For this lab, the initial apply provisions the VPC and its networking components. Running apply again with no configuration changes or infrastructure drift should produce no changes.

A separate `terraform plan` is a preview; a normal `terraform apply` recalculates the plan rather than automatically using that earlier preview.

## terraform destroy

`terraform destroy` proposes deleting all resources managed by the current Terraform state and workspace, then asks for confirmation before proceeding.

Terraform handles dependency ordering, such as removing dependent networking resources before deleting the VPC.

This command does not delete every resource in the AWS account. It targets the infrastructure managed by this configuration's state. It also leaves the Terraform configuration files available for rebuilding the environment later.

For this lab, destroying the infrastructure removes resources such as the NAT gateway to stop their ongoing charges.

## Why Terraform State Matters

Terraform state connects resource addresses in the configuration to actual AWS resource IDs. With the default local backend, this information is stored in `terraform.tfstate`.

For example, state tells Terraform which specific AWS VPC belongs to the VPC resource defined by the module. It also records resource attributes and dependency information.

State matters because it helps Terraform:

- Identify the existing resources it manages
- Determine the changes needed to match the configuration
- Track resources that need to be deleted
- Preserve dependency information for resource removal

Losing state does not delete the AWS resources. Instead, Terraform loses its mapping to them, which can lead to duplicate creation attempts or conflicts.

State can contain sensitive information, so it should be protected and excluded from Git. For team projects, a shared remote backend with access controls and state locking helps coordinate changes.

## Infrastructure Drift

Drift occurs when actual infrastructure differs from the Terraform configuration, such as when a managed subnet is manually changed in the AWS Console.

A normal plan refreshes information about tracked resources and can reveal these differences. Review the plan and decide whether to restore the configuration's intended settings or update the code to reflect the desired change.

Useful inspection commands:

```bash
terraform state list
terraform plan
```

Removing a resource from state only makes Terraform forget it; it does not delete the AWS resource.

## Lab Workflow

Run these commands from `week-08/`:

```bash
# Download the required providers and modules
terraform init

# Preview and review the proposed infrastructure changes
terraform plan

# Deploy the infrastructure after reviewing the new plan
terraform apply

# When finished, review and confirm the cleanup
terraform destroy
```

After deployment, verify that `training-vpc-tf` appears in AWS. After cleanup, confirm that Terraform reports `Destroy complete!` and the lab resources are gone.

## Git Hygiene

Add the following entries to `.gitignore`:

```gitignore
# Downloaded Terraform providers and modules
.terraform/

# Local state and backups
*.tfstate
*.tfstate.*

# Crash logs
crash.log
crash.*.log
```

Commit the Terraform configuration and `.terraform.lock.hcl` so the infrastructure definition and selected provider versions are recorded.
