import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Link from 'next/link';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/auth/login', {
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
      setMessage('Login successful');
    } else {
      const errorData = await res.json();
      setMessage(errorData.detail || 'An error occurred');
    }
  };

  return (
    <div
      style={{
        backgroundImage: 'url("/icons/tlo.png")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div className="container mt-5 pt-5">
        <div className="row">
          <div className="col-9 col-sm-7 col-md-6 m-auto">
            <div className="card border-0 shadow">
              <div className="card-body">
                <div className="text-center">
                  <img src="/icons/logo.png" alt="User Icon" style={{ height: '5em' }} />
                </div>
                <h1 className="text-center mt-4 mb-4">Zaloguj się</h1>
                <form onSubmit={handleSubmit}>
                  <fieldset>
                    <div className="form-group">
                      <label htmlFor="email">Adres E-mail:</label>
                      <input
                        className="form-control"
                        placeholder="E-mail"
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
                {message && <p className="text-center mt-3 text-danger">{message}</p>}
                
                {/* Przycisk do rejestracji */}
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
    </div>
  );
}
