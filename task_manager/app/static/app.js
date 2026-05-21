// Interactive Client-Side SPA Controller

document.addEventListener("DOMContentLoaded", () => {
    // DOM Element selections
    const taskForm = document.getElementById("task-form");
    const taskTitleInput = document.getElementById("task-title");
    const taskDescInput = document.getElementById("task-desc");
    const tasksContainer = document.getElementById("tasks-container");
    const taskCountBadge = document.getElementById("task-count");
    const loadingState = document.getElementById("loading-state");
    const emptyState = document.getElementById("empty-state");
    const submitBtn = document.getElementById("submit-btn");

    // Fetch and display active tasks on load
    fetchTasks();

    // Event: Create new task
    taskForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const title = taskTitleInput.value.trim();
        const description = taskDescInput.value.trim();

        if (!title) return;

        // Disable button during submission
        submitBtn.disabled = true;
        submitBtn.querySelector(".btn-text").textContent = "Creating...";

        try {
            const response = await fetch("/api/tasks", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                json: true,
                body: JSON.stringify({ title, description: description || null })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to create task");
            }

            const newTask = await response.json();
            
            // Clear inputs
            taskTitleInput.value = "";
            taskDescInput.value = "";
            
            showToast(`Task "${newTask.title}" created successfully!`, "success");
            await fetchTasks(); // Refresh list

        } catch (error) {
            console.error("Error creating task:", error);
            showToast(error.message, "error");
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector(".btn-text").textContent = "Create Task";
        }
    });

    // Fetch All Tasks from API
    async function fetchTasks() {
        try {
            loadingState.classList.remove("hidden");
            emptyState.classList.add("hidden");

            // Clear any previously loaded task item elements
            const existingItems = tasksContainer.querySelectorAll(".task-item");
            existingItems.forEach(item => item.remove());

            const response = await fetch("/api/tasks");
            if (!response.ok) throw new Error("Failed to fetch task list");

            const tasks = await response.json();
            
            loadingState.classList.add("hidden");
            
            // Update badge
            taskCountBadge.textContent = `${tasks.length} ${tasks.length === 1 ? 'Task' : 'Tasks'}`;

            if (tasks.length === 0) {
                emptyState.classList.remove("hidden");
                return;
            }

            // Inject task elements
            tasks.forEach(task => {
                const taskElement = createTaskElement(task);
                tasksContainer.appendChild(taskElement);
            });

        } catch (error) {
            console.error("Error loading tasks:", error);
            loadingState.classList.add("hidden");
            showToast("Failed to connect to the backend server.", "error");
        }
    }

    // Helper: Create individual Task DOM Element
    function createTaskElement(task) {
        const itemDiv = document.createElement("div");
        itemDiv.className = `task-item ${task.is_completed ? 'completed' : ''}`;
        itemDiv.dataset.id = task.id;

        // Parse human-readable UTC timestamp
        const dateObj = new Date(task.created_at);
        const formattedDate = dateObj.toLocaleDateString(undefined, { 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        itemDiv.innerHTML = `
            <div class="task-checkbox-wrapper">
                <div class="custom-checkbox" title="Toggle completion">
                    <i class="fa-solid fa-check"></i>
                </div>
            </div>
            <div class="task-content">
                <span class="task-title-text">${escapeHTML(task.title)}</span>
                ${task.description ? `<p class="task-desc-text">${escapeHTML(task.description)}</p>` : ''}
                <span class="task-time-text">
                    <i class="fa-regular fa-clock"></i> Created ${formattedDate}
                </span>
            </div>
            <div class="task-actions">
                <button class="action-btn action-btn-danger delete-btn" title="Delete Task">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </div>
        `;

        // Event: Toggle task completion status
        const checkbox = itemDiv.querySelector(".custom-checkbox");
        checkbox.addEventListener("click", async () => {
            const newStatus = !itemDiv.classList.contains("completed");
            try {
                const response = await fetch(`/api/tasks/${task.id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ is_completed: newStatus })
                });

                if (!response.ok) throw new Error("Could not update task status");
                
                const updatedTask = await response.json();
                
                if (updatedTask.is_completed) {
                    itemDiv.classList.add("completed");
                    showToast("Task completed!", "success");
                } else {
                    itemDiv.classList.remove("completed");
                    showToast("Task reopened.", "success");
                }
            } catch (error) {
                console.error("Error updating status:", error);
                showToast("Failed to update task.", "error");
            }
        });

        // Event: Delete task
        const deleteBtn = itemDiv.querySelector(".delete-btn");
        deleteBtn.addEventListener("click", async () => {
            if (!confirm(`Are you sure you want to delete task "${task.title}"?`)) return;

            try {
                const response = await fetch(`/api/tasks/${task.id}`, {
                    method: "DELETE"
                });

                if (!response.ok) throw new Error("Failed to delete task");

                itemDiv.style.animation = "slideIn 0.2s ease-in reverse forwards";
                setTimeout(() => {
                    itemDiv.remove();
                    fetchTasks(); // Reload count/state
                    showToast("Task deleted.", "success");
                }, 200);

            } catch (error) {
                console.error("Error deleting task:", error);
                showToast("Failed to delete task.", "error");
            }
        });

        return itemDiv;
    }

    // Helper: Escapes string to avoid XSS injections
    function escapeHTML(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Dynamic Premium Toast System
    function showToast(message, type = "success") {
        const container = document.getElementById("toast-container");
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        
        const icon = type === "success" 
            ? "fa-solid fa-circle-check" 
            : "fa-solid fa-circle-exclamation";

        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);

        // Remove toast automatically after 4.5 seconds
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(10px)";
            toast.style.transition = "all 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 4500);
    }
});
