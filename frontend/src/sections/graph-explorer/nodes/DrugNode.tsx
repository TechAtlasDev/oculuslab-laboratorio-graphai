import { Handle, Position, type NodeProps } from '@xyflow/react';
import { Pill } from '@phosphor-icons/react';

export function DrugNode({ data, selected }: NodeProps) {
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
          selected
            ? 'border-red-500 text-red-500 shadow-[0_0_25px_rgba(239,68,68,0.5)] scale-110'
            : 'border-red-500/30 hover:border-red-500 hover:scale-105 text-red-500/80 hover:shadow-lg'
        }`}
      >
        {/* Subtle inner radial gradient for 3D sphere feel */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-red-500/10 to-transparent pointer-events-none" />
        <Pill className="w-6 h-6 relative z-10" />
      </div>

      {/* Label underneath */}
      <div
        className={`mt-2 px-2 py-0.5 rounded-md text-[10px] font-bold tracking-wide uppercase transition-all duration-200 border bg-background/80 backdrop-blur-sm pointer-events-none select-none ${
          selected
            ? 'border-red-500/30 text-red-500 bg-red-500/5 scale-105 shadow-sm'
            : 'border-border/50 text-muted-foreground'
        }`}
      >
        {typeof data.label === 'string' ? data.label : 'DRUG'}
      </div>
    </div>
  );
}
