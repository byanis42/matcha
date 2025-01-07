"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const resp = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/register`,
        {
          email,
          username,
          first_name: firstName,
          last_name: lastName,
          password,
        }
      );
      const { access_token } = resp.data;

      localStorage.setItem('token', access_token);
      setSuccess('Inscription réussie, redirection...');
      setTimeout(() => {
        router.push('/auth/login');
      }, 1500);

    } catch (err) {
      console.error(err);
      setError('Erreur lors de l’inscription');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="bg-white p-6 rounded shadow-md w-full max-w-sm"
      >
        <h1 className="text-xl font-bold mb-4">Inscription</h1>
        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-500">{success}</p>}

        <div className="mb-4">
          <label className="block font-medium">Email</label>
          <input
            type="email"
            className="border w-full px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

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
          <label className="block font-medium">Prénom</label>
          <input
            type="text"
            className="border w-full px-3 py-2"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block font-medium">Nom</label>
          <input
            type="text"
            className="border w-full px-3 py-2"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
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
          S’inscrire
        </button>
      </form>
    </div>
  );
}
