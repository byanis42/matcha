"use client";

import React, { useState } from "react";
import axios, { AxiosError } from "axios";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import Background from "@/components/Background";

export default function RegisterPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

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

      localStorage.setItem("token", access_token);
      setSuccess("Inscription réussie, redirection...");
      setTimeout(() => {
        router.push("/auth/login");
      }, 1500);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const axiosError = err as AxiosError<{ message: string }>;
        setError(axiosError.response?.data.message || "Erreur lors de l'inscription");
      } else {
        console.error(err);
        setError("Erreur lors de l'inscription");
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
          <h1 className="text-3xl font-bold mb-6 text-center text-neon-red">Inscription</h1>
          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}
          {success && <p className="text-green-500 mb-4 text-center">{success}</p>}

          <form onSubmit={handleRegister}>
            <div className="mb-4">
              <Label htmlFor="email" className="block text-gray-300 text-sm font-bold mb-2">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Entrez votre email"
                className="bg-gray-800 text-gray-300"
              />
            </div>

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
              <Label htmlFor="firstName" className="block text-gray-300 text-sm font-bold mb-2">
                Prénom
              </Label>
              <Input
                id="firstName"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                placeholder="Entrez votre prénom"
                className="bg-gray-800 text-gray-300"
              />
            </div>

            <div className="mb-4">
              <Label htmlFor="lastName" className="block text-gray-300 text-sm font-bold mb-2">
                Nom
              </Label>
              <Input
                id="lastName"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
                placeholder="Entrez votre nom"
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
                {loading ? "Inscription..." : "S'inscrire"}
              </Button>
            </div>
          </form>

          <p className="mt-6 text-center text-gray-300">
            Vous avez déjà un compte ?{" "}
            <Link href="/auth/login" className="text-neon-red hover:text-red-600 font-semibold">
              Connectez-vous
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
