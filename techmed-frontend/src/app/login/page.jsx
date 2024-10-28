"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isSuccess, setIsSuccess] = useState(false);
    const router = useRouter();

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
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
            setTimeout(() => {
                router.push('/patient/patient-info');
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
        <div className="container mt-5 pt-5">
            <div className="row">
                <div className="col-9 col-sm-7 col-md-6 m-auto">
                    <div className="card border-0 shadow">
                        <div className="card-body">
                            <div className="text-center">
                                <img src="/logo.png" alt="User Icon" style={{ height: '5em' }} />
                            </div>
                            <h1 className="text-center mt-4 mb-4">Zaloguj się</h1>
                            <form onSubmit={handleSubmit}>
                                <fieldset>
                                    <div className="form-group">
                                        <label htmlFor="email">Adres E-mail:</label>
                                        <input
                                            className="form-control"
                                            placeholder="E-mail"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="password">Hasło:</label>
                                        <input
                                            className="form-control"
                                            placeholder="Hasło"
                                            type="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <button
                                        type="submit"
                                        className="btn btn-lg btn-block mt-3"
                                        style={{
                                            backgroundColor: '#042F43',
                                            color: '#fff',
                                            display: 'block',
                                            width: '100%',
                                        }}
                                    >
                                        Zaloguj się
                                    </button>
                                </fieldset>
                            </form>
                            {message && (
                                <p className={`text-center mt-3 ${isSuccess ? 'text-success' : 'text-danger'}`}>
                                    {message}
                                </p>
                            )}
                            <div className="text-center mt-3">
                                <p>Nie masz konta?</p>
                                <Link href="/register">
                                    <button className="btn btn-secondary">
                                        Zarejestruj się
                                    </button>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
