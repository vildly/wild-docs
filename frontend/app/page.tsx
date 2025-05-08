import ChatInterface from './components/ChatInterface';
import ProjectSidebar from './components/ProjectSidebar';

export default function Home() {
    return (
        <main className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
            <div className="container mx-auto pr-80">
                <div className="flex items-center justify-center gap-3 mb-8 pt-8">
                    <svg 
                        className="w-10 h-10 text-blue-500" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path 
                            d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" 
                            stroke="currentColor" 
                            strokeWidth="2" 
                            strokeLinecap="round" 
                            strokeLinejoin="round"
                        />
                        <path 
                            d="M14 2V8H20" 
                            stroke="currentColor" 
                            strokeWidth="2" 
                            strokeLinecap="round" 
                            strokeLinejoin="round"
                        />
                        <path 
                            d="M8 13H16" 
                            stroke="currentColor" 
                            strokeWidth="2" 
                            strokeLinecap="round" 
                            strokeLinejoin="round"
                        />
                        <path 
                            d="M8 17H16" 
                            stroke="currentColor" 
                            strokeWidth="2" 
                            strokeLinecap="round" 
                            strokeLinejoin="round"
                        />
                    </svg>
                    <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-blue-600">
                        Wild Docs
                    </h1>
                </div>
                <ChatInterface />
            </div>
            <ProjectSidebar />
        </main>
    );
}
