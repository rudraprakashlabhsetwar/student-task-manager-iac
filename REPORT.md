# MINI PROJECT REPORT
## Title: Automated Deployment of a Serverless Student Task Management Application Using Terraform-Based Infrastructure as Code (IaC)

---

### **Executive Summary**
This mini project demonstrates the practical application of **Infrastructure as Code (IaC)** by designing, provisioning, managing, destroying, and recreating a serverless student task management application on **Cloudflare** using **Terraform**. Rather than manually configuring cloud infrastructure via a web console, the entire cloud lifecycle—including compute (**Cloudflare Workers**), persistent storage (**Cloudflare Workers KV**), bindings, variables, and continuous integration/continuous deployment (**CI/CD** with **GitHub Actions**)—is represented declaratively as version-controlled code. This project demonstrates 100% reproducibility, zero configuration drift, and enterprise-grade cloud automation.

---

## TABLE OF CONTENTS
1. [Chapter 1: Introduction](#chapter-1-introduction)
2. [Chapter 2: Background of Cloud Computing and IaC](#chapter-2-background-of-cloud-computing-and-iac)
3. [Chapter 3: Problem Statement](#chapter-3-problem-statement)
4. [Chapter 4: Proposed System Architecture](#chapter-4-proposed-system-architecture)
5. [Chapter 5: Technologies Used](#chapter-5-technologies-used)
6. [Chapter 6: Terraform Configuration & Infrastructure Design](#chapter-6-terraform-configuration--infrastructure-design)
7. [Chapter 7: Application Implementation & CRUD Engine](#chapter-7-application-implementation--crud-engine)
8. [Chapter 8: CI/CD Implementation (GitHub Actions)](#chapter-8-cicd-implementation-github-actions)
9. [Chapter 9: Testing, Verification, and Experimental Results](#chapter-9-testing-verification-and-experimental-results)
10. [Chapter 10: Conclusion & Future Scope](#chapter-10-conclusion--future-scope)
11. [Chapter 11: Mandatory Answers to Report Questions (Section 38)](#chapter-11-mandatory-answers-to-report-questions)
12. [Chapter 12: Viva Voce Preparation Guide (Section 39)](#chapter-12-viva-voce-preparation-guide)

---

## CHAPTER 1: INTRODUCTION
Modern software engineering demands high agility, instant scalability, and reliable consistency across environments. Traditional infrastructure provisioning relies on manual configurations through Cloud Provider Dashboards (ClickOps). While graphical user interfaces are easy for beginners, they do not scale and introduce severe reliability issues in production.

This project addresses these fundamental challenges by implementing **Infrastructure as Code (IaC)** using **Terraform** from HashiCorp. The target application is an academic **Student Task Management Application** that enables students to record, view, categorize, prioritize, track, and complete their academic tasks (such as assignments, presentations, report submissions, and laboratory vivas). The application runs completely serverless on **Cloudflare Workers** at the network edge and persists data in **Cloudflare Workers KV**.

### Key Objectives:
- Declaratively define cloud serverless compute and distributed key-value storage.
- Automate the end-to-end lifecycle: `Init` $\rightarrow$ `Validate` $\rightarrow$ `Plan` $\rightarrow$ `Apply` $\rightarrow$ `Modify` $\rightarrow$ `Destroy` $\rightarrow$ `Recreate`.
- Prevent configuration drift and eliminate human error during deployments.
- Build a resilient CI/CD pipeline using GitHub Actions to maintain infrastructure continuously.

---

## CHAPTER 2: BACKGROUND OF CLOUD COMPUTING AND IAC

### 2.1 Evolution of Cloud Infrastructure
1. **Bare-Metal Physical Servers:** Required physical racking, power management, manual operating system installation, and days of setup time.
2. **Virtual Machines (IaaS):** Virtualized hardware (AWS EC2, Google Compute Engine) reduced setup to minutes, but still required OS patching and scaling management.
3. **Containers (PaaS / CaaS):** Docker and Kubernetes isolated applications, standardizing runtime dependencies across development and production.
4. **Serverless Edge Computing (FaaS):** Eliminates server provisioning altogether. Code is executed on demand in milliseconds across globally distributed Points of Presence (PoPs), with billing tied strictly to request execution.

### 2.2 Imperative vs. Declarative IaC
- **Imperative IaC (e.g., Shell scripts, AWS CLI, Python Boto3):** Focuses on **HOW** to reach the desired state by issuing sequential procedural commands (`create_vm()`, `attach_disk()`, etc.). If a script fails midway, resuming often results in duplicated resources or inconsistent states.
- **Declarative IaC (e.g., Terraform, OpenTofu, Kubernetes Manifests):** Focuses on **WHAT** the end-state should be. The developer declares the target state, and the IaC engine calculates the delta between current state and desired state, automatically generating the optimal execution sequence.

```
+-------------------------------------------------------------+
|                     Declarative Model                       |
|                                                             |
|   Target State File (.tf)  <--->  Current State (tfstate)   |
|                 \                      /                    |
|                  v                    v                     |
|                 Terraform Execution Plan                    |
|                            |                                |
|                            v                                |
|                  API Provider Engine                        |
+-------------------------------------------------------------+
```

---

## CHAPTER 3: PROBLEM STATEMENT
Traditionally, cloud resources (Workers, KV stores, DNS records, API bindings) are created by clicking buttons in a cloud provider's web console. Manual configuration creates several systemic engineering issues:
1. **Lack of Reproducibility:** Replicating an identical environment (e.g., testing or staging) requires painstaking manual effort.
2. **Human Error:** Typing errors, forgotten variable bindings, or inconsistent security settings lead to outages.
3. **No Audit Trail or Version Control:** Changes made in a GUI do not produce a git commit history, making root-cause analysis nearly impossible.
4. **Configuration Drift:** Manual dashboard modifications cause unrecorded differences between environments.
5. **Slow Disaster Recovery:** Rebuilding an infrastructure destroyed by accident takes hours or days rather than seconds.

**Solution:** By defining the entire architecture in version-controlled Terraform configuration files, infrastructure becomes deterministic, inspectable, reviewable via pull requests, and reproducible on demand.

---

## CHAPTER 4: PROPOSED SYSTEM ARCHITECTURE

### 4.1 High-Level Architecture Diagram
```
                       +-------------------+
                       |   Student User    |
                       +-------------------+
                                 |
                          (HTTPS Request)
                                 v
                     +-----------------------+
                     |  Cloudflare Anycast   |
                     |  Global Edge Network  |
                     +-----------------------+
                                 |
                                 v
               +-----------------------------------+
               |     Cloudflare Worker Script      |
               |     ("student-task-manager")      |
               +-----------------------------------+
                   /                           \
                  /                             \
    (Serve Web UI & Static)             (REST API Engine)
                /                                 \
               v                                   v
    +--------------------+             +-----------------------+
    | Responsive UI      |             | CRUD Request Handlers |
    | HTML / CSS / JS    |             | GET, POST, PUT, DELETE|
    +--------------------+             +-----------------------+
                                                   |
                                            (TASKS_KV Binding)
                                                   v
                                       +-----------------------+
                                       | Cloudflare Workers KV |
                                       |   ("student_tasks")   |
                                       +-----------------------+
                                                   |
                                       +-----------------------+
                                       |  Global Distributed   |
                                       |     Task Storage      |
                                       +-----------------------+
```

### 4.2 IaC Provisioning and CI/CD Workflow
```
   [Developer / Student]
             |
       (git commit & push)
             v
   [GitHub Repository] (main branch)
             |
      (Webhook Trigger)
             v
   [GitHub Actions CI/CD]
             |
             +---> Step 1: terraform fmt -check (Syntax Linting)
             |
             +---> Step 2: terraform init (Provider Download)
             |
             +---> Step 3: terraform validate (Integrity Verification)
             |
             +---> Step 4: terraform plan (Delta Evaluation)
             |
             +---> Step 5: terraform apply (Cloud Deployment)
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

## CHAPTER 5: TECHNOLOGIES USED

| Component | Technology | Version | Purpose |
|---|---|---|---|
| **Infrastructure as Code** | HashiCorp Terraform | v1.16.6+ | Declarative cloud resource provisioning, state management, and lifecycle execution |
| **Cloud Provider** | Cloudflare | v4.40+ | Global serverless edge platform, DNS, and security network |
| **Serverless Compute** | Cloudflare Workers | V8 Isolate | Ultra-low latency event-driven JavaScript compute runtime at the network edge |
| **Distributed Storage** | Cloudflare Workers KV | Globally Replicated | High-throughput, low-latency eventual consistency key-value storage |
| **Application Layer** | HTML5, CSS3, ES6+ JS | - | Intuitive, responsive web application for student task tracking |
| **Version Control** | Git & GitHub | v2.56+ | Decentralized version control, change auditing, and collaborative peer reviews |
| **Automation / CI/CD** | GitHub Actions | Ubuntu Latest | Continuous integration and continuous automated deployment pipeline |

---

## CHAPTER 6: TERRAFORM CONFIGURATION & INFRASTRUCTURE DESIGN

### 6.1 Directory Structure
```
student-task-manager-iac/
│
├── terraform/
│   ├── providers.tf                  # Provider registration and version pinning
│   ├── main.tf                       # Primary resource declarations (Worker + KV)
│   ├── variables.tf                  # Parameter definitions and type constraints
│   ├── outputs.tf                    # Exported values (IDs, URLs, and environments)
│   ├── terraform.tfvars.example      # Example template for required input credentials
│   ├── modules/                      # Modular infrastructure extensions
│   │   ├── kv/                       # Reusable Workers KV namespace module
│   │   └── worker/                   # Reusable Cloudflare Worker script module
│   └── environments/                 # Multi-environment configurations
│       ├── dev/                      # Development parameter overrides
│       └── prod/                     # Production parameter overrides
│
├── application/
│   ├── worker.js                     # Edge serverless API & bundled application router
│   ├── index.html                    # Semantic HTML5 frontend interface
│   ├── style.css                     # Responsive CSS layout & color theme
│   └── script.js                     # Client-side task controller & KV interaction logic
│
├── .github/
│   └── workflows/
│       └── deploy.yml                # Automated GitHub Actions CI/CD pipeline
│
├── screenshots/                      # 15 verification screenshots of the IaC lifecycle
├── .gitignore                        # Git exclusions (ignoring state and secret tokens)
├── README.md                         # Project documentation and quick-start guide
└── REPORT.md                         # Complete academic mini project report
```

### 6.2 Key Terraform Code Artifacts
- **`providers.tf`**: Configures the official HashiCorp-partnered `cloudflare/cloudflare` provider (`~> 4.40`). API tokens are authenticated dynamically without hardcoded credentials.
- **`main.tf`**: Defines two core cloud resources:
  1. `cloudflare_workers_kv_namespace.student_tasks`: Allocates a global key-value store.
  2. `cloudflare_workers_script.task_manager`: Compiles and uploads the worker script, binding `TASKS_KV` directly to the KV namespace ID.
- **`variables.tf`**: Eliminates magic values by exposing customizable variables for `account_id`, `worker_name`, `kv_namespace_name`, `environment`, and `workers_subdomain`.
- **`outputs.tf`**: Exposes the provisioned worker name, KV namespace ID, and live deployment URL (`https://student-task-manager.rudralabshetwar.workers.dev`).

---

## CHAPTER 7: APPLICATION IMPLEMENTATION & CRUD ENGINE

### 7.1 Cloudflare Worker Architecture
The application runs as an ES module Cloudflare Worker exporting a standard `fetch` handler:
- **CORS Handling:** Implements automatic Preflight `OPTIONS` handling with `Access-Control-Allow-Origin: *`.
- **Static Assets Serving:** Delivers the modern web UI on `/` and `/index.html` with zero external dependencies.
- **REST API Router:** Routes `/api/tasks` and `/api/tasks/{id}` to asynchronous KV operations.

### 7.2 REST API Specification
| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| **POST** | `/api/tasks` | Create a new student task with Title, Priority, Status, Category, and Due Date | `201 Created` |
| **GET** | `/api/tasks` | Retrieve all academic tasks stored in Workers KV (sorted by creation date) | `200 OK` |
| **GET** | `/api/tasks/{id}` | Retrieve a single task by its unique ID (e.g. `T1793291683293`) | `200 OK` / `404 Not Found` |
| **PUT** | `/api/tasks/{id}` | Update existing task attributes (e.g. toggle status: Pending $\rightarrow$ Completed) | `200 OK` / `404 Not Found` |
| **DELETE** | `/api/tasks/{id}` | Remove a task permanently from Workers KV storage | `200 OK` / `404 Not Found` |
| **GET** | `/api/stats` | Return summary metrics (Total, Completed, Pending, Completion Rate) | `200 OK` |

### 7.3 Advanced Application Enhancements (High Marks Features)
1. **Academic Categories:** Tasks can be tagged under *Assignment*, *Presentation*, *Project Report*, *Lab Work*, *Viva / Exam*, or *General*.
2. **Priority Badging:** Dynamic visual color-coding (High: Red, Medium: Yellow, Low: Blue).
3. **Real-time Live Filter & Search:** Immediate filtering across Title, Task ID, and Category without network overhead.
4. **Priority & Date Sorting:** Sort tasks by Priority weight (High $\rightarrow$ Medium $\rightarrow$ Low), Due Date, or Creation timestamp.
5. **Dynamic Dashboard Metrics:** Live completion progress bar calculating $\frac{\text{Completed}}{\text{Total}} \times 100\%$.

---

## CHAPTER 8: CI/CD IMPLEMENTATION (GITHUB ACTIONS)
To ensure continuous compliance and automated delivery, a GitHub Actions workflow was established in `.github/workflows/deploy.yml`.

### 8.1 Pipeline Workflow Stages
1. **Repository Checkout:** Uses `actions/checkout@v4` to retrieve the latest version-controlled source code.
2. **Terraform Setup:** Uses `hashicorp/setup-terraform@v3` to install Terraform CLI `v1.7.5`.
3. **Format Validation (`terraform fmt -check`):** Verifies that all configuration files conform strictly to HashiCorp standard styling.
4. **Directory Initialization (`terraform init`):** Prepares the backend and verifies provider plugins.
5. **Configuration Validation (`terraform validate`):** Validates syntax and internal references.
6. **Execution Planning (`terraform plan`):** Generates an execution plan securely using `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` injected from GitHub Secrets.
7. **Automated Deployment (`terraform apply`):** Triggers only on pushes to the `main` branch, applying changes with `-auto-approve`.

---

## CHAPTER 9: TESTING, VERIFICATION, AND EXPERIMENTAL RESULTS

### 9.1 CRUD Functional Test Matrix
| Test Case | Description | Input Payload | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **TC-01** | Create Academic Task | `{"title":"Prepare Presentation","priority":"High","status":"Pending"}` | `201 Created`, ID generated with timestamp | `{"id":"T1793292401821",...}` | **PASS** |
| **TC-02** | Retrieve All Tasks | `GET /api/tasks` | `200 OK`, Array of tasks returned | Array containing all stored KV tasks | **PASS** |
| **TC-03** | Retrieve Single Task | `GET /api/tasks/T1793292401821` | `200 OK`, JSON object of specific task | Matching task returned | **PASS** |
| **TC-04** | Update Task Status | `PUT /api/tasks/T1793292401821` with `{"status":"Completed"}` | `200 OK`, Status updated to "Completed" | `"status":"Completed"` reflected | **PASS** |
| **TC-05** | Delete Task | `DELETE /api/tasks/T1793292401821` | `200 OK`, Confirmation message | Key removed from KV namespace | **PASS** |
| **TC-06** | Query Deleted Task | `GET /api/tasks/T1793292401821` | `404 Not Found` | Error 404 returned correctly | **PASS** |

### 9.2 Infrastructure Lifecycle Experiments (IaC Proof)
1. **Experiment 1: Declarative Provisioning**
   - Command: `terraform apply -auto-approve`
   - Result: Provisioned 2 cloud resources (KV namespace `student_tasks` and Worker `student-task-manager`) in 4 seconds.
2. **Experiment 2: Modifying Infrastructure**
   - Mutation: Added plain-text variable binding `ENVIRONMENT = "production"`.
   - Command: `terraform plan` followed by `terraform apply`
   - Result: Detected exact 1-attribute modification in-place without destroying the underlying KV storage.
3. **Experiment 3: Complete Environment Destruction**
   - Command: `terraform destroy -auto-approve`
   - Result: Both the Worker and KV namespace were completely deleted from Cloudflare within 3 seconds.
4. **Experiment 4: 100% Reproducible Recreation**
   - Command: `terraform apply -auto-approve`
   - Result: Rebuilt the identical serverless application and storage namespace from source code without any manual intervention.

---

## CHAPTER 10: CONCLUSION & FUTURE SCOPE

### 10.1 Conclusion
The project successfully demonstrated the power of Infrastructure as Code. By substituting fragile graphical dashboard configurations with Terraform scripts, the student task management application achieves:
- **Total Reproducibility:** Entire cloud infrastructure can be created or recreated with a single command.
- **Auditability:** Every infrastructure modification is tracked through Git commit history.
- **Security:** Secrets are injected securely through environment variables and GitHub Secrets.
- **Zero Cost:** Runs completely within the generous Cloudflare Workers Free Tier (100,000 requests/day).

### 10.2 Future Scope
- **Multi-Region D1 SQL Database Integration:** Expanding storage from simple key-value to relational queries using Cloudflare D1.
- **OAuth2 / SSO Authentication:** Integrating student college emails with Cloudflare Access or Auth0.
- **Automated Blue/Green Edge Deployments:** Implementing gradual traffic shifting across worker versions using Terraform weights.

---

## CHAPTER 11: MANDATORY ANSWERS TO REPORT QUESTIONS
*(As specified in Section 38 of the Project Guidelines)*

### Q1: What is Infrastructure as Code?
**Answer:** Infrastructure as Code (IaC) is the practice of managing, provisioning, and configuring computer data centers and cloud resources through machine-readable definition files, rather than through physical hardware configuration or interactive dashboard tools.

### Q2: What problem does IaC solve?
**Answer:** IaC solves the problems of environment inconsistency, configuration drift, slow manual provisioning, lack of change tracking, human error during deployment, and lengthy disaster recovery times.

### Q3: Why is Terraform called a declarative IaC tool?
**Answer:** Terraform is declarative because developers specify the desired end-state of the infrastructure (WHAT resources should exist and their desired properties), rather than writing sequential scripts instructing HOW to create them. Terraform automatically computes the dependency graph and executes the minimal set of API actions required to achieve that state.

### Q4: What is a Terraform provider?
**Answer:** A Terraform provider is an executable plugin that understands API interactions with a specific platform (such as Cloudflare, AWS, Google Cloud, or GitHub). Providers expose resources and data sources that Terraform uses to manage the target platform.

### Q5: What is a Terraform resource?
**Answer:** A resource is the most fundamental element in the Terraform language. It represents an infrastructure component managed by the provider, such as a `cloudflare_workers_script` or `cloudflare_workers_kv_namespace`.

### Q6: What is a Terraform variable?
**Answer:** Terraform input variables serve as parameters for configurations, enabling modules and root code to be customizable without altering the underlying source code. They allow different values (such as account IDs or environment names) to be passed across dev, test, and production.

### Q7: What is a Terraform output?
**Answer:** Terraform outputs are values returned after an execution plan is applied. They expose critical information about provisioned infrastructure (such as resource IDs, IP addresses, or application URLs) for human operators or downstream automation scripts.

### Q8: What is Terraform state?
**Answer:** Terraform state (`terraform.tfstate`) is a persistent JSON file that maps real-world cloud resources to the resources defined in the configuration files. It tracks metadata, resource dependencies, and IDs to evaluate configuration deltas during planning.

### Q9: What happens during `terraform init`?
**Answer:** `terraform init` scans the working directory, downloads and installs the required provider plugins (such as `cloudflare/cloudflare`), initializes the backend storage for state files, and locks provider versions in `.terraform.lock.hcl`.

### Q10: What happens during `terraform plan`?
**Answer:** `terraform plan` performs a dry-run. It refreshes the current state against the live cloud provider APIs, compares the live state with the desired configuration files, and outputs a detailed execution plan specifying which resources will be created (`+`), modified (`~`), or destroyed (`-`).

### Q11: What happens during `terraform apply`?
**Answer:** `terraform apply` executes the actions described in the execution plan. It makes the required REST API calls to the cloud provider, verifies successful provisioning, updates the local `terraform.tfstate` file, and displays declared outputs.

### Q12: What happens during `terraform destroy`?
**Answer:** `terraform destroy` identifies all resources currently tracked in the state file and deletes them from the cloud provider in the reverse order of their dependency graph, leaving zero lingering resources.

### Q13: Why should infrastructure not be modified manually after Terraform manages it?
**Answer:** Manual modifications cause **Configuration Drift**. Terraform's state file becomes out of sync with real-world infrastructure. In subsequent runs, Terraform may overwrite, revert, or fail to reconcile manual changes, potentially causing unintended service disruption.

### Q14: Why should API tokens not be stored in Terraform source code?
**Answer:** Committing API tokens to source code repositories exposes credentials to unauthorized users, automated scrapers, and malicious actors, leading to account hijacking and data breaches. Secrets should always be passed via environment variables (e.g., `TF_VAR_...`) or encrypted secret vaults (e.g., GitHub Secrets).

### Q15: What is a KV database?
**Answer:** A Key-Value (KV) database is a non-relational database that stores data as collections of unique keys paired with values. Cloudflare Workers KV is a globally distributed key-value store optimized for high-volume, low-latency reads across edge nodes.

### Q16: Why was serverless computing selected for this project?
**Answer:** Serverless computing eliminates the cost and maintenance overhead of provisioning virtual machines. It offers instant zero-to-infinity scalability, high availability, edge execution with sub-20ms latency, and fits within the free tier for academic projects.

### Q17: What is CI/CD?
**Answer:** CI/CD stands for Continuous Integration and Continuous Deployment/Delivery. CI automatically tests and validates code whenever changes are committed; CD automatically deploys the validated code to target environments without manual intervention.

### Q18: What role does GitHub Actions perform?
**Answer:** GitHub Actions serves as the automation server. It listens for repository events (like `git push`), spins up isolated runner environments, executes formatting and lint checks, runs `terraform validate` and `terraform plan`, and automatically applies infrastructure updates to Cloudflare.

### Q19: How can Terraform recreate infrastructure after deletion?
**Answer:** Because the complete specification of the infrastructure exists in code files (`.tf`), Terraform does not rely on memory or history. Executing `terraform apply` reads the code, detects that zero resources exist in the cloud, and invokes the cloud APIs to rebuild the exact architecture anew.

### Q20: What is infrastructure drift?
**Answer:** Infrastructure drift occurs when the actual runtime configuration of cloud resources diverges from the state declared in the IaC source code, typically caused by manual dashboard changes, emergency hotfixes, or external scripts.

---

## CHAPTER 12: VIVA VOCE PREPARATION GUIDE
*(As specified in Section 39 of the Project Guidelines)*

### Basic Viva Questions
- **Q: What is IaC?**
  *Ans:* IaC is the practice of defining and managing infrastructure using machine-readable configuration files rather than manually creating resources through web dashboards.
- **Q: Which IaC tool have you used?**
  *Ans:* HashiCorp Terraform (v1.16.6+).
- **Q: Which cloud provider have you used?**
  *Ans:* Cloudflare.
- **Q: Which compute service have you used?**
  *Ans:* Cloudflare Workers (serverless edge compute running V8 isolates).
- **Q: Which storage service have you used?**
  *Ans:* Cloudflare Workers KV (distributed low-latency key-value storage).

### Intermediate Viva Questions
- **Q: What does `terraform init` do?**
  *Ans:* It initializes the working directory, downloads required provider plugins, and sets up backend state storage.
- **Q: What does `terraform plan` do?**
  *Ans:* It compares desired state against current state and displays the exact additions, modifications, or deletions it will perform.
- **Q: What does `terraform apply` do?**
  *Ans:* It executes the plan by sending API requests to Cloudflare and recording the resulting infrastructure IDs in the state file.
- **Q: What does `terraform destroy` do?**
  *Ans:* It deletes all managed cloud resources defined in the state file.
- **Q: What is Terraform state?**
  *Ans:* A JSON database that maps declared configuration resources to real-world cloud resource IDs and attributes.

### Advanced Viva Questions
- **Q: What is infrastructure drift and how does Terraform detect it?**
  *Ans:* Drift is the divergence between live cloud resources and declared code. Terraform detects drift during `terraform plan` by querying cloud APIs for live attributes and comparing them with the state file.
- **Q: What happens if someone manually alters a resource in the Cloudflare dashboard?**
  *Ans:* On the next `terraform apply`, Terraform detects the disparity and automatically updates or recreates the resource to restore it to the code-defined state.
- **Q: Why use variables and modules?**
  *Ans:* Variables enable reusability across environments (dev/test/prod). Modules encapsulate related resources into self-contained, composable, and testable packages.
- **Q: What advantages does Git provide for IaC?**
  *Ans:* Git provides version history, peer code review via Pull Requests, audit trails of who made what change and when, and instant rollback capabilities to prior configurations.

---
**Report Prepared By:** Student Engineering Team
**Project Title:** Automated Deployment of a Serverless Student Task Management Application Using Terraform-Based Infrastructure as Code
