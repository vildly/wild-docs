'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface AddProjectModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (url: string) => Promise<void>;
}

export default function AddProjectModal({ isOpen, onClose, onAdd }: AddProjectModalProps) {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const validateAndTransformUrl = (inputUrl: string): string | null => {
        try {
            // Remove any trailing slashes
            const cleanUrl = inputUrl.trim().replace(/\/+$/, '');
            
            // Check if it's a GitHub URL
            if (!cleanUrl.includes('github.com')) {
                throw new Error('Please enter a valid GitHub URL');
            }

            // Parse the URL
            const url = new URL(cleanUrl);
            
            // Check if it's a GitHub repository URL
            const pathParts = url.pathname.split('/').filter(Boolean);
            if (pathParts.length < 2) {
                throw new Error('Please enter a valid GitHub repository URL');
            }

            // If it's already a README URL, validate it
            if (pathParts.includes('blob') && pathParts.includes('README.md')) {
                // Get the index of 'blob' and 'README.md'
                const blobIndex = pathParts.indexOf('blob');
                const readmeIndex = pathParts.indexOf('README.md');
                
                // Ensure we have owner, repo, branch, and README.md in the correct order
                if (blobIndex >= 2 && readmeIndex === blobIndex + 2) {
                    const owner = pathParts[0];
                    const repo = pathParts[1];
                    const branch = pathParts[blobIndex + 1];
                    return `https://github.com/${owner}/${repo}/blob/${branch}/README.md`;
                }
                throw new Error('Invalid README URL format');
            }

            // If it's a repository URL, convert to README URL
            const [owner, repo] = pathParts;
            // Remove any existing README.md from the URL
            const cleanRepo = repo.replace('/README.md', '');
            return `https://github.com/${owner}/${cleanRepo}/blob/main/README.md`;
        } catch (err) {
            if (err instanceof Error) {
                throw new Error(err.message);
            }
            throw new Error('Please enter a valid GitHub URL');
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url.trim()) return;

        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const transformedUrl = validateAndTransformUrl(url);
            if (!transformedUrl) {
                throw new Error('Invalid GitHub URL');
            }
            
            await onAdd(transformedUrl);
            setSuccess(true);
            setUrl('');
            // Close modal after a short delay to show success message
            setTimeout(() => {
                onClose();
                setSuccess(false);
            }, 1500);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to add project');
        } finally {
            setLoading(false);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
                        onClick={onClose}
                    />
                    
                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md p-6 bg-gray-900 rounded-xl border border-gray-800 shadow-xl z-50"
                    >
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-200">Add New Project</h2>
                            <button
                                onClick={onClose}
                                className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
                            >
                                <svg
                                    className="w-5 h-5 text-gray-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <input
                                    type="url"
                                    value={url}
                                    onChange={(e) => setUrl(e.target.value)}
                                    placeholder="Enter GitHub repository URL"
                                    className="w-full p-3 bg-gray-800/50 text-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 border border-gray-700 placeholder-gray-500"
                                />
                                <p className="mt-2 text-sm text-gray-500">
                                    Example: https://github.com/username/repo
                                </p>
                            </div>

                            {error && (
                                <div className="p-3 bg-red-900/50 text-red-200 rounded-lg border border-red-800">
                                    {error}
                                </div>
                            )}

                            {success && (
                                <div className="p-3 bg-green-900/50 text-green-200 rounded-lg border border-green-800">
                                    Project added successfully!
                                </div>
                            )}

                            <div className="flex justify-end gap-3">
                                <button
                                    type="button"
                                    onClick={onClose}
                                    className="px-4 py-2 text-gray-400 hover:text-gray-300 transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={loading || !url.trim()}
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors"
                                >
                                    {loading ? (
                                        <div className="flex items-center gap-2">
                                            <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                            <span>Adding...</span>
                                        </div>
                                    ) : (
                                        'Add Project'
                                    )}
                                </button>
                            </div>
                        </form>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
} 