const API_URL = process.env.NEXT_PUBLIC_API_URL;

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
  const res = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });

  const contentType = res.headers.get("content-type");

  if (!res.ok) {
    let errorMessage = `${res.status} ${res.statusText}`;
    if (contentType && contentType.includes("application/json")) {
      const errorData = await res.json();
      errorMessage = errorData.detail || JSON.stringify(errorData.detail) || errorMessage || errorData.message;
    } else {
      const errorText = await res.text(); // HTML or other text
      console.error("Non-JSON error response:", errorText);
    }
    throw new Error(errorMessage);
  }

  if (contentType && contentType.includes("application/json")) {
    return await res.json();
  } else {
    throw new Error("Expected JSON response but received something else");
  }
};


export const updateTask = async (id, task) => {
  try {
    console.log("Updating task with ID:", id, "Data:", task);
    const res = await fetch(`${API_URL}/tasks/${id}`, {
      method: "POST", // use PUT for update to follow REST conventions
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });

    const contentType = res.headers.get("content-type");

    if (!res.ok) {
      let errorBody = {};
      try {
        if (contentType && contentType.includes("application/json")) {
          errorBody = await res.json();
        } else {
          const errText = await res.text();
          console.error("Non-JSON error response:", errText);
        }
      } catch (e) {
        console.error("Error parsing response body:", e);
      }
      const errorMessage = errorBody.message || res.statusText || "Unknown error";
      const error = new Error(errorMessage);
      error.details = errorBody.detail;
      throw error;
    }

    if (contentType && contentType.includes("application/json")) {
      return await res.json();
    } else {
      throw new Error("Expected JSON response but received something else");
    }
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

