'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { fetchTaskById, updateTask } from "../../api/tasks";


const API_URL = "http://127.0.0.1:8000";

export default function EditTaskPage() {
    const router = useRouter();
    const { id } = useParams();

    const [formData, setFormData] = useState({
        title: '',
        description: '',
        status: 'pending',
    });
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const task = await fetchTaskById(id);
                setFormData({
                    title: task.title || '',
                    description: task.description || '',
                    status: task.status || 'pending',
                });
            } catch (error) {
                setApiError(error.message);
            } finally {
                setLoading(false);
            }
        }

        if (id) fetchData();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validate = () => {
        const newErrors = {};
        if (!formData.title.trim()) newErrors.title = "Title is required";
        if (!['pending', 'done'].includes(formData.status))
            newErrors.status = "Status must be pending or done";
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setApiError('');

        if (!validate()) return;

        try {
            await updateTask(id, formData);
            router.push('/');
        } catch (error) {
            if (error.details?.errors) {
                const fieldErrors = {};
                error.details.errors.forEach(({ field, message }) => {
                    fieldErrors[field] = message;
                });
                setErrors(fieldErrors);
            } else {
                setApiError(error.message || 'Unknown error');
            }
        }
    };

    if (loading) return <p className="text-center mt-10 text-gray-600">Loading task data...</p>;

    return (
        <div className="max-w-lg mx-auto p-8 bg-white rounded-lg shadow-lg mt-12">
            <div className="flex justify-between mb-6 items-center">
                <h1 className="text-3xl font-semibold text-gray-800">Edit Task</h1>
                <button
                    onClick={() => router.back()}
                    className="text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
                    aria-label="Go back"
                >
                    ← Back
                </button>
            </div>

            {apiError && (
                <div className="bg-red-100 text-red-700 p-3 mb-4 rounded border border-red-300">
                    {apiError}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label htmlFor="title" className="block text-gray-700 font-semibold mb-1">
                        Title
                    </label>
                    <input
                        id="title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition ${errors.title ? 'border-red-500' : 'border-gray-300'
                            }`}
                        placeholder="Task title"
                    />
                    {errors.title && <p className="text-red-500 mt-1 text-sm">{errors.title}</p>}
                </div>

                <div>
                    <label htmlFor="description" className="block text-gray-700 font-semibold mb-1">
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        rows={4}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                        placeholder="Task description"
                    />
                </div>

                <div>
                    <label htmlFor="status" className="block text-gray-700 font-semibold mb-1">
                        Status
                    </label>
                    <select
                        id="status"
                        name="status"
                        value={formData.status}
                        onChange={handleChange}
                        className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition ${errors.status ? 'border-red-500' : 'border-gray-300'
                            }`}
                    >
                        <option value="pending">Pending</option>
                        <option value="done">Done</option>
                    </select>
                    {errors.status && <p className="text-red-500 mt-1 text-sm">{errors.status}</p>}
                </div>

                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                    Update Task
                </button>
            </form>
        </div>
    );
}
