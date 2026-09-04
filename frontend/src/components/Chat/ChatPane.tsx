'use client';

import React, { useState, useRef, useEffect } from 'react';
import { MessageItem, Message } from './MessageItem';
import { ModelSelector } from './ModelSelector';
import { useChatStream } from '../../hooks/useChatStream';

interface ChatPaneProps {
  onArtifactSelect: (content: string, type: string, title: string) => void;
}

export const ChatPane: React.FC<ChatPaneProps> = ({ onArtifactSelect }) => {
  // Hardcoded session for demo purposes
  const sessionId = "00000000-0000-0000-0000-000000000000";
  const { messages, sendMessage, isStreaming, statusText } = useChatStream(sessionId);
  
  const [input, setInput] = useState('');
  const [provider, setProvider] = useState<'ollama' | 'claude'>('ollama');
  const [mode, setMode] = useState<'default' | 'ship30'>('default');
  
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, statusText]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input, provider, mode);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 relative">
      <div className="p-4 border-b border-gray-200 bg-white shadow-sm flex justify-between items-center z-10">
        <div>
          <h1 className="text-lg font-bold text-gray-900">The Lenny Growth Assistant</h1>
          <p className="text-xs text-gray-500">Grounded in 200+ hours of podcast transcripts</p>
        </div>
        <ModelSelector 
          provider={provider} setProvider={setProvider} 
          mode={mode} setMode={setMode} 
        />
      </div>

      <div className="flex-1 overflow-y-auto p-4 md:p-6 pb-32">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center max-w-lg mx-auto opacity-70">
            <div className="bg-indigo-100 p-4 rounded-full mb-4">
              <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">How can I help you grow?</h2>
            <p className="text-gray-600 text-sm mb-6">Ask me about product-market fit, growth loops, or request a Ship 30 for 30 essay based on Lenny's guests.</p>
            <div className="grid grid-cols-1 gap-2 w-full text-left">
              <button onClick={() => setInput("What did Brian Chesky say about starting Airbnb?")} className="text-sm bg-white p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:shadow-sm transition-all text-gray-700">"What did Brian Chesky say about starting Airbnb?"</button>
              <button onClick={() => { setInput("Write a Ship 30 for 30 essay about building growth loops."); setMode('ship30'); }} className="text-sm bg-white p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:shadow-sm transition-all text-gray-700">"Write a Ship 30 for 30 essay about building growth loops."</button>
            </div>
          </div>
        ) : (
          messages.map(msg => (
            <MessageItem key={msg.id} message={msg} onArtifactClick={onArtifactSelect} />
          ))
        )}
        
        {statusText && (
          <div className="text-xs text-gray-500 italic ml-14 flex items-center">
            <div className="w-4 h-4 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin mr-2"></div>
            {statusText}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gray-50 via-gray-50 to-transparent p-4 pt-10">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isStreaming}
            placeholder="Ask about growth tactics..."
            className="w-full bg-white border border-gray-300 rounded-full pl-6 pr-16 py-4 shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-800 disabled:bg-gray-100 disabled:text-gray-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="absolute right-2 top-2 bottom-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white rounded-full px-4 font-semibold transition-colors flex items-center justify-center"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};
