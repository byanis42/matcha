"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import Input from '@/components/Input';
import Button from '@/components/Button';
import Link from 'next/link';
import Background from '@/components/Background';

export default function RegisterPage() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation améliorée
    if (!email || !username || !firstName || !lastName || !password) {
      setError("Veuillez remplir tous les champs");
      return;
    }

    setLoading(true);

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
    } catch (err: unknown) {
      console.error(err);
      setError('Erreur lors de l’inscription');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Background />
      <div className="min-h-screen flex items-center justify-center relative z-10">
        <div className="bg-black bg-opacity-75 p-8 rounded-lg shadow-lg w-full max-w-md transform transition-transform duration-500 hover:scale-105">
          <h1 className="text-3xl font-bold mb-6 text-center text-neon-red">Inscription</h1>
          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}
          {success && <p className="text-green-500 mb-4 text-center">{success}</p>}

          <form onSubmit={handleRegister}>
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <Input
              label="Nom d'utilisateur"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <Input
              label="Prénom"
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />

            <Input
              label="Nom"
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
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
                {loading ? "Inscription..." : "S’inscrire"}
              </Button>
            </div>
          </form>

          <p className="mt-6 text-center text-gray-300">
            Vous avez déjà un compte ?{' '}
            <Link href="/auth/login">
              <a className="text-neon-red hover:text-red-600 font-semibold">Connectez-vous</a>
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
