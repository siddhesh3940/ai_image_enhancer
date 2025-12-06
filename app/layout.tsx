import './globals.css'

export const metadata = {
  title: 'AI Video Enhancer',
  description: 'Enhance your images and videos with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}