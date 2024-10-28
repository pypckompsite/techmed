// pages/profile.js
import React from 'react';

export default function Profile() {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          backgroundColor: '#f7f9fc',
          color: '#333',
          fontFamily: 'Arial, sans-serif'
        }}
      >
        <h1>Profil Użytkownika</h1>
        <div style={{
          padding: '20px',
          borderRadius: '8px',
          backgroundColor: '#fff',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          maxWidth: '400px',
          width: '100%',
          textAlign: 'center'
        }}>
          <p><strong>Imię:</strong> Anna</p>
          <p><strong>Nazwisko:</strong> Kowalska</p>
          <p><strong>Wiek:</strong> 56 lat</p>
        </div>
      </div>
    );
  }
  