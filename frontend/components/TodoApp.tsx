import React, { useState } from 'react';
import { createTask, updateTask, deleteTask, Task } from '@/lib/api';
import { motion, AnimatePresence } from 'framer-motion';
import { Trash2, CheckCircle, Circle, Plus, Edit2, X, Save, Repeat } from 'lucide-react';

interface TodoAppProps {
  tasks: Task[];
  setTasks: React.Dispatch<React.SetStateAction<Task[]>>;
  fetchTasks: () => Promise<void>;
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function TodoApp({ tasks, setTasks, fetchTasks }: TodoAppProps) {
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');
  
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      await createTask(newTitle, newDesc);
      setNewTitle('');
      setNewDesc('');
      await fetchTasks(); // Re-fetch tasks to get the latest list
    } catch (error) {
      console.error("Failed to add task:", error);
      // Optionally, show an error message to the user
    }
  };

  const toggleComplete = async (taskToToggle: Task) => {
    const newStatus = taskToToggle.status === 'completed' ? 'pending' : 'completed';

    // Optimistically update the UI
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskToToggle.id ? { ...task, status: newStatus } : task
      )
    );

    try {
      // Send the update to the server
      await updateTask(taskToToggle.id, { status: newStatus });
    } catch (error) {
      console.error("Failed to toggle task completion:", error);
      // On error, revert the change in the UI
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskToToggle.id ? { ...task, status: taskToToggle.status } : task
        )
      );
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    // Optimistically remove the task from the UI
    setTasks(tasks.filter(t => t.id !== id));
    try {
      await deleteTask(id);
    } catch (error) {
      console.error("Failed to delete task:", error);
      // If the delete fails, re-fetch to restore the task list
      await fetchTasks();
    }
  };

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDesc(task.description || '');
  };

  const cancelEditing = () => setEditingId(null);

  const saveEdit = async (id: number) => {
    if (!editTitle.trim()) return;

    const originalTask = tasks.find(t => t.id === id);
    if (!originalTask) return;

    const updatedTask = { ...originalTask, title: editTitle, description: editDesc };

    // Optimistically update the UI
    setTasks(prevTasks => prevTasks.map(t => (t.id === id ? updatedTask : t)));
    setEditingId(null);

    try {
      await updateTask(id, { title: editTitle, description: editDesc });
    } catch (error) {
      console.error("Failed to save edit:", error);
      // On error, revert the change in the UI
      setTasks(prevTasks => prevTasks.map(t => (t.id === id ? originalTask : t)));
    }
  };

  return (
    <div className="bg-white shadow-xl rounded-lg p-6 w-full">
      <form onSubmit={handleAdd} className="mb-6 space-y-4">
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
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus size={20} />
            Add
          </button>
        </div>
      </form>

      {/* Task List - This will now update instantly */}
      <div className="space-y-3">
        <AnimatePresence>
          {tasks.map((task) => (
            <motion.div
              key={task.id}
              layout
              initial={{ opacity: 0, y: -20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              {editingId === task.id ? (
                <div className="flex-1 flex flex-col gap-2">
                  <input type="text" value={editTitle} onChange={(e) => setEditTitle(e.target.value)} className="p-2 border border-gray-300 rounded text-black font-semibold" autoFocus />
                  <input type="text" value={editDesc} onChange={(e) => setEditDesc(e.target.value)} placeholder="Description" className="p-2 border border-gray-300 rounded text-sm text-gray-600" />
                  <div className="flex gap-2 mt-2">
                    <button onClick={() => saveEdit(task.id)} className="bg-green-500 text-white px-3 py-1 rounded text-sm flex items-center gap-1 hover:bg-green-600"><Save size={14} /> Save</button>
                    <button onClick={cancelEditing} className="bg-gray-400 text-white px-3 py-1 rounded text-sm flex items-center gap-1 hover:bg-gray-500"><X size={14} /> Cancel</button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between p-4 rounded-lg border bg-white border-gray-200 hover:border-blue-300 transition">
                    <div className="flex items-center gap-4 flex-1">
                      <button onClick={() => toggleComplete(task)} className={`transition ${task.status === 'completed' ? 'text-green-500 hover:text-green-600' : 'text-gray-300 hover:text-blue-500'}`}>
                        {task.status === 'completed' ? <CheckCircle size={24} /> : <Circle size={24} />}
                      </button>
                      <div className={`flex-1 ${task.status === 'completed' ? 'opacity-50 line-through' : ''}`}>
                        <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                          {task.title}
                          {task.is_recurring && <Repeat size={14} className="text-blue-500" />}
                        </h3>
                        {task.description && <p className="text-sm text-gray-500">{task.description}</p>}
                        {(task.description === "AI is thinking..." || task.description === "AI processing...") && (
                          <div className="text-xs text-yellow-600 bg-yellow-100 border border-yellow-200 rounded-full px-2 py-0.5 inline-block mt-1">
                            Status: Processing...
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button onClick={() => startEditing(task)} className="text-gray-400 hover:text-blue-500 p-2 transition" aria-label="Edit task"><Edit2 size={18} /></button>
                      <button onClick={() => handleDelete(task.id)} className="text-gray-400 hover:text-red-500 p-2 transition" aria-label="Delete task"><Trash2 size={18} /></button>
                    </div>
                  </div>
                </>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        {tasks.length === 0 && (
          <p className="text-center text-gray-400 py-8">All caught up! Add a task to get started</p>
        )}
      </div>
    </div>
  );
}