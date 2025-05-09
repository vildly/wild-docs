'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import AddProjectModal from './AddProjectModal';

interface Project {
    name: string;
    readmeUrl: string;
    description: string;
}

// Base URL for the backend API (without /api prefix)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export default function ProjectSidebar() {
    const [isOpen, setIsOpen] = useState(true);
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);

    const fetchProjects = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/projects`);
            if (!response.ok) {
                throw new Error('Failed to fetch projects');
            }
            const data = await response.json();
            setProjects(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load projects');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProjects();
    }, []);

    const handleAddProject = async (url: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/documents/process-github`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repo_url: url }),
            });

            if (!response.ok) {
                throw new Error('Failed to add project');
            }

            // Refresh the projects list
            await fetchProjects();
        } catch (err) {
            throw new Error(err instanceof Error ? err.message : 'Failed to add project');
        }
    };

    return (
        <>
            <motion.div
                initial={{ x: 300 }}
                animate={{ x: isOpen ? 0 : 300 }}
                className="fixed right-0 top-0 h-screen w-80 bg-gray-900/95 border-l border-gray-800 shadow-xl backdrop-blur-lg"
            >
                <div className="p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-200">Projects</h2>
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
                        >
                            <svg
                                className={`w-5 h-5 text-gray-400 transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                    
                    <div className="space-y-4">
                        {loading ? (
                            <div className="flex items-center justify-center py-8">
                                <div className="w-6 h-6 border-2 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
                            </div>
                        ) : error ? (
                            <div className="p-4 bg-red-900/50 text-red-200 rounded-lg border border-red-800">
                                {error}
                            </div>
                        ) : projects.length === 0 ? (
                            <div className="text-center text-gray-400 py-8">
                                No projects found
                            </div>
                        ) : (
                            projects.map((project) => (
                                <motion.a
                                    key={project.name}
                                    href={project.readmeUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block p-4 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-blue-500/50 transition-colors"
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <h3 className="text-lg font-medium text-gray-200 mb-2">{project.name}</h3>
                                    <p className="text-sm text-gray-400">{project.description}</p>
                                </motion.a>
                            ))
                        )}

                        <motion.button
                            onClick={() => setIsAddModalOpen(true)}
                            className="w-full p-4 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-blue-500/50 transition-colors flex items-center justify-center gap-2 text-gray-400 hover:text-gray-300"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                        >
                            <svg
                                className="w-5 h-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                            </svg>
                            <span>Add Project</span>
                        </motion.button>
                    </div>
                </div>
            </motion.div>

            <AddProjectModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onAdd={handleAddProject}
            />
        </>
    );
} 