'use client';

import { useState, useEffect } from 'react';
import { Cog6ToothIcon } from '@heroicons/react/24/outline';

export default function Settings() {
  const [isOpen, setIsOpen] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    const storedKey = localStorage.getItem('openai_api_key');
    if (storedKey) {
      setApiKey('sk-....' + storedKey.slice(-4)); // Show only last 4 chars for security
    }
  }, []);

  const handleSave = () => {
    if (apiKey.startsWith('sk-') && apiKey.length > 20) {
      localStorage.setItem('openai_api_key', apiKey);
      setShowSuccess(true);
      setTimeout(() => {
        setShowSuccess(false);
        setIsOpen(false);
      }, 1500);
    }
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(true)}
        className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        title="Settings"
      >
        <Cog6ToothIcon className="w-6 h-6" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-semibold mb-4">Settings</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">
                OpenAI API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-..."
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
              />
              <p className="text-sm text-gray-500 mt-1">
                Your API key will be stored locally and never sent to our servers.
              </p>
            </div>

            {showSuccess && (
              <div className="mb-4 p-2 bg-green-100 text-green-700 rounded">
                Settings saved successfully!
              </div>
            )}

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 dark:text-gray-300 dark:hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 