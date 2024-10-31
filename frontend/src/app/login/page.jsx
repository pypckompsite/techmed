"use client";
import {useState} from 'react';
import {useRouter} from 'next/navigation';
import Link from 'next/link';
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";

export default function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isSuccess, setIsSuccess] = useState(false);
    const router = useRouter();

    const validateEmail = (email) => {//
        const re = /^[\w\-.]+@([\w-]+\.)+[\w-]{2,}$/;
        return re.test(String(email).toLowerCase());
    };

    const validatePassword = (password) => {
        return password.length >= 8; // Upewnij się, że hasło ma co najmniej 6 znaków
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Walidacja
        if (!validateEmail(email)) {
            setMessage('Proszę wprowadzić poprawny adres e-mail.');
            return;
        }
        if (!validatePassword(password)) {
            setMessage('Hasło musi mieć co najmniej 8 znaków.');
            return;
        }

        const requestBody = new URLSearchParams({
            email,
            password,
        }).toString();

        const res = await fetch("http://127.0.0.1:8000/auth/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: requestBody,
            credentials: "include",
        });

        // Oczekiwanie na odpowiedź
        if (res.ok) {
            setMessage('Zalogowano pomyślnie');
            setIsSuccess(true);
            // TODO: dodać sprawdzanie roli oraz przekierownie na odpowiedni ekran
            setTimeout(() => {
                router.push('/patient');
            }, 2000);
        } else {
            const errorData = await res.json();
            console.log('Error Data:', errorData);

            // Obsługa błędów
            if (Array.isArray(errorData.detail)) {
                setMessage(errorData.detail.map((error) => error.msg).join(', '));
            } else if (typeof errorData.detail === 'string') {
                setMessage(errorData.detail);
            } else {
                setMessage('Wystąpił błąd');
            }
            setIsSuccess(false);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen  min-w-[600px]">
            <Card className="w-full max-w-md shadow-lg">
                <CardHeader className="text-center">
                    <img src="/logo.png" alt="User Icon" className="mx-auto h-20 mb-4"/>
                    <CardTitle className="text-2xl">Zaloguj się</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <Label htmlFor="email">Adres E-mail:</Label>
                            <Input
                                id="email"
                                placeholder="E-mail"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="mt-1"
                            />
                        </div>
                        <div>
                            <Label htmlFor="password">Hasło:</Label>
                            <Input
                                id="password"
                                placeholder="Hasło"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="mt-1"
                            />
                        </div>
                        <Button type="submit" className="w-full mt-4">
                            Zaloguj się
                        </Button>
                    </form>
                    {message && (
                        <p className={`mt-3 text-center ${isSuccess ? "text-green-500" : "text-red-500"}`}>
                            {message}
                        </p>
                    )}
                    <div className="text-center mt-4">
                        <p>Nie masz konta?</p>
                        <Link href="/register">
                            <Button className="mt-2 ">
                                Zarejestruj się
                            </Button>
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
