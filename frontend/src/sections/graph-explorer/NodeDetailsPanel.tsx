import { useEffect, useState } from 'react';
import { X, Flask, Pill, Dna, Heartbeat, Hash, Link as LinkIcon, Info, CaretDown, CaretRight } from '@phosphor-icons/react';
import { fetchNodeDetails, fetchDrugRepurposing, type NodeDetails, type DrugRepurposingResponse, type RepurposingCandidate } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';

interface NodeDetailsPanelProps {
  nodeId: string | null;
  onClose: () => void;
  onExpandNeighborhood: (relation?: string, targetLabel?: string) => void;
  onInjectRepurposing?: (drugId: string, candidate: RepurposingCandidate) => void;
}

const LABEL_COLORS: Record<string, { bg: string, text: string, icon: React.ReactNode }> = {
  GEN: { bg: 'bg-blue-500/10', text: 'text-blue-500', icon: <Dna className="w-5 h-5" /> },
  DRG: { bg: 'bg-red-500/10', text: 'text-red-500', icon: <Pill className="w-5 h-5" /> },
  DIS: { bg: 'bg-emerald-500/10', text: 'text-emerald-500', icon: <Heartbeat className="w-5 h-5" /> },
  PHE: { bg: 'bg-amber-500/10', text: 'text-amber-500', icon: <Info className="w-5 h-5" /> },
  BPO: { bg: 'bg-violet-500/10', text: 'text-violet-500', icon: <Flask className="w-5 h-5" /> },
  MFN: { bg: 'bg-indigo-500/10', text: 'text-indigo-500', icon: <Flask className="w-5 h-5" /> },
  CCO: { bg: 'bg-purple-500/10', text: 'text-purple-500', icon: <Flask className="w-5 h-5" /> },
  ANA: { bg: 'bg-pink-500/10', text: 'text-pink-500', icon: <Heartbeat className="w-5 h-5" /> },
  PWY: { bg: 'bg-fuchsia-500/10', text: 'text-fuchsia-500', icon: <LinkIcon className="w-5 h-5" /> },
};

const DEFAULT_THEME = { bg: 'bg-slate-500/10', text: 'text-slate-500', icon: <Hash className="w-5 h-5" /> };

// Helper para detectar tipos primitivos
const isPrimitive = (val: any) => val !== Object(val);

