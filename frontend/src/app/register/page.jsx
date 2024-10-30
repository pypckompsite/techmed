"use client"
import {useState} from 'react';
import {useRouter} from 'next/navigation';
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button"; // Importujemy useRouter do przekierowania

export default function RegisterForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isSuccess, setIsSuccess] = useState(false); // Nowy stan do określenia sukcesu
    const router = useRouter(); // Inicjalizacja routera

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Wysyłanie danych do endpointu FastAPI
        const res = await fetch("http://127.0.0.1:8000/auth/register/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                email,
                password,
            }).toString(),
        });

        if (res.ok) {
            setMessage('Zarejestrowano poprawnie');
            setIsSuccess(true); // Ustawia flagę sukcesu
            setEmail('');
            setPassword('');
            setTimeout(() => {
                router.push('/login'); // Przekierowanie do strony logowania po 2 sekundach
            }, 2000);
        } else {
            const errorData = await res.json();
            setMessage(errorData.detail || 'Wystąpił błąd'); // Ustawiamy komunikat błędu
            setIsSuccess(false); // Ustawia flagę błędu
        }
    };

    return (
        <section className="flex justify-center items-center min-h-screen min-w-[600px]">
            <Card className="w-full max-w-md shadow-lg">
                <CardHeader className="text-center">
                    <img src="/logo.png" alt="User Icon" className="mx-auto h-20 mb-4" />
                    <CardTitle className="text-2xl">Utwórz konto</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <Label htmlFor="email">Adres E-mail:</Label>
                            <Input
                                id="email"
                                placeholder="Wprowadź E-mail"
                                type="email"
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
                                placeholder="Wprowadź hasło"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="mt-1"
                            />
                        </div>
                        <Button type="submit" className="w-full mt-4">
                            Zarejestruj
                        </Button>
                    </form>
                    {message && (
                        <p className={`mt-3 text-center ${isSuccess ? "text-green-500" : "text-red-500"}`}>
                            {message}
                        </p>
                    )}
                </CardContent>
            </Card>
        </section>
    );
}
