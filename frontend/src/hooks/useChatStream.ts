import { useState, useCallback } from 'react';
import { Message } from '../components/Chat/MessageItem';

export function useChatStream(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [statusText, setStatusText] = useState('');

  const sendMessage = useCallback(async (
    text: string, 
    provider: string, 
    mode: string
  ) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text
    };

    setMessages(prev => [...prev, userMessage]);
    setIsStreaming(true);
    setStatusText('Connecting...');

    const assistantId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, {
      id: assistantId,
      role: 'assistant',
      content: ''
    }]);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: text,
          provider,
          mode
        })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                setIsStreaming(false);
                setStatusText('');
                break;
              }
              
              try {
                const parsed = JSON.parse(data);
                if (parsed.type === 'token') {
                  setMessages(prev => prev.map(m => 
                    m.id === assistantId ? { ...m, content: m.content + parsed.content } : m
                  ));
                } else if (parsed.type === 'sources') {
                  setMessages(prev => prev.map(m => 
                    m.id === assistantId ? { ...m, sources: parsed.content } : m
                  ));
                } else if (parsed.type === 'status') {
                  setStatusText(parsed.content);
                }
              } catch (e) {
                console.error("Error parsing stream chunk", e);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error during chat stream:', error);
      setMessages(prev => prev.map(m => 
        m.id === assistantId ? { ...m, content: m.content + '\n\n**Error connecting to server.**' } : m
      ));
    } finally {
      setIsStreaming(false);
      setStatusText('');
    }
  }, [sessionId]);

  return { messages, sendMessage, isStreaming, statusText };
}
