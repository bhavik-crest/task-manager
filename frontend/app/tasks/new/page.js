'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createTask } from "../../api/tasks";

const API_URL = "http://127.0.0.1:8000";

export default function AddTaskPage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    status: "pending",
  });

  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title.trim()) newErrors.title = "Title is required.";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError("");

    if (!validateForm()) return;

    try {
      await createTask(formData);
      router.push("/");
    } catch (error) {
      if (error.details?.errors) {
        // API validation errors
        const apiErrors = {};
        error.details.errors.forEach(({ field, message }) => {
          apiErrors[field] = message;
        });
        setErrors(apiErrors);
      } else {
        setApiError(error.message || "Unknown error occurred.");
      }
    }
  };

  return (
    <div className="max-w-lg mx-auto p-8 bg-white rounded-lg shadow-lg mt-16">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-semibold text-gray-800">Add New Task</h1>
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
          aria-label="Go back"
        >
          ← Back
        </button>
      </div>

      {apiError && (
        <div className="bg-red-100 text-red-700 p-3 mb-6 rounded border border-red-300">
          {apiError}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">

        <div>
          <label htmlFor="title" className="block mb-2 font-semibold text-gray-700">
            Title
          </label>
          <input
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Task title"
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition ${errors.title ? 'border-red-500' : 'border-gray-300'
              }`}
          />
          {errors.title && <p className="text-red-500 mt-1 text-sm">{errors.title}</p>}
        </div>

        <div>
          <label htmlFor="description" className="block mb-2 font-semibold text-gray-700">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Task description"
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
        </div>

        <div>
          <label htmlFor="status" className="block mb-2 font-semibold text-gray-700">
            Status
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition border-gray-300"
          >
            <option value="pending">Pending</option>
            <option value="done">Done</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Create Task
        </button>
      </form>
    </div>
  );
}
