export interface GraphNode {
  id: string;
  label: string;
  display_name: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
}

export interface NeighborhoodResponse {
  node_id: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface RelationCount {
  relation: string;
  count: number;
}

export interface MetricsResponse {
  node_id: string;
  degree: number;
  relations_count: RelationCount[];
}

export interface GraphStats {
  total_nodes: number;
  total_edges: number;
  nodes_by_label: { label: string; count: number }[];
  edges_by_relation: { relation: string; count: number }[];
}

export interface SearchResponse {
  items: GraphNode[];
  total: number;
}

export interface NodeDetails extends GraphNode {
  properties: Record<string, any>;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function fetchStats(): Promise<GraphStats> {
  const response = await fetch(`${API_BASE_URL}/graph/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}

export async function searchNodes(q: string, label?: string, limit: number = 20): Promise<SearchResponse> {
  const url = new URL(`${API_BASE_URL}/graph/nodes/search`);
  url.searchParams.append('q', q);
  url.searchParams.append('limit', limit.toString());
  if (label) url.searchParams.append('label', label);
  
  const response = await fetch(url.toString());
  if (!response.ok) throw new Error('Failed to search nodes');
  return response.json();
}

export async function fetchNodeDetails(nodeId: string): Promise<NodeDetails> {
  const response = await fetch(`${API_BASE_URL}/graph/nodes/${nodeId}`);
  if (!response.ok) throw new Error('Failed to fetch node details');
  return response.json();
}

export async function fetchNeighborhood(
  nodeId: string, 
  limit: number = 15,
  relation?: string,
  target_label?: string
): Promise<NeighborhoodResponse> {
  const url = new URL(`${API_BASE_URL}/graph/nodes/${nodeId}/neighborhood`);
  url.searchParams.append('limit', limit.toString());
  if (relation) url.searchParams.append('relation', relation);
  if (target_label) url.searchParams.append('target_label', target_label);
  
  const response = await fetch(url.toString());
  if (!response.ok) throw new Error('Failed to fetch neighborhood');
  return response.json();
}

export async function fetchMetrics(nodeId: string): Promise<MetricsResponse> {
  const response = await fetch(`${API_BASE_URL}/graph/nodes/${nodeId}/metrics`);
  if (!response.ok) {
    throw new Error('Failed to fetch metrics');
  }
  return response.json();
}
