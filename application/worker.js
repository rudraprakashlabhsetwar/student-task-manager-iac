export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers for cross-origin API calls
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: cors });
    }

    // Serve Frontend Assets
    if (path === "/" || path === "/index.html") {
      return new Response(FRONTEND_HTML, {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "no-cache",
          ...cors,
        },
      });
    }

    if (path === "/style.css") {
      return new Response(FRONTEND_CSS, {
        headers: { "Content-Type": "text/css; charset=utf-8", ...cors },
      });
    }

    if (path === "/script.js") {
      return new Response(FRONTEND_JS, {
        headers: { "Content-Type": "application/javascript; charset=utf-8", ...cors },
      });
    }

    // REST API Routes
    if (path.startsWith("/api/tasks")) {
      try {
        return await handleTasks(request, env, path, cors);
      } catch (err) {
        return json({ error: err.message }, 500, cors);
      }
    }

    if (path === "/api/stats") {
      try {
        return await handleStats(env, cors);
      } catch (err) {
        return json({ error: err.message }, 500, cors);
      }
    }

    return new Response("Not Found", { status: 404, headers: cors });
  },
};

// Handle CRUD operations on Cloudflare Workers KV
async function handleTasks(request, env, path, cors) {
  const method = request.method;
  const KV = env.TASKS_KV;

  // GET /api/tasks (FR2: View Tasks)
  if (method === "GET" && path === "/api/tasks") {
    const list = await KV.list();
    const tasks = [];
    for (const key of list.keys) {
      const val = await KV.get(key.name, "json");
      if (val) tasks.push(val);
    }
    // Sort default newest first
    tasks.sort((a, b) => new Date(b.createdDate || 0) - new Date(a.createdDate || 0));
    return json(tasks, 200, cors);
  }

  // POST /api/tasks (FR1: Add Task)
  if (method === "POST" && path === "/api/tasks") {
    const body = await request.json();
    if (!body.title) {
      return json({ error: "Task title is required" }, 400, cors);
    }

    const id = "T" + Date.now();
    const task = {
      id,
      title: body.title,
      priority: body.priority || "Medium",
      status: body.status || "Pending",
      category: body.category || "General",
      dueDate: body.dueDate || "",
      createdDate: new Date().toISOString(),
    };

    await KV.put(id, JSON.stringify(task));
    return json(task, 201, cors);
  }

  // Routes for /api/tasks/{id}
  const match = path.match(/^\/api\/tasks\/([^/]+)$/);
  if (match) {
    const id = match[1];

    // GET /api/tasks/{id} (FR2: Get individual task)
    if (method === "GET") {
      const val = await KV.get(id, "json");
      if (!val) return json({ error: "Task not found" }, 404, cors);
      return json(val, 200, cors);
    }

    // PUT /api/tasks/{id} (FR3: Update Task)
    if (method === "PUT") {
      const existing = await KV.get(id, "json");
      if (!existing) return json({ error: "Task not found" }, 404, cors);

      const body = await request.json();
      const updated = {
        ...existing,
        ...body,
        id, // preserve immutable ID
        updatedDate: new Date().toISOString(),
      };

      await KV.put(id, JSON.stringify(updated));
      return json(updated, 200, cors);
    }

    // DELETE /api/tasks/{id} (FR4: Delete Task)
    if (method === "DELETE") {
      const existing = await KV.get(id, "json");
      if (!existing) return json({ error: "Task not found" }, 404, cors);

      await KV.delete(id);
      return json({ message: "Task deleted successfully", id }, 200, cors);
    }
  }

  return json({ error: "Method not allowed" }, 405, cors);
}

// Compute task completion statistics
async function handleStats(env, cors) {
  const KV = env.TASKS_KV;
  const list = await KV.list();
  let total = 0;
  let completed = 0;
  let pending = 0;

  for (const key of list.keys) {
    const val = await KV.get(key.name, "json");
    if (val) {
      total++;
      if (val.status === "Completed") completed++;
      else pending++;
    }
  }

  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;
  return json({ total, completed, pending, rate }, 200, cors);
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj, null, 2), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}

