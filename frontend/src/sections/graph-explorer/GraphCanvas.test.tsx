import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { GraphCanvas } from './GraphCanvas';
import type { GraphNode, GraphEdge } from '@/lib/api';

// Mock ResizeObserver
class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}
window.ResizeObserver = ResizeObserverMock as any;

describe('GraphCanvas', () => {
  const mockNodes: GraphNode[] = [
    { id: '1', label: 'GEN', display_name: 'Gene1' },
    { id: '2', label: 'DRG', display_name: 'Drug1' },
  ];

  const mockEdges: GraphEdge[] = [
    { source: '1', target: '2', relation: 'TARGETS' },
  ];

  it('renders the graph canvas svg container successfully', () => {
    const { container } = render(
      <GraphCanvas apiNodes={mockNodes} apiEdges={mockEdges} />
    );

    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
  });
});
