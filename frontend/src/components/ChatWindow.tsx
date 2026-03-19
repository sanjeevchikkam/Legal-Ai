import { useRef, useEffect, useState, FormEvent } from 'react';
import MessageBubble from './MessageBubble';

interface Message {
  role: string;
  content: string;
  sources?: { source: string; chunk_index: number; score?: number }[];
}

interface ChatWindowProps {
  messages: Message[];
  onSend: (content: string) => void;
  loading: boolean;
  disabled: boolean;
}

export default function ChatWindow({ messages, onSend, loading, disabled }: ChatWindowProps) {
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, loading]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (disabled || loading || !input.trim()) return;
    onSend(input);
    setInput('');
  };

  return (
    <>
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 pb-32">
        {messages.length === 0 && !loading && (
          <div className="h-full flex items-center justify-center">
            <p className="text-muted-foreground text-sm tracking-wide">Ask anything about your document</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-surface border-l-2 border-primary p-4">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-muted-foreground animate-pulse" />
                <div className="w-1.5 h-1.5 bg-muted-foreground animate-pulse [animation-delay:75ms]" />
                <div className="w-1.5 h-1.5 bg-muted-foreground animate-pulse [animation-delay:150ms]" />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="absolute bottom-0 left-0 right-0 p-6 bg-background">
        <form onSubmit={handleSubmit} className="flex border border-border bg-surface focus-within:border-primary transition-colors">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={disabled}
            placeholder={disabled ? "Upload a document to enable chat" : "Enter query..."}
            className="flex-1 bg-transparent p-4 text-sm outline-none text-foreground placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="px-8 bg-primary text-primary-foreground text-xs font-bold uppercase tracking-widest disabled:bg-muted disabled:text-muted-foreground transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </>
  );
}
