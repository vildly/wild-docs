'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

// Base URL for the backend API (without /api prefix)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

interface Source {
    title: string;
    url: string;
    content: string;
}

interface QueryResponse {
    status: string;
    data: {
        answer: string;
        sources: Source[];
        metadata: {
            model: string | null;
            run_id: string | null;
        };
    };
}

export default function ChatInterface() {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState<QueryResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const res = await fetch(`${API_BASE_URL}/api/chat/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            const data = await res.json();
            setResponse(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-4 min-h-[80vh]">
            <form onSubmit={handleSubmit} className="mb-8 sticky top-4 z-10">
                <div className="flex gap-2 backdrop-blur-lg bg-black/30 p-2 rounded-xl border border-gray-800 shadow-lg">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Ask about the documentation..."
                        className="flex-1 p-3 bg-gray-900/50 text-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 border border-gray-800 placeholder-gray-500"
                    />
                    <motion.button
                        type="submit"
                        disabled={loading || !query.trim()}
                        className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-500 hover:to-blue-600 disabled:from-gray-700 disabled:to-gray-800 disabled:cursor-not-allowed transition-all duration-200 shadow-lg"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        {loading ? (
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                <span>Processing...</span>
                            </div>
                        ) : (
                            'Ask'
                        )}
                    </motion.button>
                </div>
            </form>

            <AnimatePresence>
                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="p-4 mb-4 bg-red-900/50 text-red-200 rounded-lg border border-red-800"
                    >
                        {error}
                    </motion.div>
                )}

                {response && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-6"
                    >
                        <div className="prose prose-invert max-w-none bg-gray-900/50 p-6 rounded-xl border border-gray-800 shadow-lg">
                            <ReactMarkdown>{response.data.answer}</ReactMarkdown>
                        </div>

                        {response.data.sources.length > 0 && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.2 }}
                                className="mt-8"
                            >
                                <h3 className="text-lg font-semibold mb-4 text-gray-200">Sources</h3>
                                <div className="grid gap-4 md:grid-cols-2">
                                    {response.data.sources.map((source, index) => (
                                        <motion.div
                                            key={index}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: index * 0.1 }}
                                            className="p-4 bg-gray-900/50 rounded-lg border border-gray-800 hover:border-gray-700 transition-colors"
                                        >
                                            <a
                                                href={source.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-400 hover:text-blue-300 font-medium block mb-2"
                                            >
                                                {source.title}
                                            </a>
                                            <p className="text-sm text-gray-400">{source.content}</p>
                                        </motion.div>
                                    ))}
                                </div>
                            </motion.div>
                        )}

                        {response.data.metadata.model && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.4 }}
                                className="text-sm text-gray-500 mt-4 flex items-center gap-2"
                            >
                                <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                                Model: {response.data.metadata.model}
                            </motion.div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
} 