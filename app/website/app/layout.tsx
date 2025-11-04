import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GraphCare - Transform Your Codebase Into a Living Knowledge Graph',
  description: 'Professional knowledge extraction service. Turn your code and documentation into a queryable, navigable L2 organizational graph using Mind Protocol\'s universal type system.',
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
