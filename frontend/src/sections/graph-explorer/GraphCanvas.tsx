import { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import type { GraphNode, GraphEdge } from '@/lib/api';

interface GraphCanvasProps {
  apiNodes: GraphNode[];
  apiEdges: GraphEdge[];
  onNodeSelect?: (nodeId: string) => void;
  onEdgeSelect?: (edge: GraphEdge) => void;
}

const COLORS: Record<string, string> = {
  GEN: '#3B82F6', // Blue
  DRG: '#10B981', // Emerald
  DIS: '#F43F5E', // Rose
  PHE: '#F59E0B', // Amber
  BPO: '#8B5CF6', // Violet
  MFN: '#6366F1', // Indigo
  CCO: '#A855F7', // Purple
  ANA: '#EC4899', // Pink
  PWY: '#D946EF', // Fuchsia
  DEFAULT: '#94A3B8' // Slate
};

const RELATION_COLORS: Record<string, string> = {
  TARGETS: '#F43F5E', // Rose
  ASSOCIATED_WITH: '#3B82F6', // Blue
  EXPRESSION_PRESENT: '#10B981', // Emerald
  INTERACTS_WITH: '#F59E0B', // Amber
  INDICATION: '#8B5CF6', // Violet
  DEFAULT: '#94A3B8' // Slate
};

function getNodeColor(label: string): string {
  if (!label) return COLORS.DEFAULT;
  // Handle compound labels like "ANA-GEN" by checking if any key is in the label
  const foundKey = Object.keys(COLORS).find(key => label.includes(key));
  return foundKey ? COLORS[foundKey] : COLORS.DEFAULT;
}

export function GraphCanvas({ apiNodes, apiEdges, onNodeSelect, onEdgeSelect }: GraphCanvasProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  
  // Use refs to store latest callbacks to prevent infinite re-renders
  const onNodeSelectRef = useRef(onNodeSelect);
  const onEdgeSelectRef = useRef(onEdgeSelect);

  useEffect(() => {
    onNodeSelectRef.current = onNodeSelect;
    onEdgeSelectRef.current = onEdgeSelect;
  }, [onNodeSelect, onEdgeSelect]);

  // Handle Resize of the canvas wrapper
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      if (entries[0]) {
        setDimensions({
          width: entries[0].contentRect.width,
          height: entries[0].contentRect.height
        });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Main D3 Rendering (100% native exactly as the D3 documentation)
  useEffect(() => {
    if (!svgRef.current || apiNodes.length === 0) return;

    const width = dimensions.width;
    const height = dimensions.height;

    // Deep copy data to prevent D3 from mutating React props directly
    const nodes = apiNodes.map(d => ({ ...d }));
    
    // Filter valid links so d3 doesn't crash if an edge references a missing node
    const nodeIds = new Set(nodes.map(n => n.id));
    const links = apiEdges
      .filter(d => nodeIds.has(d.source) && nodeIds.has(d.target))
      .map(d => ({ ...d }));

    // Select the SVG and clear previous render
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Create a container group for zooming and panning
    const g = svg.append('g');

    // Add Zoom Behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });
    
    svg.call(zoom);

    // Initialize Force Simulation exactly like the official D3 docs
    const simulation = d3.forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink(links).id((d: any) => d.id).distance(150)) // Increased distance
      .force('charge', d3.forceManyBody().strength(-800)) // Increased repulsion
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide().radius(60)); // Increased collision radius

    // Define Arrow markers for directed edges per color
    const defs = svg.append("defs");
    Object.entries(RELATION_COLORS).forEach(([relation, color]) => {
      defs.append("marker")
        .attr("id", `arrowhead-${relation}`)
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 32) // Offset slightly more so the smaller arrow doesn't hide
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 5) // Reduced marker size
        .attr("markerHeight", 5) // Reduced marker size
        .attr("xoverflow", "visible")
        .append("svg:path")
        .attr("d", "M 0,-3.5 L 7 ,0 L 0,3.5") // Slimmer arrow path
        .attr("fill", color)
        .style("stroke", "none");
    });

    // Add links (edges)
    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', (d: any) => RELATION_COLORS[d.relation] || RELATION_COLORS.DEFAULT)
      .attr('stroke-width', 2) // Reduced line thickness so arrows scale down proportionately
      .attr('marker-end', (d: any) => `url(#arrowhead-${RELATION_COLORS[d.relation] ? d.relation : 'DEFAULT'})`)
      .style('cursor', 'pointer')
      .on('click', (_event, d: any) => {
        if (onEdgeSelectRef.current) onEdgeSelectRef.current(d);
      });

    // Add nodes
    const node = g.append('g')
      .attr('stroke', 'currentColor')
      .attr('class', 'text-background')
      .attr('stroke-width', 3)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 18)
      .attr('fill', (d: any) => getNodeColor(d.label))
      .style('cursor', 'pointer')
      .call(d3.drag<any, any>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended) as any
      )
      .on('click', (_event, d: any) => {
        if (onNodeSelectRef.current) onNodeSelectRef.current(d.id);
      });

    // Tooltip titles (only shown on hover to save massive rendering overhead)
    node.append('title')
      .text((d: any) => `${d.label}: ${d.display_name}`);

    // Tick function to update positions
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);
    });

    // Drag behavior precisely as in D3 documentation
    function dragstarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    // Cleanup simulation on unmount
    return () => {
      simulation.stop();
    };
  }, [apiNodes, apiEdges, dimensions]); // REMOVED callbacks from dependencies!

  return (
    <div ref={containerRef} className="w-full h-full bg-background overflow-hidden rounded-xl">
      <svg ref={svgRef} className="w-full h-full" />
    </div>
  );
}
