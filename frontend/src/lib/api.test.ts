import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchNeighborhood, fetchMetrics } from './api';

// Mock global fetch
globalThis.fetch = vi.fn();

describe('API Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetchNeighborhood should call the correct endpoint and return data', async () => {
    const mockData = { node_id: 'test', nodes: [], edges: [] };
    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await fetchNeighborhood('test', 10);
    
    expect(globalThis.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/graph/nodes/test/neighborhood?limit=10');
    expect(result).toEqual(mockData);
  });

  it('fetchMetrics should call the correct endpoint and return data', async () => {
    const mockData = { node_id: 'test', degree: 5, relations_count: [] };
    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await fetchMetrics('test');
    
    expect(globalThis.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/graph/nodes/test/metrics');
    expect(result).toEqual(mockData);
  });
});
