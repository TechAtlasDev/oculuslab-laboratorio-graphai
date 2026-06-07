import { X } from '@phosphor-icons/react';
import type { GraphEdge, GraphNode } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface EdgeDetailsPanelProps {
  edge: GraphEdge;
  nodes: GraphNode[];
  onClose: () => void;
}

export function EdgeDetailsPanel({ edge, nodes, onClose }: EdgeDetailsPanelProps) {
  // Find the full node objects for source and target
  // Remember that D3 might have mutated edge.source into an object, or it might be a string.
  const sourceId = typeof edge.source === 'object' ? (edge.source as any).id : edge.source;
  const targetId = typeof edge.target === 'object' ? (edge.target as any).id : edge.target;
  
  const sourceNode = nodes.find(n => n.id === sourceId);
  const targetNode = nodes.find(n => n.id === targetId);

  return (
    <div className="w-[400px] h-full bg-background border-l border-border shadow-xl flex flex-col">
      <div className="flex items-center justify-between p-4 border-b border-border">
        <h2 className="text-lg font-semibold tracking-tight">Detalles de Conexión</h2>
        <button
          onClick={onClose}
          className="p-1 rounded-md hover:bg-muted text-muted-foreground transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              Relación
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xl font-bold font-mono text-primary">
              {edge.relation}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              Nodos Asociados
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted/50 p-3 rounded-lg">
              <div className="text-xs text-muted-foreground mb-1">Origen (Source)</div>
              <div className="font-medium">{sourceNode?.display_name || sourceId}</div>
              <div className="text-xs text-muted-foreground mt-1 font-mono">{sourceId}</div>
            </div>
            
            <div className="flex justify-center">
              <div className="w-px h-4 bg-border"></div>
            </div>
            
            <div className="bg-muted/50 p-3 rounded-lg">
              <div className="text-xs text-muted-foreground mb-1">Destino (Target)</div>
              <div className="font-medium">{targetNode?.display_name || targetId}</div>
              <div className="text-xs text-muted-foreground mt-1 font-mono">{targetId}</div>
            </div>
          </CardContent>
        </Card>

        {edge.properties && Object.keys(edge.properties).length > 0 && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
                Propiedades Adicionales
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(edge.properties).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-start py-1 border-b border-border/50 last:border-0">
                    <span className="text-sm font-medium text-muted-foreground capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="text-sm text-right break-words max-w-[200px]">
                      {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
