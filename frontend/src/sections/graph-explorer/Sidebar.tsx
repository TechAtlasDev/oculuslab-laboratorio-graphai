import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { MagnifyingGlass, ChartBar, Globe } from '@phosphor-icons/react';
import { fetchStats } from '@/lib/api';
import type { MetricsResponse, GraphStats, GraphNode } from '@/lib/api';
import { AdvancedDiscoveryDialog } from './AdvancedDiscoveryDialog';

interface SidebarProps {
  onSearch: (nodeId: string, limit: number) => void;
  metrics: MetricsResponse | null;
  loading: boolean;
  onInjectNodes: (nodes: GraphNode[]) => void;
}

export function Sidebar({ onSearch, metrics, loading, onInjectNodes }: SidebarProps) {
  const [nodeId, setNodeId] = useState('ENSG00000146648');
  const [limit, setLimit] = useState(15);
  const [stats, setStats] = useState<GraphStats | null>(null);

  useEffect(() => {
    let isMounted = true;
    fetchStats()
      .then(data => {
        if (isMounted) setStats(data);
      })
      .catch(err => console.error("Failed to fetch stats", err));
    return () => { isMounted = false; };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (nodeId.trim()) {
      onSearch(nodeId.trim(), limit);
    }
  };

  return (
    <div className="w-80 h-full border-r bg-background flex flex-col overflow-y-auto">
      <div className="p-6">
        <h2 className="text-2xl font-bold tracking-tight mb-2">Graph Explorer</h2>
        <p className="text-muted-foreground text-sm mb-6">
          Query the biomedical knowledge graph.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4 mb-4">
          <div className="space-y-2">
            <Label htmlFor="nodeId">Node ID</Label>
            <Input
              id="nodeId"
              placeholder="e.g. ENSG00000146648"
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="bg-muted/50"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="limit">Connection Limit</Label>
            <Input
              id="limit"
              type="number"
              min={1}
              max={100}
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="bg-muted/50"
            />
          </div>
          <Button type="submit" className="w-full" disabled={loading}>
            <MagnifyingGlass className="mr-2 h-4 w-4" weight="bold" />
            {loading ? 'Searching...' : 'Explore Node'}
          </Button>
        </form>

        <AdvancedDiscoveryDialog onInjectNodes={onInjectNodes} />
      </div>

      <Separator />

      <div className="p-6 flex-1">
        {metrics ? (
          <>
            <div className="flex items-center gap-2 mb-4">
              <ChartBar className="h-5 w-5 text-primary" weight="fill" />
              <h3 className="font-semibold text-lg">Métricas Topológicas</h3>
            </div>
            <div className="space-y-4">
              <Card className="bg-card">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Grado Total</CardTitle>
                  <div className="text-3xl font-bold">{metrics.degree}</div>
                </CardHeader>
              </Card>

              <div className="space-y-3">
                <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Desglose de Relaciones</h4>
                <div className="space-y-2">
                  {metrics.relations_count.map((rel, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-muted/30 p-2 rounded-md text-sm border border-border/50">
                      <span className="font-medium truncate mr-2">{rel.relation}</span>
                      <Badge variant="secondary" className="shrink-0">{rel.count}</Badge>
                    </div>
                  ))}
                  {metrics.relations_count.length === 0 && (
                    <p className="text-sm text-muted-foreground italic">No relations found.</p>
                  )}
                </div>
              </div>
            </div>
          </>
        ) : stats ? (
          <>
            <div className="flex items-center gap-2 mb-4">
              <Globe className="h-5 w-5 text-primary" weight="fill" />
              <h3 className="font-semibold text-lg">Estado Global</h3>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-2">
                <Card className="bg-card">
                  <CardContent className="p-3">
                    <p className="text-xs text-muted-foreground">Total Nodos</p>
                    <p className="font-bold">{stats.total_nodes.toLocaleString()}</p>
                  </CardContent>
                </Card>
                <Card className="bg-card">
                  <CardContent className="p-3">
                    <p className="text-xs text-muted-foreground">Total Aristas</p>
                    <p className="font-bold text-emerald-500">{stats.total_edges.toLocaleString()}</p>
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase">Distribución Principal</h4>
                {stats.nodes_by_label.slice(0, 5).map((l, idx) => (
                  <div key={idx} className="flex justify-between text-sm p-1">
                    <span>{l.label}</span>
                    <span className="font-mono text-muted-foreground">{l.count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="text-center text-muted-foreground text-sm py-8 border border-dashed rounded-lg">
            Esperando datos...
          </div>
        )}
      </div>
    </div>
  );
}
