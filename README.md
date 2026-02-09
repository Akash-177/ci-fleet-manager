# CI Fleet Manager

Automated provisioning and management for Jenkins CI infrastructure.

## What This Does

Spins up multiple Jenkins instances using Terraform and provides Python tooling to monitor and manage them. Built to demonstrate platform automation patterns for CI/CD infrastructure.

## Quick Start

**Prerequisites:**
- Docker Desktop running
- Terraform installed
- Python 3.x with `docker` package

**Deploy:**
```bash
terraform init
terraform apply
```

**Manage:**
```bash
python manage_fleet.py
```

Access Jenkins instances at:
- http://localhost:8081
- http://localhost:8082  
- http://localhost:8083

**Cleanup:**
```bash
terraform destroy
```

## What's Included

**Infrastructure (Terraform):**
- `main.tf` - Provisions 3 Jenkins containers on a shared Docker network
- `variables.tf` - Configuration options (instance count, ports, image)
- `outputs.tf` - Returns URLs and instance info after deployment

**Automation (Python):**
- `manage_fleet.py` - Fleet monitoring tool with health checks and metrics

## Why This Approach

**Consistency:** All instances provisioned from the same Terraform config  
**Reproducibility:** Destroy and recreate identical environments anytime  
**Observability:** Python tooling gives real-time fleet status and metrics  
**Scalability:** Change instance count in variables.tf, reapply

## Scaling to Production

This uses Docker locally, but the same patterns apply to cloud:

- Swap Docker provider for AWS/Azure in Terraform
- Replace containers with EC2/VMs
- Add load balancer in front of instances
- Hook Python scripts to CloudWatch/Prometheus instead of Docker API

The IaC structure and automation patterns remain the same.

## Notes

Initial Jenkins setup requires unlocking each instance with the admin password from logs:
```bash
docker logs jenkins-master-1
```

Built for the Autodesk Platform Automation role application - demonstrates CI platform thinking and automation tooling.