// Inline CSS for instant sub-second edge rendering
const FRONTEND_CSS = `:root {
  --primary: #f38020;
  --primary-hover: #d96f14;
  --primary-light: #fff3e8;
  --bg-main: #f8fafc;
  --bg-card: #ffffff;
  --text-main: #1e293b;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --success: #10b981;
  --success-light: #ecfdf5;
  --warning: #f59e0b;
  --warning-light: #fffbeb;
  --danger: #ef4444;
  --danger-light: #fef2f2;
  --info: #3b82f6;
  --info-light: #eff6ff;
  --radius: 10px;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: var(--bg-main); color: var(--text-main); line-height: 1.5; padding: 1.5rem 1rem; }
.container { max-width: 1050px; margin: 0 auto; }
header { background: linear-gradient(135deg, #f38020 0%, #fa541c 100%); color: #ffffff; padding: 2rem; border-radius: var(--radius); margin-bottom: 2rem; box-shadow: var(--shadow-lg); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.header-title h1 { font-size: 1.85rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; }
.header-title p { opacity: 0.9; font-size: 0.95rem; margin-top: 0.25rem; }
.badge-iac { background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(4px); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: var(--bg-card); padding: 1.25rem; border-radius: var(--radius); box-shadow: var(--shadow); border: 1px solid var(--border-color); display: flex; flex-direction: column; }
.stat-label { font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
.stat-value { font-size: 2rem; font-weight: 700; margin: 0.25rem 0; color: var(--text-main); }
.stat-card.total .stat-value { color: var(--primary); }
.stat-card.completed .stat-value { color: var(--success); }
.stat-card.pending .stat-value { color: var(--warning); }
.stat-card.rate .stat-value { color: var(--info); }
.progress-bar-bg { width: 100%; height: 6px; background-color: var(--border-color); border-radius: 3px; overflow: hidden; margin-top: 0.5rem; }
.progress-bar-fill { height: 100%; background: linear-gradient(90deg, var(--primary) 0%, var(--success) 100%); width: 0%; transition: width 0.4s ease; }
.card { background: var(--bg-card); border-radius: var(--radius); box-shadow: var(--shadow); border: 1px solid var(--border-color); padding: 1.5rem; margin-bottom: 2rem; }
.card-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; }
.task-form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group.full-width { grid-column: 1 / -1; }
label { font-size: 0.85rem; font-weight: 600; color: var(--text-main); }
input, select { padding: 0.65rem 0.85rem; font-size: 0.95rem; border: 1px solid var(--border-color); border-radius: 6px; background-color: #ffffff; color: var(--text-main); transition: border-color 0.2s, box-shadow 0.2s; font-family: inherit; }
input:focus, select:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(243, 128, 32, 0.15); }
button.btn-primary { background-color: var(--primary); color: #ffffff; padding: 0.75rem 1.5rem; font-size: 0.95rem; font-weight: 600; border: none; border-radius: 6px; cursor: pointer; transition: background-color 0.2s, transform 0.1s; display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; }
button.btn-primary:hover { background-color: var(--primary-hover); }
button.btn-primary:active { transform: translateY(1px); }
.controls-bar { display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; background: var(--bg-card); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border-color); }
.search-box { flex: 1; min-width: 250px; }
.filter-group { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.table-responsive { overflow-x: auto; border-radius: var(--radius); border: 1px solid var(--border-color); background: var(--bg-card); }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
thead th { background-color: #f1f5f9; padding: 0.85rem 1rem; font-weight: 600; color: var(--text-muted); border-bottom: 1px solid var(--border-color); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; }
tbody tr { border-bottom: 1px solid var(--border-color); transition: background-color 0.15s; }
tbody tr:hover { background-color: #f8fafc; }
tbody td { padding: 0.95rem 1rem; vertical-align: middle; }
.badge { display: inline-block; padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-align: center; }
.priority-high { background-color: var(--danger-light); color: var(--danger); }
.priority-medium { background-color: var(--warning-light); color: var(--warning); }
.priority-low { background-color: var(--info-light); color: var(--info); }
.status-completed { background-color: var(--success-light); color: var(--success); }
.status-pending { background-color: var(--warning-light); color: var(--warning); }
.category-tag { background-color: #f1f5f9; color: var(--text-muted); font-size: 0.8rem; padding: 0.2rem 0.5rem; border-radius: 4px; }
.action-buttons { display: flex; gap: 0.4rem; }
.btn-sm { padding: 0.35rem 0.65rem; font-size: 0.8rem; border-radius: 4px; border: 1px solid var(--border-color); background: #ffffff; cursor: pointer; transition: all 0.2s; font-weight: 500; }
.btn-toggle:hover { background-color: #f1f5f9; border-color: #cbd5e1; }
.btn-delete { color: var(--danger); border-color: rgba(239, 68, 68, 0.3); }
.btn-delete:hover { background-color: var(--danger-light); border-color: var(--danger); }
.empty-state { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
footer { text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); color: var(--text-muted); font-size: 0.85rem; }
@media (max-width: 768px) { header { flex-direction: column; align-items: flex-start; } .controls-bar { flex-direction: column; align-items: stretch; } .filter-group { flex-direction: column; } }`;

