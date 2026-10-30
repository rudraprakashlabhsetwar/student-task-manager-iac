export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: cors });
    }

    // ---------- Serve Frontend ----------
    if (path === "/" || path === "/index.html" || path === "") {
      return new Response(FRONTEND_HTML, {
        headers: { 
          "Content-Type": "text/html; charset=utf-8", 
          "Cache-Control": "no-cache",
          ...cors 
        },
      });
    }

    // ---------- REST API ----------
    if (path.startsWith("/api/tasks")) {
      try {
        return await handleTasks(request, env, path, cors);
      } catch (err) {
        return json({ error: err.message }, 500, cors);
      }
    }

    return new Response("Not Found", { status: 404, headers: cors });
  },
};

async function handleTasks(request, env, path, cors) {
  const method = request.method;
  const KV = env.TASKS_KV;

  // GET /api/tasks
  if (method === "GET" && path === "/api/tasks") {
    const list = await KV.list();
    const tasks = [];
    for (const key of list.keys) {
      const val = await KV.get(key.name, "json");
      if (val) tasks.push(val);
    }
    return json(tasks, 200, cors);
  }

  // POST /api/tasks
  if (method === "POST" && path === "/api/tasks") {
    const body = await request.json();
    if (!body.title) return json({ error: "title required" }, 400, cors);

    const id = "T" + Date.now();
    const task = {
      id,
      title: body.title,
      priority: body.priority || "Medium",
      status: body.status || "Pending",
      createdDate: new Date().toISOString(),
    };
    await KV.put(id, JSON.stringify(task));
    return json(task, 201, cors);
  }

  // GET /api/tasks/{id}
  const match = path.match(/^\/api\/tasks\/([^/]+)$/);
  if (match) {
    const id = match[1];

    if (method === "GET") {
      const val = await KV.get(id, "json");
      if (!val) return json({ error: "not found" }, 404, cors);
      return json(val, 200, cors);
    }

    if (method === "PUT") {
      const existing = await KV.get(id, "json");
      if (!existing) return json({ error: "not found" }, 404, cors);
      const body = await request.json();
      const updated = { ...existing, ...body, id };
      await KV.put(id, JSON.stringify(updated));
      return json(updated, 200, cors);
    }

    if (method === "DELETE") {
      await KV.delete(id);
      return json({ deleted: id }, 200, cors);
    }
  }

  return json({ error: "unsupported" }, 405, cors);
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}

// ---------- Inlined Frontend ----------
const FRONTEND_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Task Manager</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
    h1 { color: #f38020; }
    form { display: flex; gap: .5rem; margin-bottom: 1rem; flex-wrap: wrap; }
    input, select, button { padding: .5rem; font-size: 1rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; padding: .5rem; text-align: left; }
    th { background: #f4f4f4; }
    .completed { color: green; }
    .pending { color: orange; }
    button.delete { background: #e74c3c; color: white; border: none; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Student Task Manager</h1>
  <form id="taskForm">
    <input id="title" placeholder="Task title" required />
    <select id="priority">
      <option>High</option><option selected>Medium</option><option>Low</option>
    </select>
    <select id="status">
      <option selected>Pending</option><option>Completed</option>
    </select>
    <button type="submit">Add Task</button>
  </form>
  <table>
    <thead><tr><th>ID</th><th>Title</th><th>Priority</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody id="taskList"></tbody>
  </table>
  <script>
    async function loadTasks() {
      const res = await fetch('/api/tasks');
      const tasks = await res.json();
      const tbody = document.getElementById('taskList');
      tbody.innerHTML = '';
      tasks.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = \`
          <td>\${t.id}</td>
          <td>\${t.title}</td>
          <td>\${t.priority}</td>
          <td class="\${t.status.toLowerCase()}">\${t.status}</td>
          <td>
            <button onclick="toggleStatus('\${t.id}', '\${t.status}')">Toggle</button>
            <button class="delete" onclick="deleteTask('\${t.id}')">Delete</button>
          </td>\`;
        tbody.appendChild(tr);
      });
    }

    async function toggleStatus(id, current) {
      const next = current === 'Pending' ? 'Completed' : 'Pending';
      await fetch('/api/tasks/' + id, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ status: next })
      });
      loadTasks();
    }

    async function deleteTask(id) {
      await fetch('/api/tasks/' + id, { method: 'DELETE' });
      loadTasks();
    }

    document.getElementById('taskForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const priority = document.getElementById('priority').value;
      const status = document.getElementById('status').value;
      await fetch('/api/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title, priority, status })
      });
      document.getElementById('title').value = '';
      loadTasks();
    });

    loadTasks();
  </script>
</body>
</html>`;