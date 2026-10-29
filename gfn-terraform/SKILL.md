---
name: gfn-terraform
description: Use when writing or reviewing Terraform, OpenTofu, or terragrunt code, `.tf` files and modules. Prefers terraform templates over embedded strings for 5+ templates and keeps each `.tf` file under 1000 lines.
---
## Required standards

Apply together with skills `gfn-code` and `gfn-infrastructure`.

# Terraform 

1. For 5+ string templates prefer using terraform templates rather than embedding templates into .tf file
1. Maintain each .tf file under 1000 lines (flexible limit). Split module into meaningful/scoped .tf files, maintaining right balance between files amount and single file size.
