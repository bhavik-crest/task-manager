const API_URL = "http://127.0.0.1:8000";

export const fetchTasks = async () => {
    try {
        const res = await fetch(`${API_URL}/tasks`);
        if (!res.ok) throw new Error(`Fetch error: ${res.statusText}`);
        return await res.json();
    } catch (error) {
        console.error("fetchTasks error:", error);
        throw error; // Throw so UI can also react to the error
    }
};

export const fetchTaskById = async (id) => {
    try {
        const res = await fetch(`${API_URL}/tasks/${id}`);
        if (!res.ok) throw new Error(`Fetch error: ${res.statusText}`);
        return await res.json();
    } catch (error) {
        console.error("fetchTaskById error:", error);
        throw error;
    }
};

export const createTask = async (task) => {
    try {
        const res = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(task),
        });
        if (!res.ok) throw new Error(`Create error: ${res.statusText}`);
        return await res.json();
    } catch (error) {
        console.error("createTask error:", error);
        throw error;
    }
};

export const updateTask = async (id, task) => {
    try {
        const res = await fetch(`${API_URL}/tasks/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(task),
        });
        if (!res.ok) throw new Error(`Update error: ${res.statusText}`);
        return await res.json();
    } catch (error) {
        console.error("updateTask error:", error);
        throw error;
    }
};

export const deleteTask = async (id) => {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) {
        throw new Error('Failed to delete task');
    }
    return res.json();
};

