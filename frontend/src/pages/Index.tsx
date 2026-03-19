import { useState } from 'react';
import UploadPanel from '@/components/UploadPanel';
import ChatWindow from '@/components/ChatWindow';

const API_BASE = "http://localhost:8000";

interface FileData {
  filename: string;
  chunks: number;
}

interface Message {
  role: string;
  content: string;
  sources?: { source: string; chunk_index: number; score?: number }[];
}

export default function Index() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [userType, setUserType] = useState('default');
  const [messages, setMessages] = useState<Message[]>([]);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileData, setFileData] = useState<FileData | null>(null);

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();
      setSessionId(data.session_id);
      setFileData({ filename: data.filename, chunks: data.chunks_stored });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || !sessionId) return;
    setMessages(prev => [...prev, { role: 'user', content }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: content, user_type: userType }),
      });
      if (!res.ok) throw new Error('Message failed');
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer, sources: data.sources }]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    if (sessionId) {
      try { await fetch(`${API_BASE}/delete/${sessionId}`, { method: 'DELETE' }); } catch {}
    }
    setSessionId(null);
    setMessages([]);
    setFileData(null);
    setError(null);
  };

  return (
    <div className="flex flex-col md:flex-row h-svh w-full overflow-hidden">
      <div className="w-full md:w-[30%] border-b md:border-b-0 md:border-r border-border bg-background flex flex-col">
        <UploadPanel
          onUpload={handleUpload}
          userType={userType}
          setUserType={setUserType}
          uploading={uploading}
          fileData={fileData}
          onClear={handleClear}
          error={error}
        />
      </div>
      <div className="w-full md:w-[70%] bg-background flex flex-col relative">
        <ChatWindow
          messages={messages}
          onSend={handleSendMessage}
          loading={loading}
          disabled={!sessionId}
        />
      </div>
    </div>
  );
}
