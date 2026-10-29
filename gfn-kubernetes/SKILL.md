---
name: gfn-kubernetes
description: Use when writing or reviewing Kubernetes manifests or Helm charts, e.g. `Chart.yaml`, `_helpers.tpl`, workload or PV/PVC definitions. Covers official chart reuse, keeping persistent data in a separate release, in-cluster secrets, and Terraform/Rancher annotation drift.
---
1. Don't make _helpers.tpl boierplate. Split it into meaningful files.
1. Prefer not to declare persistent data within the same release as application. The persistent data (pv/pvc/etc) should be in separate release because application reelases could be uninstalled during standart development process
1. When using helm charts, always look for official charts rather than reinventing the wheel. If chart exists consider pros and cons (vendor chart complexity vs vendoring own one) if you don't have a string opinion which to use - ask user. 
1. When secret is used only in cluster - like secret for in-cluster service for in-cluster consumer, prefer to born secret inside cluster and store it in cluster. 
1. When Terraform and/or rancher and/or helm are used for managing single cluster be aware of annotations ownership and drift detection, so terraform would not rollback rancher's ones.

