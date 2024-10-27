import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Logowanie danych przed wysłaniem
    console.log('Email:', email, 'Password:', password);
  
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
    });
  
    // Oczekiwanie na odpowiedź
    if (res.ok) {
      setMessage('Login successful');
      setTimeout(() => {
        router.push('/profile');
      }, 2000);
    } else {
      const errorData = await res.json();
      console.log('Error Data:', errorData); // Logowanie błędów
      
      // Obsługa błędów
      if (Array.isArray(errorData.detail)) {
        setMessage(errorData.detail.map((error) => error.msg).join(', '));
      } else if (typeof errorData.detail === 'string') {
        setMessage(errorData.detail);
      } else {
        setMessage('An error occurred');
      }
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
