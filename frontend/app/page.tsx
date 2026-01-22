"use client";

import { useState, useEffect } from 'react';
import TodoApp from '@/components/TodoApp';
import ChatInterface from '@/components/ChatInterface';
import { getTasks, Task } from '@/lib/api';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      // Fetch and sort tasks by ID descending
      const data = await getTasks();
      setTasks(data.sort((a, b) => b.id - a.id));
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks(); // Initial fetch

    // Set up polling every 5 seconds
    const intervalId = setInterval(fetchTasks, 5000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <main className="min-h-screen p-8 bg-gray-100 text-gray-900 flex justify-center">
      <div className="w-full max-w-3xl">
        <h1 className="text-4xl font-extrabold text-center mb-8 text-blue-900 tracking-tight">
          Hackathon Todo
        </h1>
        {/* Pass down setTasks to allow direct state manipulation */}
        <TodoApp 
          tasks={tasks} 
          setTasks={setTasks}
          loading={loading} 
          setLoading={setLoading}
          fetchTasks={fetchTasks} 
        />
      </div>
      <ChatInterface fetchTasks={fetchTasks} />
    </main>
  );
}
