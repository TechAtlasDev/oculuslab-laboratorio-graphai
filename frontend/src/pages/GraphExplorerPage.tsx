import { useState } from 'react';
import { Sidebar } from '@/sections/graph-explorer/Sidebar';
import { GraphCanvas } from '@/sections/graph-explorer/GraphCanvas';
import { NodeDetailsPanel } from '@/sections/graph-explorer/NodeDetailsPanel';
import { fetchNeighborhood, fetchMetrics } from '@/lib/api';
import type { GraphNode, GraphEdge, MetricsResponse } from '@/lib/api';

export function GraphExplorerPage() {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const handleSearch = async (nodeId: string, limit: number) => {
    setLoading(true);
    setError(null);
    try {
      const [neighborhoodData, metricsData] = await Promise.all([
        fetchNeighborhood(nodeId, limit),
        fetchMetrics(nodeId)
      ]);

      setNodes(neighborhoodData.nodes);
      setEdges(neighborhoodData.edges);
      setMetrics(metricsData);
      setSelectedNodeId(nodeId);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch graph data. Make sure the backend is running.');
      // Create mock data for UI testing if backend fails
      setNodes([
        { id: nodeId, label: 'DRG', display_name: nodeId },
        { id: 'MOCK1', label: 'DIS', display_name: 'Diabetes' },
        { id: 'MOCK2', label: 'GEN', display_name: 'EGFR' }
      ]);
      setEdges([
        { source: nodeId, target: 'MOCK1', relation: 'INDICATION' },
        { source: 'MOCK2', target: nodeId, relation: 'TARGETS' }
      ]);
      setMetrics({
        node_id: nodeId,
        degree: 2,
        relations_count: [
          { relation: 'INDICATION', count: 1 },
          { relation: 'TARGETS', count: 1 }
        ]
      });
      setSelectedNodeId(nodeId);
    } finally {
      setLoading(false);
    }
  };

  const handleExpandNeighborhood = async (relation?: string, targetLabel?: string) => {
    if (!selectedNodeId) return;
    setLoading(true);
    try {
      const data = await fetchNeighborhood(selectedNodeId, 25, relation, targetLabel);
      
      // Append only new nodes
      setNodes(prev => {
        const newNodes = data.nodes.filter(n => !prev.some(pn => pn.id === n.id));
        return [...prev, ...newNodes];
      });
      
      // Append only new edges
      setEdges(prev => {
        const newEdges = data.edges.filter(e => !prev.some(pe => pe.source === e.source && pe.target === e.target && pe.relation === e.relation));
        return [...prev, ...newEdges];
      });
      
    } catch (err) {
      console.error(err);
      // Mock expansion if offline
      setNodes(prev => [...prev, { id: `MOCK_EXP_${Date.now()}`, label: targetLabel || 'PHE', display_name: 'Expanded Node' }]);
      setEdges(prev => [...prev, { source: selectedNodeId, target: `MOCK_EXP_${Date.now()}`, relation: relation || 'ASSOCIATED_WITH' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen w-full overflow-hidden bg-background text-foreground">
      <Sidebar onSearch={handleSearch} metrics={metrics} loading={loading} />
      
      <div className="flex-1 relative overflow-hidden">
        {error && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 bg-destructive/10 border border-destructive text-destructive px-4 py-2 rounded-md shadow-md text-sm">
            {error} (Showing mock data instead)
          </div>
        )}
        <GraphCanvas 
          apiNodes={nodes} 
          apiEdges={edges} 
          onNodeSelect={setSelectedNodeId}
        />

        {/* Right Drawer */}
        <div 
          className={`absolute top-0 right-0 h-full transition-transform duration-300 ease-in-out z-20 ${
            selectedNodeId ? 'translate-x-0' : 'translate-x-full'
          }`}
        >
          <NodeDetailsPanel 
            nodeId={selectedNodeId} 
            onClose={() => setSelectedNodeId(null)}
            onExpandNeighborhood={handleExpandNeighborhood}
          />
        </div>
      </div>
    </main>
  );
}
