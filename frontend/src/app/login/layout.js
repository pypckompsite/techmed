export default function RootLayout({children}) {
    return (
        <html lang="en">
        <body  style={{
            backgroundImage: 'url("/tlo.png")',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        }}
            //className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
            {children}
        </body>
        </html>
    );
}


