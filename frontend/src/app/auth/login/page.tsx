"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const resp = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
        { username, password }
      );
      const { access_token } = resp.data;
      // Stocker le token
      localStorage.setItem('token', access_token);
      // Redirection
      router.push('/profile');
    } catch (err) {
      console.error(err);
      // pas de type any => on l'utilise => plus d'erreur "unused var"
      setError("Erreur de connexion");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded shadow-md w-full max-w-sm"
      >
        <h1 className="text-xl font-bold mb-4">Connexion</h1>
        {error && <p className="text-red-500">{error}</p>}

        <div className="mb-4">
          <label className="block font-medium">Nom d&apos;utilisateur</label>
          <input
            type="text"
            className="border w-full px-3 py-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block font-medium">Mot de passe</label>
          <input
            type="password"
            className="border w-full px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Se connecter
        </button>
      </form>
    </div>
  );
}
