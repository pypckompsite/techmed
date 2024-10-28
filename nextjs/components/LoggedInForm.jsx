import { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function UserInfoPanel() {
    const [userInfo, setUserInfo] = useState(null); // Stan na dane użytkownika
    const [message, setMessage] = useState('');

    useEffect(() => {
        // Funkcja pobierająca dane użytkownika
        const fetchUserInfo = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/auth/get_my_info", {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: "include",
                });

                if (response.ok) {
                    const data = await response.json();
                    setUserInfo(data);
                    console.log("User Data:", data); // Logowanie danych użytkownika
                } else {
                    setMessage("Błąd pobierania danych użytkownika");
                    console.error("Błąd pobierania danych użytkownika");
                }
            } catch (error) {
                setMessage("Błąd: Nie udało się pobrać danych użytkownika");
                console.error("Błąd:", error);
            }
        };

        fetchUserInfo();
    }, []);

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
                padding: '20px',
            }}
        >
            <div className="container mt-5 pt-5">
                <div className="row justify-content-center">
                    <div className="col-10 col-sm-8 col-md-6 col-lg-5">
                        <div className="card shadow-lg border-0 rounded" style={{ overflow: 'hidden' }}>
                            <div
                                className="card-header text-center"
                                style={{
                                    backgroundColor: '#042F43',
                                    color: '#ffffff',
                                    padding: '1.5em',
                                    fontSize: '1.5em',
                                    fontWeight: 'bold',
                                    letterSpacing: '1px',
                                    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)',
                                }}
                            >
                                Dane użytkownika
                            </div>
                            <div className="card-body p-4" style={{ backgroundColor: '#f9f9f9' }}>
                                <div className="text-center mb-4">
                                    <img src="/icons/logo.png" alt="User Icon" style={{ height: '80px', borderRadius: '50%', border: '2px solid #042F43', padding: '5px' }} />
                                </div>
                                {message && (
                                    <p className="text-center text-danger mb-3" style={{ fontSize: '1.1em', fontWeight: '500' }}>
                                        {message}
                                    </p>
                                )}
                                {userInfo ? (
                                    <div style={{ lineHeight: '1.8', color: '#333' }}>
                                        <div className="mb-4 p-3" style={{ border: '1px solid #e0e0e0', borderRadius: '8px', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
                                            <h5 style={{ color: '#042F43', fontWeight: '600' }}>Informacje ogólne</h5>
                                            <p style={{ fontSize: '1.05em' }}><strong>Email:</strong> {userInfo.email}</p>
                                            <p style={{ fontSize: '1.05em' }}><strong>Typ konta:</strong> {userInfo.type}</p>
                                        </div>
                                        <div className="mb-3 p-3" style={{ border: '1px solid #e0e0e0', borderRadius: '8px', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
                                            <h5 style={{ color: '#042F43', fontWeight: '600' }}>Szczegóły pacjenta</h5>
                                            <p style={{ fontSize: '1.05em' }}><strong>Imię:</strong> {userInfo.Patient.first_name}</p>
                                            <p style={{ fontSize: '1.05em' }}><strong>Nazwisko:</strong> {userInfo.Patient.last_name}</p>
                                            <p style={{ fontSize: '1.05em' }}><strong>PESEL:</strong> {userInfo.Patient.PESEL}</p>
                                            <p style={{ fontSize: '1.05em' }}><strong>Adres:</strong> {userInfo.Patient.address}</p>
                                            <p style={{ fontSize: '1.05em' }}><strong>Telefon:</strong> {userInfo.Patient.phone_number}</p>
                                        </div>
                                    </div>
                                ) : (
                                    !message && <p className="text-center" style={{ fontSize: '1.2em', color: '#555' }}>Ładowanie danych...</p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