// Renderizador Recursivo Dinámico para Objetos/Arrays Anidados
const DynamicNodeData = ({ data, level = 0 }: { data: any, level?: number }) => {
  if (data === null || data === undefined) return null;

  if (isPrimitive(data)) {
    return <span className="text-sm text-foreground/90 break-words">{String(data)}</span>;
  }

  if (Array.isArray(data)) {
    if (data.length === 0) return <span className="text-xs text-muted-foreground italic">Vacío</span>;
    
    // Lista de primitivos (ej. ["A", "B"])
    if (isPrimitive(data[0])) {
      return (
        <div className="flex flex-wrap gap-1 mt-1">
          {data.map((item, idx) => (
            <Badge key={idx} variant="secondary" className="text-[10px] bg-muted/50 font-normal">
              {String(item)}
            </Badge>
          ))}
        </div>
      );
    }

    // Lista de Objetos (ej. synonyms, hallmarks)
    return (
      <div className="space-y-2 mt-2">
        {data.map((item, idx) => (
          <div key={idx} className={`p-2 rounded-md border border-border/40 bg-background/40 space-y-1 ${level > 0 ? 'ml-2 border-l-2 border-l-primary/30' : ''}`}>
             <DynamicNodeData data={item} level={level + 1} />
          </div>
        ))}
      </div>
    );
  }

  // Objeto normal (Diccionario)
  return (
    <div className="space-y-2">
      {Object.entries(data).map(([key, value]) => {
        // Ignorar nulos o listas vacías
        if (value === null || value === undefined) return null;
        if (Array.isArray(value) && value.length === 0) return null;

        return (
          <div key={key} className="flex flex-col">
            <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider mb-0.5 flex items-center gap-1">
              <span className="w-1 h-1 rounded-full bg-primary/40 inline-block"></span>
              {key.replace(/_/g, ' ')}
            </span>
            <div className={level > 0 ? 'pl-2' : ''}>
              <DynamicNodeData data={value} level={level + 1} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Sección Acordeón personalizada para las propiedades dinámicas superiores
function ExpandableSection({ title, children, count, defaultOpen = false }: { title: string, children: React.ReactNode, count?: number, defaultOpen?: boolean }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  return (
    <div className="border border-border/40 rounded-lg bg-card/50 overflow-hidden shadow-sm transition-all">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-3 bg-muted/10 hover:bg-muted/30 transition-colors text-left"
      >
        <div className="flex items-center gap-2">
          {isOpen ? <CaretDown className="w-4 h-4 text-muted-foreground" /> : <CaretRight className="w-4 h-4 text-muted-foreground" />}
          <span className="font-medium text-sm capitalize text-foreground/90">{title.replace(/_/g, ' ')}</span>
          {count !== undefined && count > 0 && <Badge variant="outline" className="text-[10px] py-0 h-4 px-1.5 bg-background">{count}</Badge>}
        </div>
      </button>
      {isOpen && (
        <div className="p-3 border-t border-border/40 bg-background/20 max-h-96 overflow-y-auto custom-scrollbar">
          {children}
        </div>
      )}
    </div>
  );
}

export function NodeDetailsPanel({ nodeId, onClose, onExpandNeighborhood, onInjectRepurposing }: NodeDetailsPanelProps) {
  const [details, setDetails] = useState<NodeDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [repurposing, setRepurposing] = useState<DrugRepurposingResponse | null>(null);
  const [repurposingLoading, setRepurposingLoading] = useState(false);

  useEffect(() => {
    if (!nodeId) {
      setDetails(null);
      setRepurposing(null);
      return;
    }
    setRepurposing(null);

    let isMounted = true;
    setLoading(true);
    fetchNodeDetails(nodeId)
      .then(data => {
        if (isMounted) setDetails(data);
      })
      .catch(err => console.error("Failed to fetch node details", err))
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => { isMounted = false; };
  }, [nodeId]);

  const handleRepurposing = async () => {
    if (!nodeId) return;
    setRepurposingLoading(true);
    try {
      const data = await fetchDrugRepurposing(nodeId);
      setRepurposing(data);
    } catch (err) {
      console.error(err);
    } finally {
      setRepurposingLoading(false);
    }
  };

  if (!nodeId) return null;

  const theme = details ? (LABEL_COLORS[details.label] || DEFAULT_THEME) : DEFAULT_THEME;
  const properties = details?.properties as any;

  const renderDynamicAttributes = () => {
    if (!properties) return null;
    
    // Ignoramos campos que ya se muestran en el header
    const ignoredKeys = ['name', 'display_name', 'symbol', 'description', 'biotype', 'is_approved', 'type'];
    const keys = Object.keys(properties).filter(k => !ignoredKeys.includes(k) && properties[k] !== null);
    
    if (keys.length === 0) return null;

    return (
      <div className="space-y-3 mt-6">
        <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
          <Hash className="w-4 h-4 text-primary" />
          Atributos Dinámicos
        </h3>
        <div className="space-y-2">
          {keys.map(key => {
            const value = properties[key];
            if (Array.isArray(value) && value.length === 0) return null;
            if (typeof value === 'object' && value !== null && Object.keys(value).length === 0) return null;
            
            const count = Array.isArray(value) ? value.length : (typeof value === 'object' && value !== null ? Object.keys(value).length : undefined);
            
            return (
              <ExpandableSection key={key} title={key} count={count}>
                <DynamicNodeData data={value} />
              </ExpandableSection>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="absolute top-0 right-0 h-full w-[450px] bg-background/95 backdrop-blur-xl border-l border-border/50 shadow-2xl flex flex-col z-20 transition-transform duration-300">
      {/* Header */}
      <div className="p-4 border-b border-border/50 flex items-center justify-between sticky top-0 bg-background/80 backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-xl ${theme.bg} ${theme.text} shadow-inner`}>
            {theme.icon}
          </div>
          <div>
            <h2 className="font-semibold text-base leading-tight">Detalles del Nodo</h2>
            <p className="text-xs text-muted-foreground font-mono">{details?.id || nodeId}</p>
          </div>
        </div>
        <Button variant="ghost" size="icon" onClick={onClose} className="rounded-full hover:bg-muted">
          <X className="w-5 h-5" />
        </Button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
        {loading ? (
          <div className="space-y-4">
            <Skeleton className="h-8 w-3/4 rounded-lg" />
            <Skeleton className="h-4 w-1/2 rounded-md" />
            <Skeleton className="h-24 w-full rounded-xl" />
            <Skeleton className="h-10 w-full rounded-xl" />
          </div>
        ) : details ? (
          <>
            {/* Title Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className={`${theme.text} border-current bg-background shadow-sm`}>
                  {details.label}
                </Badge>
                {properties?.is_approved !== undefined && (
                  <Badge variant={properties.is_approved ? 'default' : 'secondary'} className={properties.is_approved ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' : ''}>
                    {properties.is_approved ? 'Aprobado (FDA/EMA)' : 'En Investigación'}
                  </Badge>
                )}
                {properties?.biotype && (
                  <Badge variant="secondary" className="bg-muted/50">{properties.biotype}</Badge>
                )}
              </div>
              
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-foreground leading-snug">
                  {properties?.name || details.display_name}
                </h1>
                {(properties?.symbol || properties?.type) && (
                  <p className="text-base text-muted-foreground font-medium mt-1">
                    {properties?.symbol || properties?.type}
                  </p>
                )}
              </div>
              
              {properties?.description && (
                <p className="text-sm leading-relaxed text-muted-foreground/90 bg-muted/20 p-3 rounded-lg border border-border/30">
                  {properties.description}
                </p>
              )}
            </div>

            <Separator className="bg-border/50" />

            {/* Semantic Actions */}
            <div className="space-y-3">
              <h3 className="font-semibold text-sm flex items-center gap-2">
                <LinkIcon className="w-4 h-4 text-primary" />
                Acciones Semánticas
              </h3>
              
              {details.label === 'DRG' && (
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('INDICATION', 'DIS')}>
                    <Heartbeat className="w-4 h-4 mr-2 text-emerald-500" /> Cargar Indicaciones
                  </Button>
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('TARGETS', 'GEN')}>
                    <Dna className="w-4 h-4 mr-2 text-blue-500" /> Cargar Genes Diana
                  </Button>
                </div>
              )}

              {details.label === 'GEN' && (
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('ASSOCIATED_WITH', 'DIS')}>
                    <Heartbeat className="w-4 h-4 mr-2 text-emerald-500" /> Cargar Enfermedades
                  </Button>
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('', 'PWY')}>
                    <LinkIcon className="w-4 h-4 mr-2 text-fuchsia-500" /> Cargar Vías Metabólicas
                  </Button>
                </div>
              )}

              {details.label === 'DIS' && (
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('ASSOCIATED_WITH', 'GEN')}>
                    <Dna className="w-4 h-4 mr-2 text-blue-500" /> Cargar Genes Asociados
                  </Button>
                  <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood('INDICATION', 'DRG')}>
                    <Pill className="w-4 h-4 mr-2 text-red-500" /> Cargar Fármacos Tratantes
                  </Button>
                </div>
              )}

              {/* Fallback for others */}
              {!['GEN', 'DRG', 'DIS'].includes(details.label) && (
                <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => onExpandNeighborhood()}>
                  <LinkIcon className="w-4 h-4 mr-2" /> Cargar Vecindario Completo
                </Button>
              )}
            </div>

            {/* Drug Repurposing Engine (DRG specifically) */}
            {details.label === 'DRG' && (
              <div className="space-y-3 pt-2">
                <h3 className="font-semibold text-sm flex items-center gap-2">
                  <Flask className="w-4 h-4 text-indigo-500" />
                  Motor de Reposicionamiento
                </h3>
                <Button 
                  variant="default" 
                  className="w-full justify-start bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-md border-0 transition-all" 
                  onClick={handleRepurposing}
                  disabled={repurposingLoading}
                >
                  <Flask className="w-4 h-4 mr-2" />
                  {repurposingLoading ? 'Buscando Rutas (2 Saltos)...' : 'Ejecutar Drug Repurposing'}
                </Button>

                {repurposing && (
                  <div className="mt-4 space-y-3 bg-indigo-500/5 p-4 rounded-xl border border-indigo-500/20">
                    <h4 className="text-xs font-semibold text-indigo-500 uppercase tracking-wider">Candidatos Identificados</h4>
                    {repurposing.candidates.length === 0 ? (
                      <p className="text-sm text-muted-foreground italic">No se encontraron candidatos a 2 saltos.</p>
                    ) : (
                      repurposing.candidates.map((cand, i) => (
                        <div key={i} className="bg-background/80 backdrop-blur-sm border border-border/50 rounded-lg p-3 shadow-sm space-y-2 hover:border-indigo-500/30 transition-colors">
                          <div className="flex items-start justify-between">
                            <div>
                              <p className="font-medium text-sm text-emerald-600 dark:text-emerald-400">{cand.disease.display_name || cand.disease.label}</p>
                              <p className="text-[10px] text-muted-foreground font-mono">{cand.disease.id}</p>
                            </div>
                            <Badge variant="secondary" className="text-[10px] bg-orange-500/10 text-orange-600 dark:text-orange-400 border-orange-500/20">
                              {cand.evidence_count} Vías
                            </Badge>
                          </div>
                          
                          <div className="space-y-1.5 pt-1">
                            <p className="text-[10px] text-muted-foreground uppercase font-semibold">Genes Puente (Dianas):</p>
                            <div className="flex flex-wrap gap-1">
                              {cand.intermediate_nodes.map(n => (
                                <Badge key={n.id} variant="outline" className="text-[10px] text-blue-600 dark:text-blue-400 border-blue-500/30 bg-blue-500/5 font-normal">
                                  {n.display_name || n.id}
                                </Badge>
                              ))}
                            </div>
                          </div>

                          {onInjectRepurposing && (
                            <Button variant="ghost" size="sm" className="w-full text-xs h-7 mt-2 border border-dashed border-indigo-500/30 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-500/10" onClick={() => onInjectRepurposing(nodeId, cand)}>
                              Visualizar Ruta Molecular
                            </Button>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Dynamic Attributes Render */}
            {renderDynamicAttributes()}
          </>
        ) : (
          <div className="text-center text-muted-foreground pt-10">
            Error al cargar los detalles.
          </div>
        )}
      </div>
    </div>
  );
}