// Inline JS for instant browser loading
const FRONTEND_JS = `let allTasks = [];
document.addEventListener("DOMContentLoaded", () => {
  loadTasks();
  const form = document.getElementById("taskForm");
  if (form) form.addEventListener("submit", handleAddTask);
  ["searchInput", "filterStatus", "filterPriority", "filterCategory", "sortSelect"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener(id === "searchInput" ? "input" : "change", renderTasks);
  });
});

async function loadTasks() {
  try {
    const res = await fetch("/api/tasks");
    if (!res.ok) throw new Error("Failed to load tasks");
    allTasks = await res.json();
    renderTasks();
    updateStatistics();
  } catch (err) {
    console.error("Error:", err);
  }
}

async function handleAddTask(e) {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const priority = document.getElementById("priority").value;
  const status = document.getElementById("status").value;
  const category = document.getElementById("category").value;
  const dueDate = document.getElementById("dueDate").value;
  if (!title) return;

  try {
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, priority, status, category, dueDate })
    });
    if (!res.ok) throw new Error("Creation failed");
    document.getElementById("title").value = "";
    document.getElementById("dueDate").value = "";
    await loadTasks();
  } catch (err) {
    alert("Error: " + err.message);
  }
}

async function toggleStatus(id, currentStatus) {
  const nextStatus = currentStatus === "Pending" ? "Completed" : "Pending";
  try {
    await fetch("/api/tasks/" + id, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: nextStatus })
    });
    await loadTasks();
  } catch (err) {
    alert("Error: " + err.message);
  }
}

async function deleteTask(id) {
  if (!confirm("Are you sure you want to delete this task?")) return;
  try {
    await fetch("/api/tasks/" + id, { method: "DELETE" });
    await loadTasks();
  } catch (err) {
    alert("Error: " + err.message);
  }
}

function renderTasks() {
  const tbody = document.getElementById("taskList");
  if (!tbody) return;
  const search = (document.getElementById("searchInput")?.value || "").toLowerCase();
  const filterStat = document.getElementById("filterStatus")?.value || "ALL";
  const filterPrio = document.getElementById("filterPriority")?.value || "ALL";
  const filterCat = document.getElementById("filterCategory")?.value || "ALL";
  const sortBy = document.getElementById("sortSelect")?.value || "date_desc";

  let filtered = allTasks.filter(t => {
    const matchSearch = t.title.toLowerCase().includes(search) || (t.id && t.id.toLowerCase().includes(search)) || (t.category && t.category.toLowerCase().includes(search));
    const matchStat = filterStat === "ALL" || t.status === filterStat;
    const matchPrio = filterPrio === "ALL" || t.priority === filterPrio;
    const matchCat = filterCat === "ALL" || (t.category || "General") === filterCat;
    return matchSearch && matchStat && matchPrio && matchCat;
  });

  filtered.sort((a, b) => {
    if (sortBy === "priority") {
      const weight = { High: 3, Medium: 2, Low: 1 };
      return (weight[b.priority] || 0) - (weight[a.priority] || 0);
    }
    if (sortBy === "title") return a.title.localeCompare(b.title);
    if (sortBy === "date_asc") return new Date(a.createdDate || 0) - new Date(b.createdDate || 0);
    return new Date(b.createdDate || 0) - new Date(a.createdDate || 0);
  });

  tbody.innerHTML = "";
  if (filtered.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No academic tasks found.</td></tr>';
    return;
  }

  filtered.forEach(t => {
    const tr = document.createElement("tr");
    tr.innerHTML = \`
      <td><strong>\${escapeHtml(t.id)}</strong></td>
      <td>\${escapeHtml(t.title)}</td>
      <td><span class="category-tag">\${escapeHtml(t.category || "General")}</span></td>
      <td><span class="badge priority-\${(t.priority || "Medium").toLowerCase()}">\${escapeHtml(t.priority || "Medium")}</span></td>
      <td><span class="badge status-\${(t.status || "Pending").toLowerCase()}">\${escapeHtml(t.status || "Pending")}</span></td>
      <td>\${escapeHtml(t.dueDate || "-")}</td>
      <td>
        <div class="action-buttons">
          <button class="btn-sm btn-toggle" onclick="toggleStatus('\${escapeHtml(t.id)}', '\${escapeHtml(t.status || "Pending")}')">
            \${t.status === "Completed" ? "↩ Reopen" : "✓ Complete"}
          </button>
          <button class="btn-sm btn-delete" onclick="deleteTask('\${escapeHtml(t.id)}')">✕ Delete</button>
        </div>
      </td>\`;
    tbody.appendChild(tr);
  });
}

function updateStatistics() {
  const total = allTasks.length;
  const completed = allTasks.filter(t => t.status === "Completed").length;
  const pending = allTasks.filter(t => t.status === "Pending").length;
  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

  document.getElementById("statTotal").textContent = total;
  document.getElementById("statCompleted").textContent = completed;
  document.getElementById("statPending").textContent = pending;
  document.getElementById("statRate").textContent = rate + "%";
  document.getElementById("progressBar").style.width = rate + "%";
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}`;

