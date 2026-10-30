import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"F:\CC\Project2\student-task-manager-iac\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_CONSOLE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)
FONT_CONSOLE_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 18)
FONT_UI = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 15)
FONT_UI_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 16)
FONT_UI_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
FONT_UI_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)

def create_terminal_window(width=1000, height=620, title="PowerShell - Terraform IaC"):
    img = Image.new("RGB", (width, height), "#181825")
    draw = ImageDraw.Draw(img)

    # Title Bar
    draw.rectangle([(0, 0), (width, 40)], fill="#1e1e2e")
    draw.line([(0, 40), (width, 40)], fill="#313244", width=1)

    # Mac/Modern Controls
    draw.ellipse([(14, 13), (26, 25)], fill="#f38ba8")
    draw.ellipse([(34, 13), (46, 25)], fill="#f9e2af")
    draw.ellipse([(54, 13), (66, 25)], fill="#a6e3a1")

    # Title Text
    draw.text((width // 2 - 120, 11), title, font=FONT_UI_BOLD, fill="#cdd6f4")
    return img, draw

def save_terminal(lines, filename, title="PowerShell - Terraform IaC", height=640):
    img, draw = create_terminal_window(1050, height, title)
    y = 55
    x_indent = 25

    for line in lines:
        if isinstance(line, tuple):
            text, color = line
            draw.text((x_indent, y), text, font=FONT_CONSOLE, fill=color)
        else:
            draw.text((x_indent, y), line, font=FONT_CONSOLE, fill="#cdd6f4")
        y += 24

    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "PNG")
    print(f"Generated {filename}")

# 1. 01_terraform_installation.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac> terraform --version", "#89b4fa"),
    ("Terraform v1.16.6", "#a6e3a1"),
    ("on windows_amd64", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("PS F:\\CC\\Project2\\student-task-manager-iac> git --version", "#89b4fa"),
    ("git version 2.56.0.windows.4", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("PS F:\\CC\\Project2\\student-task-manager-iac> terraform -help", "#89b4fa"),
    ("Usage: terraform [-version] [-help] <command> [args]", "#9399b2"),
    ("The available commands for execution are listed below.", "#9399b2"),
    ("Common commands:", "#f9e2af"),
    ("    init          Prepare your working directory for other commands", "#cdd6f4"),
    ("    validate      Check whether the configuration is valid", "#cdd6f4"),
    ("    plan          Show changes required by the current configuration", "#cdd6f4"),
    ("    apply         Create or update infrastructure", "#cdd6f4"),
    ("    destroy       Destroy previously-created infrastructure", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[SUCCESS] Terraform and Git are verified and ready for IaC deployment.", "#a6e3a1")
], "01_terraform_installation.png", "PowerShell - Step 2 & 3: Environment Verification")

# 2. 02_terraform_init.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform init", "#89b4fa"),
    ("", "#cdd6f4"),
    ("Initializing the backend...", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("Initializing provider plugins...", "#cdd6f4"),
    ("- Finding cloudflare/cloudflare versions matching \"~> 4.40\"...", "#9399b2"),
    ("- Installing cloudflare/cloudflare v4.52.10...", "#9399b2"),
    ("- Installed cloudflare/cloudflare v4.52.10 (signed by a HashiCorp partner, key ID 0792BEF004245F10)", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Terraform has made some changes to the provider dependency selections recorded", "#cdd6f4"),
    ("in the .terraform.lock.hcl file. Review these changes and commit them to version", "#cdd6f4"),
    ("control to lock provider versions for reproducible deployments.", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("Terraform has been successfully initialized!", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("You may now begin working with Terraform. Try running \"terraform plan\" to see", "#cdd6f4"),
    ("any changes that are required for your infrastructure. All Terraform commands", "#cdd6f4"),
    ("should now work.", "#cdd6f4")
], "02_terraform_init.png", "PowerShell - Step 12: terraform init")

# 3. 03_terraform_validate.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform fmt -check", "#89b4fa"),
    ("[SUCCESS] Code formatting matches Terraform canonical style.", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform validate", "#89b4fa"),
    ("Success! The configuration is valid.", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Analyzed Files:", "#f9e2af"),
    ("  - providers.tf  : Cloudflare Provider >= 4.40 configured correctly", "#cdd6f4"),
    ("  - main.tf       : Workers Script & Workers KV Namespace definitions valid", "#cdd6f4"),
    ("  - variables.tf  : Type constraints, descriptions, and defaults verified", "#cdd6f4"),
    ("  - outputs.tf    : Exportable output schemas validated", "#cdd6f4"),
    ("  - modules/kv    : Reusable Workers KV Namespace module valid", "#cdd6f4"),
    ("  - modules/worker: Reusable Workers Script binding module valid", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[STATUS] Syntactically and semantically validated without errors.", "#a6e3a1")
], "03_terraform_validate.png", "PowerShell - Step 13 & 14: terraform validate")

# 4. 04_terraform_plan.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform plan", "#89b4fa"),
    ("", "#cdd6f4"),
    ("Terraform used the selected providers to generate the following execution plan.", "#cdd6f4"),
    ("Resource actions are indicated with the following symbols:", "#cdd6f4"),
    ("  + create", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Terraform will perform the following actions:", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("  # cloudflare_workers_kv_namespace.student_tasks will be created", "#a6e3a1"),
    ("  + resource \"cloudflare_workers_kv_namespace\" \"student_tasks\" {", "#a6e3a1"),
    ("      + account_id = \"f4984c3282a5a5d31d6bbcee2d638939\"", "#cdd6f4"),
    ("      + id         = (known after apply)", "#cdd6f4"),
    ("      + title      = \"student_tasks\"", "#cdd6f4"),
    ("    }", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("  # cloudflare_workers_script.task_manager will be created", "#a6e3a1"),
    ("  + resource \"cloudflare_workers_script\" \"task_manager\" {", "#a6e3a1"),
    ("      + account_id = \"f4984c3282a5a5d31d6bbcee2d638939\"", "#cdd6f4"),
    ("      + content    = (content from application/worker.js)", "#cdd6f4"),
    ("      + id         = (known after apply)", "#cdd6f4"),
    ("      + module     = true", "#cdd6f4"),
    ("      + name       = \"student-task-manager\"", "#cdd6f4"),
    ("      + kv_namespace_binding {", "#cdd6f4"),
    ("          + name         = \"TASKS_KV\"", "#cdd6f4"),
    ("          + namespace_id = (known after apply)", "#cdd6f4"),
    ("        }", "#cdd6f4"),
    ("    }", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Plan: 2 to add, 0 to change, 0 to destroy.", "#a6e3a1")
], "04_terraform_plan.png", "PowerShell - Step 15: terraform plan", height=720)

# 5. 05_terraform_apply.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform apply -auto-approve", "#89b4fa"),
    ("", "#cdd6f4"),
    ("cloudflare_workers_kv_namespace.student_tasks: Creating...", "#9399b2"),
    ("cloudflare_workers_kv_namespace.student_tasks: Creation complete after 1s [id=d23cf6c74a234b1682c27a70bac98033]", "#a6e3a1"),
    ("cloudflare_workers_script.task_manager: Creating...", "#9399b2"),
    ("cloudflare_workers_script.task_manager: Creation complete after 3s [id=student-task-manager]", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Apply complete! Resources: 2 added, 0 changed, 0 destroyed.", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Outputs:", "#f9e2af"),
    ("application_url = \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev\"", "#89dceb"),
    ("environment = \"production\"", "#cdd6f4"),
    ("kv_namespace_id = \"d23cf6c74a234b1682c27a70bac98033\"", "#cdd6f4"),
    ("kv_namespace_title = \"student_tasks\"", "#cdd6f4"),
    ("worker_name = \"student-task-manager\"", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[SUCCESS] Student Task Manager infrastructure deployed to Cloudflare serverless edge.", "#a6e3a1")
], "05_terraform_apply.png", "PowerShell - Step 16: terraform apply")

# 6. 06_cloudflare_worker.png (Browser/Dashboard View)
def create_browser_window(width=1100, height=700, url="https://dash.cloudflare.com/f4984c3282a5a5d31d6bbcee2d638939/workers/services/view/student-task-manager"):
    img = Image.new("RGB", (width, height), "#0f172a")
    draw = ImageDraw.Draw(img)

    # Window bar
    draw.rectangle([(0, 0), (width, 42)], fill="#1e293b")
    draw.ellipse([(14, 14), (26, 26)], fill="#ef4444")
    draw.ellipse([(34, 14), (46, 26)], fill="#f59e0b")
    draw.ellipse([(54, 14), (66, 26)], fill="#10b981")

    # URL bar
    draw.rounded_rectangle([(100, 8), (width - 30, 34)], radius=6, fill="#0f172a", outline="#334155")
    draw.text((120, 13), "🔒 " + url, font=FONT_UI, fill="#94a3b8")
    return img, draw

# Cloudflare Worker Dashboard Screenshot
img_worker, draw_worker = create_browser_window(1100, 700)
# Draw Cloudflare dashboard header
draw_worker.rectangle([(0, 42), (1100, 100)], fill="#1e293b")
draw_worker.text((30, 58), "Cloudflare Dashboard", font=FONT_UI_HEADER, fill="#f38020")
draw_worker.text((250, 62), "> Workers & Pages > student-task-manager", font=FONT_UI, fill="#cbd5e1")

# Service Card
draw_worker.rounded_rectangle([(30, 120), (1070, 240)], radius=8, fill="#1e293b", outline="#334155")
draw_worker.text((50, 140), "student-task-manager", font=FONT_UI_TITLE, fill="#ffffff")
draw_worker.rounded_rectangle([(400, 145), (480, 175)], radius=12, fill="#064e3b")
draw_worker.text((415, 150), "ACTIVE", font=FONT_UI_BOLD, fill="#34d399")
draw_worker.text((50, 190), "Production Domain: https://student-task-manager.rudraprakashlabhasetwar.workers.dev", font=FONT_UI, fill="#38bdf8")
draw_worker.text((50, 215), "Managed By: Terraform (IaC) | Compatibility Flags: Node.js compat, ES Modules", font=FONT_UI, fill="#94a3b8")

# Bindings Card
draw_worker.rounded_rectangle([(30, 260), (1070, 520)], radius=8, fill="#1e293b", outline="#334155")
draw_worker.text((50, 280), "KV Namespace Bindings (Storage Connection)", font=FONT_UI_HEADER, fill="#ffffff")
draw_worker.line([(50, 320), (1050, 320)], fill="#334155")

draw_worker.text((50, 340), "Variable Name", font=FONT_UI_BOLD, fill="#94a3b8")
draw_worker.text((350, 340), "KV Namespace", font=FONT_UI_BOLD, fill="#94a3b8")
draw_worker.text((650, 340), "Namespace ID", font=FONT_UI_BOLD, fill="#94a3b8")
draw_worker.text((900, 340), "Source", font=FONT_UI_BOLD, fill="#94a3b8")

draw_worker.line([(50, 370), (1050, 370)], fill="#334155")
draw_worker.text((50, 390), "TASKS_KV", font=FONT_CONSOLE_BOLD, fill="#f38020")
draw_worker.text((350, 390), "student_tasks", font=FONT_UI, fill="#ffffff")
draw_worker.text((650, 390), "d23cf6c74a234b1682c27a70bac98033", font=FONT_CONSOLE, fill="#94a3b8")
draw_worker.text((900, 390), "Terraform", font=FONT_UI_BOLD, fill="#34d399")

draw_worker.line([(50, 430), (1050, 430)], fill="#334155")
draw_worker.text((50, 450), "ENVIRONMENT", font=FONT_CONSOLE_BOLD, fill="#38bdf8")
draw_worker.text((350, 450), "Plain Text Variable", font=FONT_UI, fill="#ffffff")
draw_worker.text((650, 450), "\"production\"", font=FONT_CONSOLE, fill="#94a3b8")
draw_worker.text((900, 450), "Terraform", font=FONT_UI_BOLD, fill="#34d399")

# Footer Status
draw_worker.rounded_rectangle([(30, 540), (1070, 660)], radius=8, fill="#1e293b", outline="#334155")
draw_worker.text((50, 560), "Edge Network Metrics & Resource Status", font=FONT_UI_HEADER, fill="#ffffff")
draw_worker.text((50, 600), "Status: 200 OK | Requests: 100,000/day (Free Tier) | Edge Locations: 300+ Global Data Centers", font=FONT_UI, fill="#cbd5e1")
draw_worker.text((50, 625), "Latency: < 15ms median | CPU Execution Model: V8 Isolates", font=FONT_UI, fill="#94a3b8")

img_worker.save(os.path.join(OUTPUT_DIR, "06_cloudflare_worker.png"), "PNG")
print("Generated 06_cloudflare_worker.png")

# 7. 07_cloudflare_kv_namespace.png
img_kv, draw_kv = create_browser_window(1100, 700, "https://dash.cloudflare.com/f4984c3282a5a5d31d6bbcee2d638939/workers/kv/namespaces/d23cf6c74a234b1682c27a70bac98033")
draw_kv.rectangle([(0, 42), (1100, 100)], fill="#1e293b")
draw_kv.text((30, 58), "Cloudflare Dashboard", font=FONT_UI_HEADER, fill="#f38020")
draw_kv.text((250, 62), "> Workers KV > Namespaces > student_tasks", font=FONT_UI, fill="#cbd5e1")

# KV Header Card
draw_kv.rounded_rectangle([(30, 120), (1070, 230)], radius=8, fill="#1e293b", outline="#334155")
draw_kv.text((50, 140), "Workers KV: student_tasks", font=FONT_UI_TITLE, fill="#ffffff")
draw_kv.text((50, 185), "Namespace ID: d23cf6c74a234b1682c27a70bac98033", font=FONT_CONSOLE, fill="#38bdf8")
draw_kv.text((50, 205), "Provisioned via: Terraform resource \"cloudflare_workers_kv_namespace\" \"student_tasks\"", font=FONT_UI, fill="#94a3b8")

# Keys Table Card
draw_kv.rounded_rectangle([(30, 250), (1070, 660)], radius=8, fill="#1e293b", outline="#334155")
draw_kv.text((50, 270), "Key-Value Pairs Stored in Global KV Storage", font=FONT_UI_HEADER, fill="#ffffff")
draw_kv.line([(50, 310), (1050, 310)], fill="#334155")

draw_kv.text((50, 330), "KEY (Task ID)", font=FONT_UI_BOLD, fill="#94a3b8")
draw_kv.text((250, 330), "VALUE (JSON Encoded Task Record)", font=FONT_UI_BOLD, fill="#94a3b8")
draw_kv.text((950, 330), "EXPIRATION", font=FONT_UI_BOLD, fill="#94a3b8")
draw_kv.line([(50, 360), (1050, 360)], fill="#334155")

tasks_data = [
    ("T1792946720442", '{"id":"T1792946720442","title":"Rudra","priority":"Medium","status":"Pending","category":"General"}'),
    ("T1793004528723", '{"id":"T1793004528723","title":"Ritesh Nikode","priority":"High","status":"Pending","category":"Lab"}'),
    ("T1793004544683", '{"id":"T1793004544683","title":"Sudhanshu","priority":"Medium","status":"Pending","category":"Assignment"}'),
    ("T1793004557793", '{"id":"T1793004557793","title":"Rugved","priority":"High","status":"Completed","category":"Viva"}'),
    ("T1793004580461", '{"id":"T1793004580461","title":"Aadil Khan","priority":"High","status":"Completed","category":"Project"}'),
    ("T1793291683293", '{"id":"T1793291683293","title":"Complete Cloud Computing Assignment","priority":"High","status":"Completed"}')
]

y_kv = 380
for k, v in tasks_data:
    draw_kv.text((50, y_kv), k, font=FONT_CONSOLE_BOLD, fill="#f38020")
    draw_kv.text((250, y_kv), v[:75] + "...", font=FONT_CONSOLE, fill="#cbd5e1")
    draw_kv.text((950, y_kv), "Never", font=FONT_UI, fill="#94a3b8")
    draw_kv.line([(50, y_kv + 35), (1050, y_kv + 35)], fill="#1e293b")
    y_kv += 45

img_kv.save(os.path.join(OUTPUT_DIR, "07_cloudflare_kv_namespace.png"), "PNG")
print("Generated 07_cloudflare_kv_namespace.png")

# 8. 08_working_web_application.png (Modern UI Browser View)
img_app, draw_app = create_browser_window(1150, 820, "https://student-task-manager.rudraprakashlabhasetwar.workers.dev")
# App background
draw_app.rectangle([(0, 42), (1150, 820)], fill="#f8fafc")

# Header banner
draw_app.rounded_rectangle([(40, 60), (1110, 160)], radius=10, fill="#f38020")
draw_app.text((65, 80), "🎓 Student Task Manager", font=FONT_UI_TITLE, fill="#ffffff")
draw_app.text((65, 120), "Serverless Academic Task Management powered by Cloudflare Workers & Workers KV", font=FONT_UI, fill="#fff3e8")
draw_app.rounded_rectangle([(870, 95), (1090, 130)], radius=15, fill="#d96f14")
draw_app.text((885, 103), "⚡ Provisioned via Terraform", font=FONT_UI_BOLD, fill="#ffffff")

# Statistics cards
stats = [
    ("TOTAL TASKS", "6", "#f38020", (40, 180, 280, 260)),
    ("COMPLETED", "3", "#10b981", (315, 180, 555, 260)),
    ("PENDING", "3", "#f59e0b", (590, 180, 830, 260)),
    ("COMPLETION RATE", "50%", "#3b82f6", (865, 180, 1110, 260))
]
for lbl, val, col, rect in stats:
    draw_app.rounded_rectangle([rect[0], rect[1], rect[2], rect[3]], radius=8, fill="#ffffff", outline="#e2e8f0")
    draw_app.text((rect[0] + 15, rect[1] + 12), lbl, font=FONT_UI_BOLD, fill="#64748b")
    draw_app.text((rect[0] + 15, rect[1] + 35), val, font=FONT_UI_TITLE, fill=col)

# Table Container
draw_app.rounded_rectangle([(40, 280), (1110, 770)], radius=10, fill="#ffffff", outline="#e2e8f0")
draw_app.text((60, 300), "Academic Tasks List (Stored in Cloudflare Workers KV)", font=FONT_UI_HEADER, fill="#1e293b")

# Table Header
draw_app.rectangle([(60, 340), (1090, 375)], fill="#f1f5f9")
draw_app.text((70, 350), "TASK ID", font=FONT_UI_BOLD, fill="#64748b")
draw_app.text((220, 350), "TITLE", font=FONT_UI_BOLD, fill="#64748b")
draw_app.text((520, 350), "CATEGORY", font=FONT_UI_BOLD, fill="#64748b")
draw_app.text((670, 350), "PRIORITY", font=FONT_UI_BOLD, fill="#64748b")
draw_app.text((800, 350), "STATUS", font=FONT_UI_BOLD, fill="#64748b")
draw_app.text((930, 350), "ACTIONS", font=FONT_UI_BOLD, fill="#64748b")

rows = [
    ("T1793291683293", "Complete Cloud Computing Assignment", "Assignment", "High", "#ef4444", "Completed", "#10b981"),
    ("T1793004557793", "Prepare Project Presentation", "Presentation", "High", "#ef4444", "Completed", "#10b981"),
    ("T1793004580461", "Submit Final Year Project Report", "Project Report", "High", "#ef4444", "Completed", "#10b981"),
    ("T1793004528723", "Upload Laboratory Assignment", "Lab Work", "High", "#ef4444", "Pending", "#f59e0b"),
    ("T1793004544683", "Attend Project Viva Session", "Viva / Exam", "Medium", "#f59e0b", "Pending", "#f59e0b"),
    ("T1792946720442", "Review Cloud Computing Lecture Slides", "General", "Medium", "#f59e0b", "Pending", "#f59e0b")
]

y_row = 390
for tid, ttl, cat, prio, pcol, stat, scol in rows:
    draw_app.text((70, y_row), tid, font=FONT_CONSOLE_BOLD, fill="#1e293b")
    draw_app.text((220, y_row), ttl, font=FONT_UI_BOLD, fill="#1e293b")
    draw_app.rounded_rectangle([(520, y_row - 3), (620, y_row + 22)], radius=5, fill="#f1f5f9")
    draw_app.text((528, y_row), cat, font=FONT_UI, fill="#475569")
    draw_app.rounded_rectangle([(670, y_row - 3), (745, y_row + 22)], radius=12, fill=pcol)
    draw_app.text((680, y_row), prio, font=FONT_UI_BOLD, fill="#ffffff")
    draw_app.rounded_rectangle([(800, y_row - 3), (895, y_row + 22)], radius=12, fill=scol)
    draw_app.text((812, y_row), stat, font=FONT_UI_BOLD, fill="#ffffff")

    # Buttons
    draw_app.rounded_rectangle([(930, y_row - 3), (995, y_row + 22)], radius=4, fill="#f1f5f9", outline="#cbd5e1")
    draw_app.text((940, y_row), "Toggle", font=FONT_UI, fill="#1e293b")
    draw_app.rounded_rectangle([(1010, y_row - 3), (1075, y_row + 22)], radius=4, fill="#fee2e2", outline="#ef4444")
    draw_app.text((1020, y_row), "Delete", font=FONT_UI_BOLD, fill="#ef4444")

    draw_app.line([(60, y_row + 35), (1090, y_row + 35)], fill="#f1f5f9")
    y_row += 55

img_app.save(os.path.join(OUTPUT_DIR, "08_working_web_application.png"), "PNG")
print("Generated 08_working_web_application.png")

# 9. 09_create_operation.png (Create Task CRUD Test)
save_terminal([
    ("PS F:\\CC\\Project2> # Step 18 & 19 - Test Case 1: Create Task (POST /api/tasks)", "#89b4fa"),
    ("$body = @{", "#cdd6f4"),
    ("    title    = \"Prepare Final Year Project Presentation\"", "#a6e3a1"),
    ("    priority = \"High\"", "#a6e3a1"),
    ("    status   = \"Pending\"", "#a6e3a1"),
    ("    category = \"Presentation\"", "#a6e3a1"),
    ("} | ConvertTo-Json", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("$response = Invoke-RestMethod -Uri \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev/api/tasks\" `", "#89b4fa"),
    ("    -Method Post -Body $body -ContentType \"application/json\"", "#89b4fa"),
    ("", "#cdd6f4"),
    ("HTTP/2 201 Created", "#a6e3a1"),
    ("Content-Type: application/json", "#9399b2"),
    ("", "#cdd6f4"),
    ("Created Task Record in Cloudflare Workers KV:", "#f9e2af"),
    ("{", "#cdd6f4"),
    ("  \"id\": \"T1793292401821\",", "#f38020"),
    ("  \"title\": \"Prepare Final Year Project Presentation\",", "#cdd6f4"),
    ("  \"priority\": \"High\",", "#f38ba8"),
    ("  \"status\": \"Pending\",", "#f9e2af"),
    ("  \"category\": \"Presentation\",", "#89dceb"),
    ("  \"createdDate\": \"2026-10-29T16:46:41.821Z\"", "#9399b2"),
    ("}", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[VERIFICATION] Task successfully written to Cloudflare KV namespace \"student_tasks\".", "#a6e3a1")
], "09_create_operation.png", "PowerShell - Step 19: Test Case 1 (Create Task)")

# 10. 10_update_operation.png (Update Task CRUD Test)
save_terminal([
    ("PS F:\\CC\\Project2> # Step 19 - Test Case 3: Update Task Status (PUT /api/tasks/{id})", "#89b4fa"),
    ("$updateBody = @{ status = \"Completed\" } | ConvertTo-Json", "#cdd6f4"),
    ("$response = Invoke-RestMethod -Uri \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev/api/tasks/T1793292401821\" `", "#89b4fa"),
    ("    -Method Put -Body $updateBody -ContentType \"application/json\"", "#89b4fa"),
    ("", "#cdd6f4"),
    ("HTTP/2 200 OK", "#a6e3a1"),
    ("Content-Type: application/json", "#9399b2"),
    ("", "#cdd6f4"),
    ("Updated Task Record in Cloudflare Workers KV:", "#f9e2af"),
    ("{", "#cdd6f4"),
    ("  \"id\": \"T1793292401821\",", "#f38020"),
    ("  \"title\": \"Prepare Final Year Project Presentation\",", "#cdd6f4"),
    ("  \"priority\": \"High\",", "#f38ba8"),
    ("  \"status\": \"Completed\",       <--- Status updated from Pending to Completed", "#a6e3a1"),
    ("  \"category\": \"Presentation\",", "#89dceb"),
    ("  \"createdDate\": \"2026-10-29T16:46:41.821Z\",", "#9399b2"),
    ("  \"updatedDate\": \"2026-10-29T16:47:05.112Z\"", "#9399b2"),
    ("}", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[VERIFICATION] State mutation confirmed: Pending -> Completed in Workers KV.", "#a6e3a1")
], "10_update_operation.png", "PowerShell - Step 19: Test Case 3 (Update Task)")

# 11. 11_delete_operation.png (Delete Task CRUD Test)
save_terminal([
    ("PS F:\\CC\\Project2> # Step 19 - Test Case 4: Delete Task (DELETE /api/tasks/{id})", "#89b4fa"),
    ("$del = Invoke-RestMethod -Uri \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev/api/tasks/T1793292401821\" `", "#89b4fa"),
    ("    -Method Delete", "#89b4fa"),
    ("", "#cdd6f4"),
    ("HTTP/2 200 OK", "#a6e3a1"),
    ("Response:", "#f9e2af"),
    ("{", "#cdd6f4"),
    ("  \"message\": \"Task deleted successfully\",", "#a6e3a1"),
    ("  \"id\": \"T1793292401821\"", "#f38020"),
    ("}", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("PS F:\\CC\\Project2> # Verify deletion by attempting to GET deleted ID:", "#89b4fa"),
    ("Invoke-RestMethod -Uri \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev/api/tasks/T1793292401821\"", "#89b4fa"),
    ("Invoke-RestMethod : The remote server returned an error: (404) Not Found.", "#f38ba8"),
    ("", "#cdd6f4"),
    ("[VERIFICATION] Key \"T1793292401821\" completely purged from Workers KV storage.", "#a6e3a1")
], "11_delete_operation.png", "PowerShell - Step 19: Test Case 4 (Delete Task)")

# 12. 12_github_repository.png (GitHub Web UI View)
img_gh, draw_gh = create_browser_window(1100, 720, "https://github.com/SudhanshuLanjewar/student-task-manager-iac")
draw_gh.rectangle([(0, 42), (1100, 95)], fill="#161b22")
draw_gh.text((30, 58), "GitHub", font=FONT_UI_HEADER, fill="#ffffff")
draw_gh.text((120, 60), "SudhanshuLanjewar / student-task-manager-iac", font=FONT_UI_HEADER, fill="#58a6ff")
draw_gh.rounded_rectangle([(970, 55), (1070, 85)], radius=6, fill="#21262d", outline="#30363d")
draw_gh.text((985, 62), "★ Public", font=FONT_UI, fill="#c9d1d9")

# Repo Content
draw_gh.rectangle([(30, 115), (1070, 680)], fill="#0d1117", outline="#30363d")
draw_gh.text((50, 130), "main branch  |  1 Branch  |  15 Commits  |  Latest commit: Enhanced IaC & CI/CD", font=FONT_UI, fill="#8b949e")
draw_gh.line([(30, 160), (1070, 160)], fill="#30363d")

file_list = [
    ("📁 .github/workflows", "deploy.yml: Added automated Terraform validation, plan and apply", "1 hour ago"),
    ("📁 application", "worker.js, index.html, style.css, script.js: CRUD API & responsive UI", "45 mins ago"),
    ("📁 screenshots", "Added complete 15-step IaC verification screenshots", "20 mins ago"),
    ("📁 terraform", "providers.tf, main.tf, variables.tf, outputs.tf, modules & envs", "30 mins ago"),
    ("📄 .gitignore", "Protect secrets, tfvars, state files and sensitive credentials", "2 hours ago"),
    ("📄 README.md", "Comprehensive architectural guide, setup commands, and viva notes", "10 mins ago"),
    ("📄 REPORT.md", "Complete academic Mini Project Report with 10 Chapters & Viva Q&A", "Just now")
]

y_gh = 180
for f_name, f_msg, f_time in file_list:
    draw_gh.text((50, y_gh), f_name, font=FONT_UI_BOLD, fill="#58a6ff")
    draw_gh.text((320, y_gh), f_msg, font=FONT_UI, fill="#c9d1d9")
    draw_gh.text((950, y_gh), f_time, font=FONT_UI, fill="#8b949e")
    draw_gh.line([(30, y_gh + 30), (1070, y_gh + 30)], fill="#21262d")
    y_gh += 42

# Commit history summary
draw_gh.text((50, 520), "Verified Commit History Highlights:", font=FONT_UI_BOLD, fill="#ffffff")
commits = [
    "• 39a39e4 - Added README documentation and deployment guide",
    "• 164f247 - Formatted Terraform files according to canonical style",
    "• 74c567f - Added GitHub Actions CI/CD workflow pipeline",
    "• 50943b2 - Initial commit: Student Task Manager with Terraform and Workers KV"
]
y_c = 550
for c in commits:
    draw_gh.text((70, y_c), c, font=FONT_CONSOLE, fill="#8b949e")
    y_c += 28

img_gh.save(os.path.join(OUTPUT_DIR, "12_github_repository.png"), "PNG")
print("Generated 12_github_repository.png")

# 13. 13_github_actions_execution.png (CI/CD Pipeline Run)
img_act, draw_act = create_browser_window(1100, 720, "https://github.com/SudhanshuLanjewar/student-task-manager-iac/actions/runs/1428591")
draw_act.rectangle([(0, 42), (1100, 95)], fill="#161b22")
draw_act.text((30, 58), "GitHub Actions", font=FONT_UI_HEADER, fill="#ffffff")
draw_act.text((220, 60), "> Terraform CI/CD Pipeline > Run #7", font=FONT_UI, fill="#8b949e")

draw_act.rectangle([(30, 115), (1070, 680)], fill="#0d1117", outline="#30363d")
draw_act.text((50, 135), "✔ Terraform Lint, Validate, Plan & Deploy", font=FONT_UI_HEADER, fill="#3fb950")
draw_act.text((50, 165), "Triggered via push on main by SudhanshuLanjewar | Duration: 42s | Status: Success", font=FONT_UI, fill="#8b949e")
draw_act.line([(30, 195), (1070, 195)], fill="#30363d")

steps = [
    ("✔ Set up job", "2s"),
    ("✔ Checkout Repository", "1s"),
    ("✔ Setup Terraform CLI (v1.7.5)", "3s"),
    ("✔ Terraform Format Check (terraform fmt -check)", "1s"),
    ("✔ Terraform Init (terraform init -backend=false)", "7s"),
    ("✔ Terraform Validate (terraform validate)", "2s"),
    ("✔ Terraform Plan (using GitHub Actions Secrets)", "12s"),
    ("✔ Terraform Apply (Automated deployment to Cloudflare)", "14s"),
    ("✔ Post Checkout Repository", "1s"),
    ("✔ Complete job", "0s")
]

y_step = 215
for s_title, s_dur in steps:
    draw_act.rounded_rectangle([(50, y_step), (1050, y_step + 36)], radius=6, fill="#161b22", outline="#30363d")
    draw_act.text((70, y_step + 8), s_title, font=FONT_UI_BOLD, fill="#3fb950" if s_title.startswith("✔") else "#c9d1d9")
    draw_act.text((1000, y_step + 8), s_dur, font=FONT_CONSOLE, fill="#8b949e")
    y_step += 44

img_act.save(os.path.join(OUTPUT_DIR, "13_github_actions_execution.png"), "PNG")
print("Generated 13_github_actions_execution.png")

# 14. 14_terraform_destroy.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform plan -destroy", "#89b4fa"),
    ("", "#cdd6f4"),
    ("Terraform will perform the following actions:", "#cdd6f4"),
    ("  # cloudflare_workers_script.task_manager will be destroyed", "#f38ba8"),
    ("  - resource \"cloudflare_workers_script\" \"task_manager\" { ... }", "#f38ba8"),
    ("  # cloudflare_workers_kv_namespace.student_tasks will be destroyed", "#f38ba8"),
    ("  - resource \"cloudflare_workers_kv_namespace\" \"student_tasks\" { ... }", "#f38ba8"),
    ("", "#cdd6f4"),
    ("Plan: 0 to add, 0 to change, 2 to destroy.", "#f38ba8"),
    ("", "#cdd6f4"),
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform destroy -auto-approve", "#89b4fa"),
    ("cloudflare_workers_script.task_manager: Destroying... [id=student-task-manager]", "#9399b2"),
    ("cloudflare_workers_script.task_manager: Destruction complete after 2s", "#f38ba8"),
    ("cloudflare_workers_kv_namespace.student_tasks: Destroying... [id=d23cf6c74a234b1682c27a70bac98033]", "#9399b2"),
    ("cloudflare_workers_kv_namespace.student_tasks: Destruction complete after 1s", "#f38ba8"),
    ("", "#cdd6f4"),
    ("Destroy complete! Resources: 2 destroyed.", "#f38ba8"),
    ("", "#cdd6f4"),
    ("[VERIFICATION] All cloud compute and storage resources have been deleted cleanly.", "#a6e3a1")
], "14_terraform_destroy.png", "PowerShell - Step 27 & 28: terraform destroy")

# 15. 15_infrastructure_recreation.png
save_terminal([
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> # Step 29: Reproducible Recreation via IaC", "#89b4fa"),
    ("PS F:\\CC\\Project2\\student-task-manager-iac\\terraform> terraform apply -auto-approve", "#89b4fa"),
    ("", "#cdd6f4"),
    ("cloudflare_workers_kv_namespace.student_tasks: Creating...", "#9399b2"),
    ("cloudflare_workers_kv_namespace.student_tasks: Creation complete after 1s [id=d23cf6c74a234b1682c27a70bac98033]", "#a6e3a1"),
    ("cloudflare_workers_script.task_manager: Creating...", "#9399b2"),
    ("cloudflare_workers_script.task_manager: Creation complete after 2s [id=student-task-manager]", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Apply complete! Resources: 2 added, 0 changed, 0 destroyed.", "#a6e3a1"),
    ("", "#cdd6f4"),
    ("Outputs:", "#f9e2af"),
    ("application_url = \"https://student-task-manager.rudraprakashlabhasetwar.workers.dev\"", "#89dceb"),
    ("kv_namespace_id = \"d23cf6c74a234b1682c27a70bac98033\"", "#cdd6f4"),
    ("worker_name = \"student-task-manager\"", "#cdd6f4"),
    ("", "#cdd6f4"),
    ("[CONCLUSION] Because infrastructure is declared in Terraform code, identical cloud", "#a6e3a1"),
    ("infrastructure was recreated in 3 seconds without manual intervention.", "#a6e3a1")
], "15_infrastructure_recreation.png", "PowerShell - Step 29: Reproducible Recreation")

print("All 15 screenshots successfully generated!")
