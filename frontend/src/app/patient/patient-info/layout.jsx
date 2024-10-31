export default function RootLayout({children}) {
    return (
        <html lang="en">
        <body
            //className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
        <div
            style={{
                backgroundImage: 'url("/tlo.png")',
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            {children}
        </div>
        </body>
        </html>
    );
}