// Self-contained full HTML page served on root /
const FRONTEND_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Task Manager - Cloudflare Workers & Terraform</title>
  <style>\${FRONTEND_CSS}</style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-title">
        <h1>🎓 Student Task Manager</h1>
        <p>Serverless Academic Task Management powered by Cloudflare Workers & Workers KV</p>
      </div>
      <div class="badge-iac">⚡ Provisioned via Terraform IaC</div>
    </header>

    <div class="stats-grid">
      <div class="stat-card total">
        <span class="stat-label">Total Tasks</span>
        <span class="stat-value" id="statTotal">0</span>
      </div>
      <div class="stat-card completed">
        <span class="stat-label">Completed</span>
        <span class="stat-value" id="statCompleted">0</span>
      </div>
      <div class="stat-card pending">
        <span class="stat-label">Pending</span>
        <span class="stat-value" id="statPending">0</span>
      </div>
      <div class="stat-card rate">
        <span class="stat-label">Completion Rate</span>
        <span class="stat-value" id="statRate">0%</span>
        <div class="progress-bar-bg"><div class="progress-bar-fill" id="progressBar"></div></div>
      </div>
    </div>

    <div class="card">
      <h2 class="card-title">➕ Add Academic Task</h2>
      <form id="taskForm">
        <div class="task-form-grid">
          <div class="form-group full-width">
            <label for="title">Task Title *</label>
            <input type="text" id="title" placeholder="e.g., Complete Cloud Computing Assignment" required>
          </div>
          <div class="form-group">
            <label for="category">Category</label>
            <select id="category">
              <option value="Assignment" selected>Assignment</option>
              <option value="Presentation">Presentation</option>
              <option value="Project Report">Project Report</option>
              <option value="Lab Work">Lab Work</option>
              <option value="Viva / Exam">Viva / Exam</option>
              <option value="General">General</option>
            </select>
          </div>
          <div class="form-group">
            <label for="priority">Priority</label>
            <select id="priority">
              <option value="High">High Priority</option>
              <option value="Medium" selected>Medium Priority</option>
              <option value="Low">Low Priority</option>
            </select>
          </div>
          <div class="form-group">
            <label for="status">Initial Status</label>
            <select id="status">
              <option value="Pending" selected>Pending</option>
              <option value="Completed">Completed</option>
            </select>
          </div>
          <div class="form-group">
            <label for="dueDate">Due Date</label>
            <input type="date" id="dueDate">
          </div>
        </div>
        <button type="submit" class="btn-primary">Add Task to Cloudflare KV</button>
      </form>
    </div>

    <div class="controls-bar">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="🔍 Search tasks by title, ID, category...">
      </div>
      <div class="filter-group">
        <select id="filterStatus">
          <option value="ALL">All Statuses</option>
          <option value="Pending">Pending</option>
          <option value="Completed">Completed</option>
        </select>
        <select id="filterPriority">
          <option value="ALL">All Priorities</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
        <select id="filterCategory">
          <option value="ALL">All Categories</option>
          <option value="Assignment">Assignment</option>
          <option value="Presentation">Presentation</option>
          <option value="Project Report">Project Report</option>
          <option value="Lab Work">Lab Work</option>
          <option value="Viva / Exam">Viva / Exam</option>
          <option value="General">General</option>
        </select>
        <select id="sortSelect">
          <option value="date_desc">Newest First</option>
          <option value="date_asc">Oldest First</option>
          <option value="priority">Priority (High to Low)</option>
          <option value="title">Title (A-Z)</option>
        </select>
      </div>
    </div>

    <div class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>Task ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Due Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="taskList"></tbody>
      </table>
    </div>

    <footer>
      <p>Student Task Management Application | Deployed with Terraform to Cloudflare Workers & KV</p>
      <p>Infrastructure as Code (IaC) Mini Project</p>
    </footer>
  </div>

  <script>\${FRONTEND_JS}</script>
</body>
</html>`;
