import React from 'react';

interface ModelSelectorProps {
  provider: 'ollama' | 'gemini';
  setProvider: (p: 'ollama' | 'gemini') => void;
  mode: 'default' | 'ship30';
  setMode: (m: 'default' | 'ship30') => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({ provider, setProvider, mode, setMode }) => {
  return (
    <div className="flex items-center space-x-4 bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex items-center space-x-2">
        <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Provider</label>
        <select 
          value={provider} 
          onChange={(e) => setProvider(e.target.value as 'ollama' | 'gemini')}
          className="text-sm bg-gray-50 border border-gray-200 rounded-md py-1 px-2 focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="gemini">Gemini 2.5 (Cloud)</option>
          <option value="ollama">Ollama (Local)</option>
        </select>
      </div>
      
      <div className="flex items-center space-x-2">
        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Skill</span>
        <select 
          value={mode} 
          onChange={(e) => setMode(e.target.value as 'default' | 'ship30')}
          className="text-sm bg-gray-50 border border-gray-200 text-gray-700 rounded px-2 py-1 focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="default">Standard RAG</option>
          <option value="ship30">Ship 30 for 30</option>
        </select>
      </div>
    </div>
  );
};
