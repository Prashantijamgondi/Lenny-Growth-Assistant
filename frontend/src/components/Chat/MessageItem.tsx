import React from 'react';

export interface Source {
  episode: string;
  guest: string;
  timestamp: string;
  score: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources?: Source[];
}

interface MessageItemProps {
  message: Message;
  onArtifactClick?: (content: string, type: string, title: string) => void;
}

export const MessageItem: React.FC<MessageItemProps> = ({ message, onArtifactClick }) => {
  const isUser = message.role === 'user';
  
  // Very basic XML artifact parsing for the demo
  const extractArtifact = (text: string) => {
    const artifactRegex = /<artifact\s+type="(html|markdown)"\s+title="([^"]+)">([\s\S]*?)<\/artifact>/i;
    const match = text.match(artifactRegex);
    
    if (match) {
      const type = match[1];
      const title = match[2];
      const content = match[3];
      const cleanText = text.replace(artifactRegex, '').trim();
      return { hasArtifact: true, cleanText, type, title, content };
    }
    
    return { hasArtifact: false, cleanText: text };
  };

  const { hasArtifact, cleanText, type, title, content } = extractArtifact(message.content);

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div className={`flex max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center text-sm font-bold shadow-sm ${
          isUser ? 'bg-indigo-600 text-white ml-3' : 'bg-emerald-500 text-white mr-3'
        }`}>
          {isUser ? 'U' : 'L'}
        </div>
        
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-3 rounded-2xl shadow-sm ${
            isUser ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white border border-gray-200 text-gray-800 rounded-tl-none'
          }`}>
            <div className="whitespace-pre-wrap leading-relaxed text-sm">
              {cleanText}
            </div>
            
            {hasArtifact && (
              <div className="mt-4 border-t border-gray-100 pt-3">
                <button 
                  onClick={() => onArtifactClick?.(content!, type!, title!)}
                  className="flex items-center space-x-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors w-full justify-center border border-indigo-100"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  <span>View Artifact: {title}</span>
                </button>
              </div>
            )}
          </div>
          
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-2 text-xs text-gray-500 flex flex-wrap gap-2 max-w-full">
              {message.sources.slice(0, 3).map((source, idx) => (
                <span key={idx} className="bg-gray-100 px-2 py-1 rounded-md border border-gray-200 inline-flex items-center shadow-sm">
                  <svg className="w-3 h-3 mr-1 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h2V2zM5 5v8h10V5H5zm2 2h2v2H7V7zm4 0h2v2h-2V7zm-4 4h2v2H7v-2zm4 0h2v2h-2v-2z" clipRule="evenodd" />
                  </svg>
                  {source.guest} • {source.timestamp}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
