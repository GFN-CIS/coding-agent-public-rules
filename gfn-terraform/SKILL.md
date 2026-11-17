---
name: gfn-terraform
description: Use when writing or reviewing Terraform, OpenTofu, or terragrunt code, `.tf` files and modules. Prefers terraform templates over embedded strings for 5+ templates and keeps each `.tf` file under 1000 lines.
---
## Required standards

Apply together with skills `gfn-code` and `gfn-infrastructure`.

# Terraform 

1. For 5+ string templates prefer using terraform templates rather than embedding templates into .tf file
1. Maintain each .tf file under 1000 lines (flexible limit). Split module into meaningful/scoped .tf files, maintaining right balance between files amount and single file size.
2. Never put the terraform modules inside terragrunt folder. Terragrunt is for the environments while terraform is for entities inside this environment.
3. Treat terraform sub-modules are private unless parent module is not a library module. For example tf/modulea/submodule is private and cannot be imported from tf/moduleb/submoduleb, unless tf/modulea is library module by the nature. In the above case tf/modulea/submodule should be moved to tf/lib/library-name/submodule
