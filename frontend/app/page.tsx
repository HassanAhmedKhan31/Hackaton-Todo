// Task ID: T-010, T-015
import TodoApp from '@/components/TodoApp';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gray-100 text-gray-900 flex justify-center">
      <div className="w-full max-w-3xl">
        <h1 className="text-4xl font-extrabold text-center mb-8 text-blue-900 tracking-tight">
          Hackathon Todo
        </h1>
        <TodoApp />
      </div>
      <ChatInterface />
    </main>
  );
}

// Verification:
// 1. Ensure Backend is running: uvicorn backend.main:app --reload --port 8000
// 2. Run Frontend: cd frontend && npm run dev
// 3. Open http://localhost:3000
