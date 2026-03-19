import { ChangeEvent } from 'react';

interface FileData {
  filename: string;
  chunks: number;
}

interface UploadPanelProps {
  onUpload: (file: File) => void;
  userType: string;
  setUserType: (type: string) => void;
  uploading: boolean;
  fileData: FileData | null;
  onClear: () => void;
  error: string | null;
}

export default function UploadPanel({ onUpload, userType, setUserType, uploading, fileData, onClear, error }: UploadPanelProps) {
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  return (
    <div className="p-6 flex flex-col h-full space-y-8">
      <h1 className="text-primary text-xl font-semibold tracking-tight">YourLegal</h1>

      <div className="space-y-2">
        <label className="text-[10px] uppercase tracking-widest text-muted-foreground font-medium">User Context</label>
        <select
          value={userType}
          onChange={(e) => setUserType(e.target.value)}
          className="w-full bg-surface border border-border text-sm p-2.5 text-foreground outline-none focus:border-primary transition-colors"
        >
          <option value="default">Human</option>
          <option value="lawyer">Lawyer</option>
          <option value="founder">Founder</option>
        </select>
      </div>

      <div className="flex-1 space-y-4">
        <label className="text-[10px] uppercase tracking-widest text-muted-foreground font-medium">Document Upload</label>
        <div className="relative group">
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            disabled={uploading}
          />
          <div className={`border-2 border-dashed border-border p-8 text-center ${uploading ? 'opacity-50' : 'group-hover:border-primary'}`}>
            <p className="text-sm text-muted-foreground">
              {uploading ? "Processing..." : "Drop PDF/DOCX or click to browse"}
            </p>
          </div>
        </div>

        {fileData && (
          <div className="bg-surface border border-border p-3 flex items-center justify-between">
            <div className="flex items-center space-x-2 overflow-hidden">
              <span className="text-green-500">✓</span>
              <span className="text-xs truncate text-foreground">{fileData.filename}</span>
            </div>
            <span className="mono text-[10px] text-primary bg-primary/10 px-1.5 py-0.5">
              {fileData.chunks} CHUNKS
            </span>
          </div>
        )}

        {error && <p className="text-xs text-destructive mt-2">{error}</p>}
        <p className="text-[11px] text-muted-foreground italic">Upload a legal document to begin analysis.</p>
      </div>

      <button
        onClick={onClear}
        className="w-full py-3 border border-border text-xs uppercase tracking-widest text-muted-foreground hover:bg-destructive/10 hover:text-destructive hover:border-destructive/50 transition-colors"
      >
        Clear Session
      </button>
    </div>
  );
}
