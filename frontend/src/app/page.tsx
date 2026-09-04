'use client';

import { useState } from 'react';
import { ChatPane } from '../components/Chat/ChatPane';
import { ArtifactViewer } from '../components/Artifact/ArtifactViewer';

export default function Home() {
  const [artifact, setArtifact] = useState<{content: string, type: string, title: string} | null>(null);

  const handleArtifactSelect = (content: string, type: string, title: string) => {
    setArtifact({ content, type, title });
  };

  return (
    <main className="flex h-screen w-full bg-white overflow-hidden font-sans">
      {/* Left side: Chat (takes up more space when artifact is closed) */}
      <div className={`transition-all duration-300 ease-in-out ${artifact ? 'w-full md:w-1/2 lg:w-5/12 hidden md:block' : 'w-full max-w-5xl mx-auto'}`}>
        <ChatPane onArtifactSelect={handleArtifactSelect} />
      </div>

      {/* Right side: Artifact Viewer */}
      {artifact && (
        <div className="w-full md:w-1/2 lg:w-7/12 h-full z-20 md:z-auto absolute md:relative top-0 right-0">
          <ArtifactViewer 
            type={artifact.type as any}
            content={artifact.content}
            title={artifact.title}
            isOpen={!!artifact}
            onClose={() => setArtifact(null)}
          />
        </div>
      )}
    </main>
  );
}
