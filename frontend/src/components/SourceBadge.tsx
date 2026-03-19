interface Source {
  source: string;
  chunk_index: number;
  score?: number;
}

export default function SourceBadge({ source }: { source: Source }) {
  return (
    <div className="flex items-center border border-primary/30 px-2 py-1 space-x-2 bg-primary/5">
      <span className="text-[9px] text-primary font-bold uppercase tracking-tighter">Source</span>
      <span className="text-[10px] text-muted-foreground truncate max-w-[120px]">{source.source}</span>
      <span className="mono text-[9px] text-primary">[{source.chunk_index}]</span>
    </div>
  );
}
