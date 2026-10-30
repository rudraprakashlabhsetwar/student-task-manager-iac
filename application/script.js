async function loadTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  const tbody = document.getElementById("taskList");
  tbody.innerHTML = "";
  tasks.forEach((t) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${t.id}</td>
      <td>${t.title}</td>
      <td>${t.priority}</td>
      <td class="${t.status.toLowerCase()}">${t.status}</td>
      <td>
        <button onclick="toggleStatus('${t.id}', '${t.status}')">Toggle</button>
        <button class="delete" onclick="deleteTask('${t.id}')">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
}

async function toggleStatus(id, current) {
  const next = current === "Pending" ? "Completed" : "Pending";
  await fetch("/api/tasks/" + id, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: next }),
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch("/api/tasks/" + id, { method: "DELETE" });
  loadTasks();
}

document.getElementById("taskForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const priority = document.getElementById("priority").value;
  const status = document.getElementById("status").value;
  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, priority, status }),
  });
  document.getElementById("title").value = "";
  loadTasks();
});

loadTasks();
