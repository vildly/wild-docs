import './globals.css';
import { Inter } from 'next/font/google';
import Settings from './components/Settings';
import ProjectSidebar from './components/ProjectSidebar';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Wild Docs',
  description: 'Documentation made wild',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
          <div className="fixed top-4 right-4 z-50">
            <Settings />
          </div>
          <div className="fixed right-0 top-0 h-screen z-40">
            <ProjectSidebar />
          </div>
          {children}
        </div>
      </body>
    </html>
  );
}
