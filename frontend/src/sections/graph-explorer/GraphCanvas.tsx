import { useEffect, useRef, useState, useMemo, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import type { ForceGraphMethods, NodeObject } from 'react-force-graph-2d';
import { MagnifyingGlassPlus, MagnifyingGlassMinus, CornersOut } from '@phosphor-icons/react';
import type { GraphNode, GraphEdge } from '@/lib/api';

interface GraphCanvasProps {
  apiNodes: GraphNode[];
  apiEdges: GraphEdge[];
  onNodeSelect?: (nodeId: string) => void;
}

const LABEL_COLORS: Record<string, string> = {
  GEN: '#3b82f6',     // blue-500
  DRG: '#10b981',     // emerald-500
  DIS: '#ef4444',     // red-500
  PHE: '#f59e0b',     // amber-500
  BPO: '#8b5cf6',     // violet-500
  MFN: '#6366f1',     // indigo-500
  CCO: '#a855f7',     // purple-500
  ANA: '#ec4899',     // pink-500
  PWY: '#d946ef',     // fuchsia-500
};

const DEFAULT_COLOR = '#64748b'; // slate-500

export function GraphCanvas({ apiNodes, apiEdges, onNodeSelect }: GraphCanvasProps) {
  const fgRef = useRef<ForceGraphMethods | undefined>(undefined);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [hoverNode, setHoverNode] = useState<NodeObject | null>(null);

  // Resize observer to keep canvas full size
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  // Transform data for react-force-graph
  const graphData = useMemo(() => {
    // We pass the arrays directly. react-force-graph will mutate the objects to add x, y, vx, vy,
    // which correctly preserves their physics state across renders.
    return { nodes: apiNodes, links: apiEdges };
  }, [apiNodes, apiEdges]);

  // Configure forces when data changes
  useEffect(() => {
    const fg = fgRef.current;
    if (fg && graphData.nodes.length > 0) {
      fg.d3Force('charge')?.strength(-400); // Repel nodes more
      fg.d3Force('link')?.distance(120); // Space out links

      // Center and zoom after a slight delay ONLY if it's the first load
      if (graphData.nodes.length <= 30) {
        setTimeout(() => {
          fg.centerAt(0, 0, 1000);
          fg.zoom(1.2, 1000);
        }, 100);
      }
    }
  }, [graphData]);

  // Calculate node degrees dynamically
  const nodeDegrees = useMemo(() => {
    const degrees = new Map<string, number>();
    apiEdges.forEach(e => {
      const source: any = e.source;
      const target: any = e.target;
      const s = typeof source === 'object' ? source.id : source;
      const t = typeof target === 'object' ? target.id : target;
      if (s) degrees.set(s, (degrees.get(s) || 0) + 1);
      if (t) degrees.set(t, (degrees.get(t) || 0) + 1);
    });
    return degrees;
  }, [apiEdges]);

  // Custom node rendering for premium look
  const paintNode = useCallback((node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const label = node.display_name || node.name || node.id;
    const isHovered = node === hoverNode;
    const fontSize = 18 / globalScale; 
    
    // Uniform node size
    const r = 8; 
    const color = LABEL_COLORS[node.label] || DEFAULT_COLOR;

    // Draw glow if hovered
    if (isHovered) {
      ctx.beginPath();
      ctx.arc(node.x, node.y, r * 1.5, 0, 2 * Math.PI, false);
      ctx.fillStyle = `${color}40`; // 25% opacity
      ctx.fill();
    }

    // Draw Node Circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, 2 * Math.PI, false);
    ctx.fillStyle = color;
    ctx.fill();

    // Node Stroke
    ctx.lineWidth = isHovered ? 2 / globalScale : 1 / globalScale;
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();

    // Smooth subtle animation for text opacity based on zoom
    const textOpacity = Math.min(1, Math.max(0, (globalScale - 0.6) / 0.4));

    // Only draw text if it's visible enough OR if it's hovered
    if (textOpacity > 0 || isHovered) {
      const currentOpacity = isHovered ? 1 : textOpacity;

      // Draw Text (Name)
      ctx.font = `${isHovered ? 'bold ' : ''}${fontSize}px Inter, sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = isHovered ? '#ffffff' : `rgba(255, 255, 255, ${0.9 * currentOpacity})`;
      ctx.fillText(label, node.x, node.y + r + fontSize);

      // Draw Code (ID) as a Badge
      const codeFontSize = fontSize * 0.85; 
      ctx.font = `${codeFontSize}px monospace`;
      const textWidth = ctx.measureText(node.id).width;
      const badgeWidth = textWidth + 12 / globalScale; 
      const badgeHeight = codeFontSize + 6 / globalScale;
      const badgeY = node.y + r + fontSize + 6 / globalScale;

      // Badge Background
      ctx.fillStyle = isHovered ? color : `rgba(255, 255, 255, ${0.95 * currentOpacity})`;
      ctx.beginPath();
      ctx.roundRect(node.x - badgeWidth / 2, badgeY, badgeWidth, badgeHeight, 4 / globalScale);
      ctx.fill();

      // Badge Text
      ctx.fillStyle = isHovered ? '#ffffff' : `rgba(0, 0, 0, ${currentOpacity})`;
      ctx.fillText(node.id, node.x, badgeY + badgeHeight / 2);
    }
  }, [hoverNode, nodeDegrees]);

  // Edge text drawing
  const paintLink = useCallback((link: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
    // Smooth fade for edge text
    const textOpacity = Math.min(1, Math.max(0, (globalScale - 0.6) / 0.4));
    if (textOpacity <= 0) return;
    
    const start = link.source;
    const end = link.target;
    if (!start || !end || typeof start !== 'object' || typeof end !== 'object') return;

    const rel = link.relation;
    if (!rel) return;

    const textPos = {
      x: start.x + (end.x - start.x) / 2,
      y: start.y + (end.y - start.y) / 2
    };

    // Make text same relative size as node names
    const fontSize = 14 / globalScale;
    ctx.font = `${fontSize}px Inter, sans-serif`;
    
    ctx.save();
    ctx.translate(textPos.x, textPos.y);
    
    // Rotate text to align with line
    const angle = Math.atan2(end.y - start.y, end.x - start.x);
    if (angle > Math.PI / 2 || angle < -Math.PI / 2) {
      ctx.rotate(angle + Math.PI);
    } else {
      ctx.rotate(angle);
    }

    // Draw solid capsule background for edge text
    const textWidth = ctx.measureText(rel).width;
    const paddingX = 8 / globalScale;
    const paddingY = 4 / globalScale;
    
    ctx.fillStyle = `rgba(15, 23, 42, ${0.85 * textOpacity})`; // Dark slate background
    ctx.beginPath();
    ctx.roundRect(-textWidth / 2 - paddingX / 2, -fontSize / 2 - paddingY / 2, textWidth + paddingX, fontSize + paddingY, 4 / globalScale);
    ctx.fill();

    // Fill text
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = `rgba(255, 255, 255, ${textOpacity})`; 
    ctx.fillText(rel, 0, 0);
    
    ctx.restore();
  }, []);

  return (
    <div
      ref={containerRef}
      className="w-full h-full relative overflow-hidden"
      style={{
        backgroundColor: 'hsl(var(--background))',
        backgroundImage: 'radial-gradient(hsl(var(--foreground)/0.1) 1px, transparent 1px)',
        backgroundSize: '30px 30px',
        cursor: hoverNode ? 'pointer' : 'grab'
      }}
    >
      {/* Subtle background glow */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_center,_hsl(var(--primary)/0.15)_0%,_transparent_70%)]" />

      {graphData.nodes.length > 0 && (
        <ForceGraph2D
          ref={fgRef}
          width={dimensions.width}
          height={dimensions.height}
          minZoom={0.2}
          maxZoom={10}
          graphData={graphData}
          nodeLabel={(node: any) => `<div style="background:#000;border:1px solid #333;padding:4px 8px;border-radius:4px;font-size:12px;color:#fff;">
            <strong>${node.display_name || node.name || node.id}</strong><br/>
            <span style="color:#aaa;font-size:10px;">${node.label}</span>
          </div>`}
          nodeColor={(node: any) => LABEL_COLORS[node.label] || DEFAULT_COLOR}
          nodeRelSize={6}
          nodeCanvasObject={paintNode}
          nodeCanvasObjectMode={() => 'replace'}

          // Edge styles
          linkCanvasObject={paintLink}
          linkCanvasObjectMode={() => 'after'}
          linkColor={() => 'rgba(100, 116, 139, 0.4)'} // Slate 500 with opacity to be visible in light mode too
          linkWidth={(link) => (hoverNode && (link.source === hoverNode || link.target === hoverNode) ? 2 : 1)}
          linkDirectionalParticles={2}
          linkDirectionalParticleWidth={1.5}
          linkDirectionalParticleSpeed={0.005}
          linkDirectionalParticleColor={(link: any) => {
            const sourceColor = LABEL_COLORS[link.source.label] || DEFAULT_COLOR;
            return sourceColor; // Particle takes color of source node
          }}

          // Interactions
          onNodeHover={setHoverNode}
          onNodeClick={(node: any) => {
            const fg = fgRef.current;
            if (fg) {
              fg.centerAt(node.x, node.y, 1000);
              fg.zoom(2, 1000);
            }
            if (onNodeSelect) {
              onNodeSelect(node.id);
            }
          }}
          onNodeDragEnd={(node: any) => {
            // Pin node position after dragging
            node.fx = node.x;
            node.fy = node.y;
          }}

          // Smooth physics
          d3AlphaDecay={0.02}
          d3VelocityDecay={0.3}
          cooldownTicks={100}

          // Render Minimap
          onRenderFramePost={(ctx) => {
            const mapWidth = 150;
            const mapHeight = 100;
            const margin = 20;
            const mapX = dimensions.width - mapWidth - margin;
            const mapY = dimensions.height - mapHeight - margin;

            // Draw Minimap Background
            ctx.save();
            ctx.resetTransform(); // Use screen coordinates
            ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.roundRect(mapX, mapY, mapWidth, mapHeight, 8);
            ctx.fill();
            ctx.stroke();

            // Find bounds of nodes
            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            graphData.nodes.forEach((node: any) => {
              const n = node;
              if (n.x !== undefined && n.y !== undefined) {
                if (n.x < minX) minX = n.x;
                if (n.x > maxX) maxX = n.x;
                if (n.y < minY) minY = n.y;
                if (n.y > maxY) maxY = n.y;
              }
            });

            // Add padding to bounds
            const padding = 50;
            minX -= padding; maxX += padding;
            minY -= padding; maxY += padding;

            const graphWidth = Math.max(maxX - minX, 1);
            const graphHeight = Math.max(maxY - minY, 1);
            const scale = Math.min(mapWidth / graphWidth, mapHeight / graphHeight) * 0.8;

            const offsetX = mapX + mapWidth / 2 - ((maxX + minX) / 2) * scale;
            const offsetY = mapY + mapHeight / 2 - ((maxY + minY) / 2) * scale;

            // Draw Nodes on Minimap
            graphData.nodes.forEach((node: any) => {
              const n = node;
              if (n.x !== undefined && n.y !== undefined) {
                ctx.beginPath();
                ctx.arc(n.x * scale + offsetX, n.y * scale + offsetY, 1.5, 0, 2 * Math.PI);
                ctx.fillStyle = LABEL_COLORS[n.label] || DEFAULT_COLOR;
                ctx.fill();
              }
            });
            ctx.restore();
          }}
        />
      )}

      {graphData.nodes.length > 0 && (
        <div className="absolute bottom-6 left-6 flex flex-col gap-2 z-10">
          <button
            className="p-2 bg-background/80 backdrop-blur border rounded-md hover:bg-muted text-foreground transition-colors shadow-sm"
            onClick={() => {
              const fg = fgRef.current;
              if (fg) {
                const currentZoom = fg.zoom();
                fg.zoom(currentZoom * 1.5, 400);
              }
            }}
            title="Zoom In"
          >
            <MagnifyingGlassPlus className="w-5 h-5" />
          </button>
          <button
            className="p-2 bg-background/80 backdrop-blur border rounded-md hover:bg-muted text-foreground transition-colors shadow-sm"
            onClick={() => {
              const fg = fgRef.current;
              if (fg) {
                const currentZoom = fg.zoom();
                fg.zoom(currentZoom / 1.5, 400);
              }
            }}
            title="Zoom Out"
          >
            <MagnifyingGlassMinus className="w-5 h-5" />
          </button>
          <button
            className="p-2 bg-background/80 backdrop-blur border rounded-md hover:bg-muted text-foreground transition-colors shadow-sm"
            onClick={() => {
              const fg = fgRef.current;
              if (fg) {
                fg.centerAt(0, 0, 800);
                fg.zoom(1.2, 800);
              }
            }}
            title="Centrar Grafo"
          >
            <CornersOut className="w-5 h-5" />
          </button>
        </div>
      )}

      {graphData.nodes.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
          Realiza una búsqueda para visualizar el grafo.
        </div>
      )}
    </div>
  );
}
