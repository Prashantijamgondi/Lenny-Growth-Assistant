import React from 'react';
import ReactMarkdown from 'react-markdown';
import { SandboxedIframe } from './SandboxedIframe';

interface ArtifactViewerProps {
  type: 'html' | 'markdown' | null;
  content: string;
  title: string;
  isOpen: boolean;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<ArtifactViewerProps> = ({ type, content, title, isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="flex flex-col h-full w-full bg-white border-l border-gray-200 shadow-xl overflow-hidden transition-all duration-300">
      <div className="flex justify-between items-center p-4 border-b border-gray-100 bg-gray-50">
        <h3 className="font-semibold text-gray-800 truncate pr-4">{title || 'Generated Artifact'}</h3>
        <button 
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-200 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div className="flex-1 overflow-auto p-4 bg-gray-50">
        {type === 'html' ? (
          <SandboxedIframe content={content} title={title} />
        ) : type === 'markdown' ? (
          <div className="prose prose-sm md:prose-base max-w-none bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="animate-pulse flex flex-col items-center">
              <div className="h-8 w-8 bg-gray-200 rounded-full mb-4"></div>
              <p>Generating artifact...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
