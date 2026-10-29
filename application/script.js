// Student Task Manager - Client Logic
let allTasks = [];

document.addEventListener("DOMContentLoaded", () => {
  loadTasks();

  // Attach form submit
  const form = document.getElementById("taskForm");
  if (form) {
    form.addEventListener("submit", handleAddTask);
  }

  // Attach search and filter events
  const searchInput = document.getElementById("searchInput");
  const filterStatus = document.getElementById("filterStatus");
  const filterPriority = document.getElementById("filterPriority");
  const filterCategory = document.getElementById("filterCategory");
  const sortSelect = document.getElementById("sortSelect");

  if (searchInput) searchInput.addEventListener("input", renderTasks);
  if (filterStatus) filterStatus.addEventListener("change", renderTasks);
  if (filterPriority) filterPriority.addEventListener("change", renderTasks);
  if (filterCategory) filterCategory.addEventListener("change", renderTasks);
  if (sortSelect) sortSelect.addEventListener("change", renderTasks);
});

// Load tasks from Cloudflare Workers KV API
async function loadTasks() {
  try {
    const res = await fetch("/api/tasks");
    if (!res.ok) throw new Error("Failed to load tasks");
    allTasks = await res.json();
    renderTasks();
    updateStatistics();
  } catch (err) {
    console.error("Error loading tasks:", err);
  }
}

// Add a new task (POST /api/tasks)
async function handleAddTask(e) {
  e.preventDefault();

  const titleInput = document.getElementById("title");
  const prioritySelect = document.getElementById("priority");
  const statusSelect = document.getElementById("status");
  const categorySelect = document.getElementById("category");
  const dueDateInput = document.getElementById("dueDate");

  const title = titleInput.value.trim();
  const priority = prioritySelect ? prioritySelect.value : "Medium";
  const status = statusSelect ? statusSelect.value : "Pending";
  const category = categorySelect ? categorySelect.value : "General";
  const dueDate = dueDateInput ? dueDateInput.value : "";

  if (!title) return;

  try {
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, priority, status, category, dueDate }),
    });

    if (!res.ok) throw new Error("Error creating task");

    // Reset inputs
    titleInput.value = "";
    if (dueDateInput) dueDateInput.value = "";

    await loadTasks();
  } catch (err) {
    alert("Error adding task: " + err.message);
  }
}

// Toggle task status between Pending and Completed (PUT /api/tasks/{id})
async function toggleStatus(id, currentStatus) {
  const nextStatus = currentStatus === "Pending" ? "Completed" : "Pending";
  try {
    const res = await fetch(`/api/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: nextStatus }),
    });
    if (!res.ok) throw new Error("Failed to update status");
    await loadTasks();
  } catch (err) {
    alert("Error updating task: " + err.message);
  }
}

// Delete task (DELETE /api/tasks/{id})
async function deleteTask(id) {
  if (!confirm("Are you sure you want to delete this task?")) return;

  try {
    const res = await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete task");
    await loadTasks();
  } catch (err) {
    alert("Error deleting task: " + err.message);
  }
}

// Render filtered and sorted tasks in table
function renderTasks() {
  const tbody = document.getElementById("taskList");
  if (!tbody) return;

  const search = (document.getElementById("searchInput")?.value || "").toLowerCase();
  const filterStat = document.getElementById("filterStatus")?.value || "ALL";
  const filterPrio = document.getElementById("filterPriority")?.value || "ALL";
  const filterCat = document.getElementById("filterCategory")?.value || "ALL";
  const sortBy = document.getElementById("sortSelect")?.value || "date_desc";

  let filtered = allTasks.filter((t) => {
    const matchSearch =
      t.title.toLowerCase().includes(search) ||
      (t.id && t.id.toLowerCase().includes(search)) ||
      (t.category && t.category.toLowerCase().includes(search));

    const matchStatus = filterStat === "ALL" || t.status === filterStat;
    const matchPriority = filterPrio === "ALL" || t.priority === filterPrio;
    const matchCategory = filterCat === "ALL" || (t.category || "General") === filterCat;

    return matchSearch && matchStatus && matchPriority && matchCategory;
  });

  // Sort
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
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="empty-state">
          <div>No academic tasks found matching current filters.</div>
        </td>
      </tr>`;
    return;
  }

  filtered.forEach((task) => {
    const tr = document.createElement("tr");

    const priorityClass = `priority-${(task.priority || "Medium").toLowerCase()}`;
    const statusClass = `status-${(task.status || "Pending").toLowerCase()}`;
    const formattedDate = task.createdDate ? new Date(task.createdDate).toLocaleDateString() : "-";
    const categoryName = task.category || "General";
    const dueDateDisplay = task.dueDate || "-";

    tr.innerHTML = `
      <td><strong>${escapeHtml(task.id)}</strong></td>
      <td>${escapeHtml(task.title)}</td>
      <td><span class="category-tag">${escapeHtml(categoryName)}</span></td>
      <td><span class="badge ${priorityClass}">${escapeHtml(task.priority || "Medium")}</span></td>
      <td><span class="badge ${statusClass}">${escapeHtml(task.status || "Pending")}</span></td>
      <td>${escapeHtml(dueDateDisplay)}</td>
      <td>
        <div class="action-buttons">
          <button class="btn-sm btn-toggle" onclick="toggleStatus('${escapeHtml(task.id)}', '${escapeHtml(task.status || "Pending")}')" title="Change Status">
            ${task.status === "Completed" ? "↩ Reopen" : "✓ Complete"}
          </button>
          <button class="btn-sm btn-delete" onclick="deleteTask('${escapeHtml(task.id)}')" title="Delete Task">
            ✕ Delete
          </button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Update task statistics dashboard
function updateStatistics() {
  const total = allTasks.length;
  const completed = allTasks.filter((t) => t.status === "Completed").length;
  const pending = allTasks.filter((t) => t.status === "Pending").length;
  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const totalEl = document.getElementById("statTotal");
  const completedEl = document.getElementById("statCompleted");
  const pendingEl = document.getElementById("statPending");
  const rateEl = document.getElementById("statRate");
  const progressBar = document.getElementById("progressBar");

  if (totalEl) totalEl.textContent = total;
  if (completedEl) completedEl.textContent = completed;
  if (pendingEl) pendingEl.textContent = pending;
  if (rateEl) rateEl.textContent = `${rate}%`;
  if (progressBar) progressBar.style.width = `${rate}%`;
}

// Utility to escape HTML and prevent XSS
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
