'use client';

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchTasks, deleteTask } from "../api/tasks";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const loadTasks = () => {
    setLoading(true);
    fetchTasks()
      .then((data) => {
        setTasks(data);
        setLoading(false);
      })
      .catch(console.error);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleEdit = (taskId) => {
    router.push(`/tasks/${taskId}`);
  };

  const handleDelete = async (taskId) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await deleteTask(taskId);
      loadTasks();
    } catch (error) {
      alert("Failed to delete task");
      console.error(error);
    }
  };

  if (loading) return <p className="text-center mt-10">Loading tasks...</p>;

  return (
    <div className="max-w-4xl bg-white mx-auto mt-12 p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-semibold">Tasks</h2>
        <button
          onClick={() => router.push('/tasks/new')}
          className="bg-blue-600 text-white px-5 py-2 rounded shadow hover:bg-blue-700 transition"
        >
          + Add Task
        </button>
      </div>

      <ul>
        {tasks.map((task) => (
          <li
            key={task.id}
            className="bg-white p-5 rounded-lg shadow mb-4 flex justify-between items-center"
          >
            <div>
              <h3 className="text-xl font-bold">{task.title}</h3>
              <p className="text-gray-600">{task.description}</p>
              <span
                className={`inline-block rounded px-3 py-1 mt-2 text-sm font-medium ${task.status === 'pending' ? "bg-yellow-300 text-yellow-900" : "bg-green-300 text-green-900"
                  }`}
              >
                {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
              </span>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={() => handleEdit(task.id)}
                aria-label={`Edit task ${task.title}`}
                className="text-blue-600 hover:text-blue-800 text-2xl cursor-pointer"
              >
                ✏️
              </button>
              <button
                onClick={() => handleDelete(task.id)}
                aria-label={`Delete task ${task.title}`}
                className="text-red-600 hover:text-red-800 text-2xl"
              >
                🗑️
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
