"use client";

import React, { useState } from "react";
import axios, { AxiosError } from "axios";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import Background from "@/components/Background";

export default function LoginPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

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
      localStorage.setItem("token", access_token);
      router.push("/profile");
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const axiosError = err as AxiosError<{ message: string }>;
        setError(axiosError.response?.data.message || "Erreur de connexion");
      } else {
        console.error(err);
        setError("Erreur de connexion");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Background />
      <div className="min-h-screen flex items-center justify-center relative z-10">
        <div className="bg-black bg-opacity-75 p-8 rounded-lg shadow-lg w-full max-w-md">
          <h1 className="text-3xl font-bold mb-6 text-center text-neon-red">Connexion</h1>
          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <Label htmlFor="username" className="block text-gray-300 text-sm font-bold mb-2">
                Nom d&apos;utilisateur
              </Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Entrez votre nom d'utilisateur"
                className="bg-gray-800 text-gray-300"
              />
            </div>

            <div className="mb-4">
              <Label htmlFor="password" className="block text-gray-300 text-sm font-bold mb-2">
                Mot de passe
              </Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Entrez votre mot de passe"
                className="bg-gray-800 text-gray-300"
              />
            </div>

            <div className="flex items-center justify-between mt-6">
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Connexion..." : "Se connecter"}
              </Button>
            </div>
          </form>

          <p className="mt-6 text-center text-gray-300">
            Vous n&apos;avez pas de compte ?{" "}
            <Link href="/auth/register" className="text-neon-red hover:text-red-600 font-semibold">
              Inscrivez-vous
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
