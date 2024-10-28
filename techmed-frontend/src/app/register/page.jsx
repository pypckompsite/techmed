"use client"
import {useState} from 'react';
import {useRouter} from 'next/navigation'; // Importujemy useRouter do przekierowania
import 'bootstrap/dist/css/bootstrap.min.css';

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
        <section className="w-100">
            <div className="container mt-5 pt-5">
                <div className="row">
                    <div className="col-9 col-sm-7 col-md-6 mx-auto">
                        <div className="card border-0 shadow">
                            <div className="card-body">
                                <div className="text-center">
                                    <img src="/logo.png" alt="User Icon" style={{height: '5em'}}/>
                                </div>
                                <h1 className="text-center mt-4 mb-4">Utwórz konto</h1>
                                <form onSubmit={handleSubmit}>
                                    <fieldset>
                                        <div className="form-group">
                                            <label htmlFor="email">Adres E-mail:</label>
                                            <input
                                                className="form-control"
                                                placeholder="Wprowadź E-mail"
                                                type="email"
                                                value={email}
                                                onChange={(e) => setEmail(e.target.value)}
                                                required
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="password">Hasło:</label>
                                            <input
                                                className="form-control"
                                                placeholder="Wprowadź hasło"
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
                                            Zarejestruj
                                        </button>
                                    </fieldset>
                                </form>
                                {message && (
                                    <p
                                        className={`text-center mt-3 ${isSuccess ? 'text-success' : 'text-danger'}`}
                                    >
                                        {message}
                                    </p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
