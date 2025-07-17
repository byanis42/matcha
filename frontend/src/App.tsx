import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center text-primary-600 mb-8">
          Welcome to Matcha
        </h1>
        <div className="text-center">
          <p className="text-gray-600 mb-6">
            Dating website built with Clean Architecture
          </p>
          <button
            onClick={() => setCount((count) => count + 1)}
            className="bg-primary-500 hover:bg-primary-600 text-white font-bold py-2 px-4 rounded transition duration-200"
          >
            Count: {count}
          </button>
        </div>
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            Built with React 18, TypeScript, Vite, and Tailwind CSS
          </p>
        </div>
      </div>
    </div>
  )
}

export default App