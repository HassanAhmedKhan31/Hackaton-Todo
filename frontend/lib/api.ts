// Task ID: T-010
import axios from 'axios';

// Define Task Interface
export interface Task {
  id: number;
  title: string;
  description?: string;
  status: string;
  user_id?: string;
  is_recurring?: boolean;
  recurrence_interval?: string;
  remind_at?: string; // Assuming string for simplicity, can be Date
}

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
});

console.log('API Base URL:', api.defaults.baseURL);

// Request Interceptor
api.interceptors.request.use((config) => {
  console.log(`Starting Request: ${config.method?.toUpperCase()} ${config.url}`);
  return config;
});

// Response Interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(`Request Failed: ${error.config?.url}`, error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
    return Promise.reject(error);
  }
);

export const getTasks = async (): Promise<Task[]> => {
  const response = await api.get('/tasks/');
  return response.data;
};

export const createTask = async (title: string, description: string): Promise<Task> => {
  const response = await api.post('/tasks/', { title, description });
  return response.data;
};

export const updateTask = async (id: number, task: Partial<Task>): Promise<Task> => {
  const response = await api.put(`/tasks/${id}`, task);
  return response.data;
};

export const deleteTask = async (id: number): Promise<void> => {
  await api.delete(`/tasks/${id}`);
};
