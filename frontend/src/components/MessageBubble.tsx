import SourceBadge from './SourceBadge';

interface Message {
  role: string;
  content: string;
  sources?: { source: string; chunk_index: number; score?: number }[];
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] ${isUser ? '' : 'space-y-3'}`}>
        <div className={`p-4 text-sm leading-relaxed ${
          isUser
            ? 'bg-primary text-primary-foreground font-medium'
            : 'bg-surface border-l-2 border-primary text-foreground'
        }`}>
          {message.content}
        </div>

        {!isUser && message.sources && (
          <div className="flex flex-wrap gap-2">
            {message.sources.map((source, idx) => (
              <SourceBadge key={idx} source={source} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
