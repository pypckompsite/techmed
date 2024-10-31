"use client";

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";

export default function PatientInfoPanel() {
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
        <div className="container mx-auto mt-5 pt-5">
            <div className="flex justify-center">
                <Card className="max-w-md shadow-lg">
                    <CardHeader className="bg-[#042F43] text-white text-center py-4">
                        <CardTitle className="text-lg font-bold">Dane użytkownika</CardTitle>
                    </CardHeader>
                    <CardContent className="p-4 bg-gray-50">
                        <div className="text-center mb-4">
                            <Image
                                src="/logo.png"
                                alt="User Icon"
                                height={80}
                                width={80}
                                className="rounded-full border-2 border-[#042F43] p-1"
                            />
                        </div>
                        {message && (
                            <p className="text-center text-red-500 mb-3 font-medium">{message}</p>
                        )}
                        {userInfo ? (
                            <div className="text-gray-800">
                                <div className="mb-4 p-3 border border-gray-300 rounded-lg shadow-md">
                                    <h5 className="text-[#042F43] font-semibold">Informacje ogólne</h5>
                                    <p><strong>Email:</strong> {userInfo.email}</p>
                                    <p><strong>Typ konta:</strong> {userInfo.type}</p>
                                </div>
                                <div className="mb-3 p-3 border border-gray-300 rounded-lg shadow-md">
                                    <h5 className="text-[#042F43] font-semibold">Szczegóły pacjenta</h5>
                                    <p><strong>Imię:</strong> {userInfo.Patient.first_name}</p>
                                    <p><strong>Nazwisko:</strong> {userInfo.Patient.last_name}</p>
                                    <p><strong>PESEL:</strong> {userInfo.Patient.PESEL}</p>
                                    <p><strong>Adres:</strong> {userInfo.Patient.address}</p>
                                    <p><strong>Telefon:</strong> {userInfo.Patient.phone_number}</p>
                                </div>
                            </div>
                        ) : (
                            !message &&
                            <p className="text-center text-gray-500">Ładowanie danych...</p>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
