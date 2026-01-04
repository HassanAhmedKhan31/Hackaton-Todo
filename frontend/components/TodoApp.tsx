// Task ID: T-016 (Edit & Delete)
"use client";

import React, { useState, useEffect } from 'react';
import { getTasks, createTask, updateTask, deleteTask, Task } from '@/lib/api';
import { Trash2, CheckCircle, Circle, Plus, Edit2, X, Save } from 'lucide-react';

export default function TodoApp() {
  const [tasks, setTasks] = useState<Task[]>([]);
  
  // State for creating new tasks
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [loading, setLoading] = useState(false);

  // State for editing existing tasks
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await getTasks();
      setTasks(data.sort((a, b) => b.id - a.id));
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    setLoading(true);
    try {
      await createTask(newTitle, newDesc);
      setNewTitle('');
      setNewDesc('');
      await fetchTasks();
    } catch (error) {
      console.error("Failed to add task:", error);
    } finally {
      setLoading(false);
    }
  };

  const toggleComplete = async (task: Task) => {
    try {
      const newStatus = task.status === 'completed' ? 'pending' : 'completed';
      // Optimistic update
      setTasks(tasks.map(t => t.id === task.id ? { ...t, status: newStatus } : t));
      await updateTask(task.id, { ...task, status: newStatus });
    } catch (error) {
      console.error("Failed to update status:", error);
      fetchTasks();
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
      setTasks(tasks.filter(t => t.id !== id));
      await deleteTask(id);
    } catch (error) {
      console.error("Failed to delete task:", error);
      fetchTasks();
    }
  };

  // --- New Edit Functions ---

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDesc(task.description || '');
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle('');
    setEditDesc('');
  };

  const saveEdit = async (id: number) => {
    if (!editTitle.trim()) return;
    
    // Optimistic update
    const updatedTasks = tasks.map(t => 
      t.id === id ? { ...t, title: editTitle, description: editDesc } : t
    );
    setTasks(updatedTasks);
    setEditingId(null); // Exit edit mode immediately

    try {
      // Find the original task to preserve status
      const originalTask = tasks.find(t => t.id === id);
      if (originalTask) {
        await updateTask(id, { 
            ...originalTask, 
            title: editTitle, 
            description: editDesc 
        });
      }
    } catch (error) {
      console.error("Failed to save edit:", error);
      fetchTasks(); // Revert on error
    }
  };

  return (
    <div className="bg-white shadow-xl rounded-lg p-6 w-full">
      {/* Create Task Form */}
      <form onSubmit={handleAdd} className="mb-8 space-y-4">
        <div>
          <input
            type="text"
            placeholder="What needs to be done?"
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Description (optional)"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-black"
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50"
          >
            <Plus size={20} />
            Add
          </button>
        </div>
      </form>

      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <div
            key={task.id}
            className={`flex items-center justify-between p-4 rounded-lg border ${
              task.status === 'completed' ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-200 hover:border-blue-300'
            } transition`}
          >
            {editingId === task.id ? (
              // --- EDIT MODE ---
              <div className="flex-1 flex flex-col gap-2">
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="p-2 border border-gray-300 rounded text-black font-semibold"
                  autoFocus
                />
                <input
                  type="text"
                  value={editDesc}
                  onChange={(e) => setEditDesc(e.target.value)}
                  placeholder="Description"
                  className="p-2 border border-gray-300 rounded text-sm text-gray-600"
                />
                <div className="flex gap-2 mt-2">
                  <button 
                    onClick={() => saveEdit(task.id)}
                    className="bg-green-500 text-white px-3 py-1 rounded text-sm flex items-center gap-1 hover:bg-green-600"
                  >
                    <Save size={14} /> Save
                  </button>
                  <button 
                    onClick={cancelEditing}
                    className="bg-gray-400 text-white px-3 py-1 rounded text-sm flex items-center gap-1 hover:bg-gray-500"
                  >
                    <X size={14} /> Cancel
                  </button>
                </div>
              </div>
            ) : (
              // --- VIEW MODE ---
              <>
                <div className="flex items-center gap-4 flex-1">
                  <button
                    onClick={() => toggleComplete(task)}
                    className={`transition ${
                      task.status === 'completed' ? 'text-green-500 hover:text-green-600' : 'text-gray-300 hover:text-blue-500'
                    }`}
                  >
                    {task.status === 'completed' ? <CheckCircle size={24} /> : <Circle size={24} />}
                  </button>
                  
                  <div className={`flex-1 ${task.status === 'completed' ? 'opacity-50 line-through' : ''}`}>
                    <h3 className="font-semibold text-gray-800">{task.title}</h3>
                    {task.description && <p className="text-sm text-gray-500">{task.description}</p>}
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => startEditing(task)}
                    className="text-gray-400 hover:text-blue-500 p-2 transition"
                    aria-label="Edit task"
                  >
                    <Edit2 size={18} />
                  </button>
                  <button
                    onClick={() => handleDelete(task.id)}
                    className="text-gray-400 hover:text-red-500 p-2 transition"
                    aria-label="Delete task"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
        
        {tasks.length === 0 && (
          <p className="text-center text-gray-400 py-8">No tasks yet. Add one above!</p>
        )}
      </div>
    </div>
  );
}