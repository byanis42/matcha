"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import Input from '@/components/Input';
import Button from '@/components/Button';
import Link from 'next/link';
import Background from '@/components/Background';

export default function LoginPage() {
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation améliorée
    if (!username || !password) {
      setError("Veuillez remplir tous les champs");
      return;
    }

    setLoading(true);

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
    } catch (err: unknown) {
      console.error(err);
      setError("Erreur de connexion");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Background />
      <div className="min-h-screen flex items-center justify-center relative z-10">
        <div className="bg-black bg-opacity-75 p-8 rounded-lg shadow-lg w-full max-w-md transform transition-transform duration-500 hover:scale-105">
          <h1 className="text-3xl font-bold mb-6 text-center text-neon-red">Connexion</h1>
          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

          <form onSubmit={handleLogin}>
            <Input
              label="Nom d'utilisateur"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <Input
              label="Mot de passe"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <div className="flex items-center justify-between mt-6">
              <Button type="submit" className="w-full bg-neon-red hover:bg-red-600">
                {loading ? "Connexion..." : "Se connecter"}
              </Button>
            </div>
          </form>

          <p className="mt-6 text-center text-gray-300">
            Vous n&rsquo;avez pas de compte ?{' '}
            <Link href="/auth/register">
              <a className="text-neon-red hover:text-red-600 font-semibold">Inscrivez-vous</a>
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
