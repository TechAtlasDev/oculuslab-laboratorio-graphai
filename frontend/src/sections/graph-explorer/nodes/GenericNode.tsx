import { Handle, Position, type NodeProps } from '@xyflow/react';
import { Flask, Heartbeat, Info, Hash, Link as LinkIcon } from '@phosphor-icons/react';

const ICON_MAP: Record<string, React.ReactNode> = {
  PHE: <Info className="w-6 h-6" />,
  BPO: <Flask className="w-6 h-6" />,
  MFN: <Flask className="w-6 h-6" />,
  CCO: <Flask className="w-6 h-6" />,
  ANA: <Heartbeat className="w-6 h-6" />,
  PWY: <LinkIcon className="w-6 h-6" />,
};

const THEME_MAP: Record<string, { border: string, text: string, glow: string, bgGlow: string, label: string }> = {
  PHE: { border: 'border-amber-500/30 hover:border-amber-500 text-amber-500/80', text: 'text-amber-500', glow: 'shadow-[0_0_20px_rgba(245,158,11,0.4)] border-amber-500 text-amber-500 scale-110', bgGlow: 'bg-gradient-to-tr from-amber-500/10', label: 'PHENOTYPE' },
  BPO: { border: 'border-violet-500/30 hover:border-violet-500 text-violet-500/80', text: 'text-violet-500', glow: 'shadow-[0_0_20px_rgba(139,92,246,0.4)] border-violet-500 text-violet-500 scale-110', bgGlow: 'bg-gradient-to-tr from-violet-500/10', label: 'BIOL_PROCESS' },
  MFN: { border: 'border-indigo-500/30 hover:border-indigo-500 text-indigo-500/80', text: 'text-indigo-500', glow: 'shadow-[0_0_20px_rgba(99,102,241,0.4)] border-indigo-500 text-indigo-500 scale-110', bgGlow: 'bg-gradient-to-tr from-indigo-500/10', label: 'MOL_FUNCTION' },
  CCO: { border: 'border-purple-500/30 hover:border-purple-500 text-purple-500/80', text: 'text-purple-500', glow: 'shadow-[0_0_20px_rgba(168,85,247,0.4)] border-purple-500 text-purple-500 scale-110', bgGlow: 'bg-gradient-to-tr from-purple-500/10', label: 'CELL_COMPONENT' },
  ANA: { border: 'border-pink-500/30 hover:border-pink-500 text-pink-500/80', text: 'text-pink-500', glow: 'shadow-[0_0_20px_rgba(236,72,153,0.4)] border-pink-500 text-pink-500 scale-110', bgGlow: 'bg-gradient-to-tr from-pink-500/10', label: 'ANATOMY' },
  PWY: { border: 'border-fuchsia-500/30 hover:border-fuchsia-500 text-fuchsia-500/80', text: 'text-fuchsia-500', glow: 'shadow-[0_0_20px_rgba(217,70,239,0.4)] border-fuchsia-500 text-fuchsia-500 scale-110', bgGlow: 'bg-gradient-to-tr from-fuchsia-500/10', label: 'PATHWAY' },
};

const DEFAULT_THEME = {
  border: 'border-muted-foreground/30 hover:border-muted-foreground text-muted-foreground/80',
  text: 'text-muted-foreground',
  glow: 'shadow-[0_0_20px_rgba(100,116,139,0.4)] border-muted-foreground text-muted-foreground scale-110',
  bgGlow: 'bg-gradient-to-tr from-muted-foreground/10',
  label: 'GENERIC'
};

export function GenericNode({ data, selected }: NodeProps) {
  const nodeType = ((data.fullNode as any)?.label || '') as string;
  const theme = THEME_MAP[nodeType] || DEFAULT_THEME;
  const icon = ICON_MAP[nodeType] || <Hash className="w-6 h-6" />;

  return (
    <div className="relative flex flex-col items-center group">
      {/* Target/Source handles in center (hidden, edges render behind) */}
      <Handle
        type="target"
        position={Position.Top}
        className="!top-1/2 !left-1/2 !-translate-x-1/2 !-translate-y-1/2 !w-4 !h-4 !opacity-0 pointer-events-none"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="!top-1/2 !left-1/2 !-translate-x-1/2 !-translate-y-1/2 !w-4 !h-4 !opacity-0 pointer-events-none"
      />

      {/* Sphere Node */}
      <div
        className={`flex items-center justify-center w-18 h-18 rounded-full border-2 transition-all duration-300 bg-card/90 backdrop-blur-md shadow-md ${
          selected ? theme.glow : `${theme.border} hover:scale-105 hover:shadow-lg`
        }`}
      >
        {/* Subtle inner radial gradient for 3D sphere feel */}
        <div className={`absolute inset-0 rounded-full ${theme.bgGlow} to-transparent pointer-events-none`} />
        <div className="relative z-10">{icon}</div>
      </div>

      {/* Label underneath */}
      <div
        className={`mt-2 px-2 py-0.5 rounded-md text-[10px] font-bold tracking-wide uppercase transition-all duration-200 border bg-background/80 backdrop-blur-sm pointer-events-none select-none ${
          selected
            ? `border-border/80 ${theme.text} bg-muted scale-105 shadow-sm`
            : 'border-border/50 text-muted-foreground'
        }`}
      >
        {typeof data.label === 'string' ? data.label : theme.label}
      </div>
    </div>
  );
}
