import React from 'react';
import { ChatPane } from '@/components/Chat/ChatPane';
import { ArtifactViewer } from '@/components/Artifact/ArtifactViewer';

export default function Home() {
  return (
    <main className="flex h-screen w-screen bg-gray-50 text-gray-900 font-sans overflow-hidden">
      {/* Left Column: Chat Interface */}
      <section className="flex-1 flex flex-col max-w-3xl mx-auto border-r border-gray-200 bg-white shadow-sm">
        <header className="p-6 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-gray-900">
              Lenny Growth Assistant
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Ask product & growth questions backed by podcast transcripts.
            </p>
          </div>
        </header>
        
        {/* The main chat component handles the history and input */}
        <div className="flex-1 overflow-y-auto">
          <ChatPane />
        </div>
      </section>

      {/* Right Column: Artifact Viewer (Hidden on mobile) */}
      <aside className="hidden lg:flex flex-col w-1/2 h-full bg-gray-50 p-6">
        <div className="h-full w-full bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <ArtifactViewer />
        </div>
      </aside>
    </main>
  );
}
