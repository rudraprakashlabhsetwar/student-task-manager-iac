# 🎓 Automated Deployment of a Serverless Student Task Management Application Using Terraform (IaC)

[![Terraform](https://img.shields.io/badge/Terraform-1.16+-623CE4?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers%20%26%20KV-F38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/SudhanshuLanjewar/student-task-manager-iac/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Mini Project on Infrastructure as Code (IaC)**
> Design, provision, manage, destroy, and recreate a serverless academic task management system on Cloudflare using HashiCorp Terraform.

---

## 🌐 Live Application
- **Production URL:** [https://student-task-manager.sudhanshulanjewar195.workers.dev](https://student-task-manager.sudhanshulanjewar195.workers.dev)
- **Edge Runtime:** Cloudflare V8 Serverless Isolates
- **Storage Backend:** Cloudflare Workers KV (Global Low-Latency Key-Value Store)

---

## 📋 Problem Statement & Purpose
Traditionally, cloud compute, storage, bindings, and environment variables are provisioned manually using web dashboards (*ClickOps*). Manual configuration suffers from:
- Inconsistent environments and human typographical errors.
- Lack of version control, audit trails, and peer review.
- Configuration drift and lengthy disaster recovery times.

**The Solution:** This project replaces manual configuration with **Infrastructure as Code (IaC)**. The entire cloud environment is declared in `.tf` configuration files, enabling automated provisioning, continuous delivery via GitHub Actions, and 100% reproducible disaster recreation.

---

## 🏛️ System Architecture

```
                    STUDENT / BROWSER
                            |
                     (HTTPS Request)
                            v
               +-------------------------+
               |    Cloudflare Edge      |
               | (300+ PoPs Worldwide)   |
               +-------------------------+
                            |
                            v
             +------------------------------+
             |   Cloudflare Worker Script   |
             |   ("student-task-manager")   |
             +------------------------------+
                /                        \
               /                          \
        (Serve Web UI)              (REST API Engine)
              /                            \
             v                              v
    +-----------------+           +--------------------+
    | Responsive UI   |           | CRUD Router        |
    | HTML, CSS, JS   |           | GET, POST, PUT, DEL|
    +-----------------+           +--------------------+
                                            |
                                   (TASKS_KV Binding)
                                            v
                                 +--------------------+
                                 | Cloudflare KV      |
                                 | ("student_tasks")  |
                                 +--------------------+
```

### Infrastructure Lifecycle Automation
```
   [Developer / Student]
             |
        (git push)
             v
   [GitHub Repository]
             |
             v
   [GitHub Actions CI/CD]
             |
             +---> terraform fmt -check
             +---> terraform init
             +---> terraform validate
             +---> terraform plan
             +---> terraform apply
                         |
                         v
              [Cloudflare REST API]
                         |
           +-------------+-------------+
           |                           |
           v                           v
  [Cloudflare Worker]         [Workers KV Namespace]
```

---

## ✨ Features

### Core Functional Requirements
- **FR1: Add Academic Task:** Create tasks with unique IDs, titles, priorities (High, Medium, Low), and statuses (Pending, Completed).
- **FR2: View Tasks:** Retrieve and display stored academic tasks in a clean, modern layout.
- **FR3: Update Task:** Toggle or mutate status between Pending and Completed.
- **FR4: Delete Task:** Permanently remove task records from storage with confirmation.
- **FR5: Persistent Storage:** Direct integration with Cloudflare Workers KV.

### Advanced Enhancements (For Higher Marks)
- **Academic Categories:** Tag tasks as *Assignment*, *Presentation*, *Project Report*, *Lab Work*, *Viva / Exam*, or *General*.
- **Due Dates / Deadlines:** Track assignment deadlines via HTML5 date inputs.
- **Real-Time Live Search:** Search instantly across Title, Task ID, and Category.
- **Multi-Filter & Sorting:** Filter by Status, Priority, or Category, and sort by Priority weight or Creation date.
- **Live Task Completion Statistics:** Visual dashboard displaying Total, Completed, Pending, and Completion Rate (%) with a dynamic progress bar.
- **Modular Terraform Code:** Includes reusable modules (`modules/kv`, `modules/worker`) and multi-environment examples (`dev`, `prod`).

---

## 📁 Project Directory Structure

```
student-task-manager-iac/
│
├── terraform/
│   ├── providers.tf                  # Provider definition (~> 4.40)
│   ├── main.tf                       # Cloud resources (Worker & KV)
│   ├── variables.tf                  # Reusable input variables
│   ├── outputs.tf                    # Deployment outputs & application URL
│   ├── terraform.tfvars.example      # Example input parameters template
│   ├── modules/                      # Reusable Terraform Modules (Section 35)
│   │   ├── kv/                       # Reusable Workers KV Namespace module
│   │   └── worker/                   # Reusable Worker Script module
│   └── environments/                 # Multi-Environment configs (Section 34)
│       ├── dev/                      # Development environment settings
│       └── prod/                     # Production environment settings
│
├── application/
│   ├── worker.js                     # Serverless edge API & frontend bundle
│   ├── index.html                    # Semantic HTML5 user interface
│   ├── style.css                     # Responsive styling & design tokens
│   └── script.js                     # Client-side controller & KV communication
│
├── .github/
│   └── workflows/
│       └── deploy.yml                # Automated GitHub Actions CI/CD workflow
│
├── screenshots/                      # 15 Complete IaC demonstration screenshots
├── .gitignore                        # Git exclusions for secrets and state
├── README.md                         # Project documentation
└── REPORT.md                         # Complete academic mini project report
```

---

## 🚀 Quick-Start Guide

### Prerequisites
- [Git](https://git-scm.com/) installed (`git --version`)
- [Terraform](https://developer.hashicorp.com/terraform/install) installed (`terraform --version`)
- Cloudflare Free Account with API Token having `Workers Scripts:Edit` and `Workers KV Storage:Edit` permissions.

### 1. Clone the Repository
```bash
git clone https://github.com/SudhanshuLanjewar/student-task-manager-iac.git
cd student-task-manager-iac/terraform
```

### 2. Set Up Credentials
Create `terraform.tfvars` from the provided example:
```bash
cp terraform.tfvars.example terraform.tfvars
```
Fill in your credentials:
```hcl
cloudflare_api_token = "your_actual_api_token"
account_id           = "your_actual_account_id"
worker_name          = "student-task-manager"
kv_namespace_name    = "student_tasks"
environment          = "production"
workers_subdomain    = "your-workers-subdomain"
```

Or export them as environment variables (recommended for security):
```powershell
# PowerShell
$env:TF_VAR_cloudflare_api_token="your_api_token"
$env:TF_VAR_account_id="your_account_id"
```
```bash
# Linux/macOS
export TF_VAR_cloudflare_api_token="your_api_token"
export TF_VAR_account_id="your_account_id"
```

### 3. Execute the Terraform Lifecycle

```bash
# Step 1: Initialize Terraform & Download Cloudflare Provider
terraform init

# Step 2: Format configuration code to standard style
terraform fmt

# Step 3: Validate syntax and internal references
terraform validate

# Step 4: Preview planned cloud resources
terraform plan

# Step 5: Provision Cloudflare Worker and Workers KV
terraform apply -auto-approve

# Step 6: Verify deployment outputs
terraform output
```

---

## 📡 REST API Reference

All endpoints accept and return JSON.

### 1. Create a Task
```bash
curl -X POST "https://student-task-manager.sudhanshulanjewar195.workers.dev/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Cloud Computing Assignment",
    "priority": "High",
    "status": "Pending",
    "category": "Assignment",
    "dueDate": "2026-11-05"
  }'
```
**Response (201 Created):**
```json
{
  "id": "T1793292401821",
  "title": "Complete Cloud Computing Assignment",
  "priority": "High",
  "status": "Pending",
  "category": "Assignment",
  "dueDate": "2026-11-05",
  "createdDate": "2026-10-29T16:46:41.821Z"
}
```

### 2. Get All Tasks
```bash
curl "https://student-task-manager.sudhanshulanjewar195.workers.dev/api/tasks"
```

### 3. Get Task by ID
```bash
curl "https://student-task-manager.sudhanshulanjewar195.workers.dev/api/tasks/T1793292401821"
```

### 4. Update Task Status
```bash
curl -X PUT "https://student-task-manager.sudhanshulanjewar195.workers.dev/api/tasks/T1793292401821" \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

### 5. Delete Task
```bash
curl -X DELETE "https://student-task-manager.sudhanshulanjewar195.workers.dev/api/tasks/T1793292401821"
```

---

## 🔄 Automated CI/CD Pipeline (GitHub Actions)

The repository includes an enterprise-grade CI/CD pipeline in `.github/workflows/deploy.yml`:
1. Triggers automatically on `push` or `pull_request` to `main`.
2. Validates code formatting via `terraform fmt -check`.
3. Validates syntax via `terraform validate`.
4. Runs `terraform plan` using encrypted GitHub Secrets (`CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`).
5. Executes automated zero-downtime deployment (`terraform apply`) directly to Cloudflare.

---

## 🧪 IaC Demonstration (Destroy & Recreate)

To demonstrate the core tenet of Infrastructure as Code:

```bash
# 1. Destroy the entire cloud environment
terraform destroy -auto-approve

# 2. Verify all resources are removed from Cloudflare
# (Application returns 404 / inactive)

# 3. Recreate the complete infrastructure from code
terraform apply -auto-approve
```
Within **3 seconds**, Terraform reconciles state and recreates the identical serverless application and KV storage namespace automatically!

---

## 📸 Screenshots Gallery
All 15 required verification screenshots are located in the `screenshots/` directory:
- `01_terraform_installation.png` - Terraform and Git environment validation
- `02_terraform_init.png` - Provider plugin installation and initialization
- `03_terraform_validate.png` - Configuration validation confirmation
- `04_terraform_plan.png` - Execution plan showing proposed cloud resources
- `05_terraform_apply.png` - Provisioning success and exported outputs
- `06_cloudflare_worker.png` - Cloudflare Workers dashboard and binding configuration
- `07_cloudflare_kv_namespace.png` - Cloudflare Workers KV namespace key-value data
- `08_working_web_application.png` - Modern student task management interface
- `09_create_operation.png` - Task creation operation (POST /api/tasks)
- `10_update_operation.png` - Task update operation (PUT /api/tasks/{id})
- `11_delete_operation.png` - Task deletion operation (DELETE /api/tasks/{id})
- `12_github_repository.png` - GitHub repository layout and commit history
- `13_github_actions_execution.png` - CI/CD pipeline successful run
- `14_terraform_destroy.png` - Automated infrastructure removal
- `15_infrastructure_recreation.png` - Reproducible infrastructure recreation

---

## 📖 Mini Project Report & Viva Voce
- **Full Report:** See [REPORT.md](REPORT.md) for the complete 10-chapter academic report.
- **Viva Voce Prep:** Chapter 11 & Chapter 12 of `REPORT.md` contain comprehensive answers to all 20 evaluation questions and 15 viva voce questions.

---

## 👥 Authors
- **Project Title:** Automated Deployment of a Serverless Student Task Management Application Using Terraform
- **Course:** Cloud Computing / Infrastructure as Code Mini Project
