// src/app/page.jsx
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import Image from "next/image";

export default function HomePage() {
    return (
        <section className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
            <div className="text-center mb-12">
                <Image
                    src="/logo.png"
                    alt="Logo systemu"
                    width={300}
                    height={300}
                    className="block mx-auto" // Dodanie klas do obrazka
                />
                <p className="text-lg text-gray-700 mt-4">
                    Kompleksowy system zarządzania dokumentacją medyczną
                </p>
            </div>


            <Card className="max-w-4xl shadow-lg mb-10">
                <CardHeader className="text-center">
                    <CardTitle className="text-2xl">O Projekcie Techmed</CardTitle>
                </CardHeader>
                <CardContent className="p-6 space-y-4">
                    <p>
                        <strong>Techmed</strong> to inicjatywa zespołu pięciu studentów, mająca na celu zbudowanie
                        intuicyjnego systemu do zarządzania dokumentacją medyczną. Nasz system pomaga placówkom
                        medycznym uprościć procesy administracyjne, poprawić komunikację między pacjentami a lekarzami
                        oraz zapewnić bezpieczny dostęp do danych medycznych.
                    </p>
                    <p>
                        Dzięki Techmed, lekarze i pracownicy administracyjni mają dostęp do pełnej dokumentacji
                        medycznej pacjentów, co usprawnia diagnostykę, przepływ informacji oraz kontrolę nad
                        dokumentami.
                    </p>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl">
                <Card className="shadow-md">
                    <CardHeader className="text-center">
                        <CardTitle className="text-xl">Bezpieczny dostęp do dokumentacji</CardTitle>
                    </CardHeader>
                    <CardContent className="p-6">
                        <p>
                            Techmed zapewnia pełne bezpieczeństwo i zgodność z regulacjami ochrony danych, pozwalając
                            na bezpieczne przechowywanie i przetwarzanie dokumentów medycznych.
                        </p>
                    </CardContent>
                </Card>

                <Card className="shadow-md">
                    <CardHeader className="text-center">
                        <CardTitle className="text-xl">Wygodne zarządzanie pacjentami</CardTitle>
                    </CardHeader>
                    <CardContent className="p-6">
                        <p>
                            System ułatwia zarządzanie danymi pacjentów, umożliwiając szybki dostęp do historii
                            leczenia, zaleceń oraz wyników badań.
                        </p>
                    </CardContent>
                </Card>

                <Card className="shadow-md">
                    <CardHeader className="text-center">
                        <CardTitle className="text-xl">Wsparcie komunikacji lekarz-pacjent</CardTitle>
                    </CardHeader>
                    <CardContent className="p-6">
                        <p>
                            Techmed umożliwia łatwą komunikację między lekarzem a pacjentem, dzięki czemu każda
                            wizyta może być lepiej przygotowana, a pacjent czuje się lepiej poinformowany.
                        </p>
                    </CardContent>
                </Card>

                <Card className="shadow-md">
                    <CardHeader className="text-center">
                        <CardTitle className="text-xl">Intuicyjny interfejs</CardTitle>
                    </CardHeader>
                    <CardContent className="p-6">
                        <p>
                            Projektując Techmed, postawiliśmy na intuicyjność, aby każdy użytkownik mógł sprawnie
                            poruszać się po systemie i bez problemu odnaleźć potrzebne informacje.
                        </p>
                    </CardContent>
                </Card>
            </div>

            <div className="flex space-x-4 mt-10">
                <Link href="/login" passHref>
                    <Button>Logowanie</Button>
                </Link>
                <Link href="/register" passHref>
                    <Button>Rejestracja</Button>
                </Link>
            </div>

            <footer className="text-center text-gray-600 mt-12">
                <p>© {new Date().getFullYear()} Techmed | Projekt zespołowy pięciu studentów</p>
            </footer>
        </section>
    );
}
