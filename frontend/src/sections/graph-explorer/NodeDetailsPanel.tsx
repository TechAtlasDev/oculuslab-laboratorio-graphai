import { useEffect, useState } from 'react';
import { X, Flask, Pill, Dna, Heartbeat, Hash, Link as LinkIcon, Info } from '@phosphor-icons/react';
import { fetchNodeDetails, type NodeDetails } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';

interface NodeDetailsPanelProps {
  nodeId: string | null;
  onClose: () => void;
  onExpandNeighborhood: (relation?: string, targetLabel?: string) => void;
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

export function NodeDetailsPanel({ nodeId, onClose, onExpandNeighborhood }: NodeDetailsPanelProps) {
  const [details, setDetails] = useState<NodeDetails | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!nodeId) {
      setDetails(null);
      return;
    }

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

  if (!nodeId) return null;

  const theme = details ? (LABEL_COLORS[details.label] || DEFAULT_THEME) : DEFAULT_THEME;

  return (
    <div className="absolute top-0 right-0 h-full w-96 bg-background/95 backdrop-blur border-l shadow-2xl flex flex-col z-20 transition-transform duration-300">
      {/* Header */}
      <div className="p-4 border-b flex items-center justify-between sticky top-0 bg-background/80 backdrop-blur z-10">
        <div className="flex items-center gap-2">
          <div className={`p-2 rounded-md ${theme.bg} ${theme.text}`}>
            {theme.icon}
          </div>
          <h2 className="font-semibold text-lg">Detalles del Nodo</h2>
        </div>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="w-5 h-5" />
        </Button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {loading ? (
          <div className="space-y-4">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-10 w-full" />
          </div>
        ) : details ? (
          <>
            {/* Title Section */}
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="outline" className={`${theme.text} border-current`}>
                  {details.label}
                </Badge>
                <span className="text-xs text-muted-foreground font-mono bg-muted px-2 py-1 rounded">
                  {details.id}
                </span>
              </div>
              <h1 className="text-2xl font-bold tracking-tight mb-1">
                {details.properties?.name || details.display_name}
              </h1>
              {details.properties?.symbol && (
                <p className="text-lg text-muted-foreground">{details.properties.symbol}</p>
              )}
            </div>

            <Separator />

            {/* Entity Specific Properties */}
            {details.label === 'DRG' && (
              <div className="space-y-4">
                {details.properties.is_approved !== undefined && (
                  <div>
                    <Badge variant={details.properties.is_approved ? 'default' : 'secondary'} className={details.properties.is_approved ? 'bg-emerald-500' : ''}>
                      {details.properties.is_approved ? 'Aprobado (FDA/EMA)' : 'En Investigación'}
                    </Badge>
                  </div>
                )}
                {details.properties.type && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Tipo de Molécula</span>
                    <p className="font-medium">{details.properties.type}</p>
                  </div>
                )}
                {details.properties.description && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Descripción</span>
                    <p className="text-sm leading-relaxed text-muted-foreground">{details.properties.description}</p>
                  </div>
                )}
                
                <div className="pt-4 space-y-2">
                  <h3 className="font-semibold text-sm">Acciones Semánticas</h3>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('INDICATION', 'DIS')}>
                    <Heartbeat className="w-4 h-4 mr-2 text-emerald-500" />
                    Cargar Indicaciones (Enfermedades)
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('TARGETS', 'GEN')}>
                    <Dna className="w-4 h-4 mr-2 text-blue-500" />
                    Cargar Genes Diana (Targets)
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('SYNERGISTIC_INTERACTION', 'DRG')}>
                    <Pill className="w-4 h-4 mr-2 text-red-500" />
                    Cargar Drogas Sinérgicas
                  </Button>
                </div>
              </div>
            )}

            {details.label === 'GEN' && (
              <div className="space-y-4">
                {details.properties.biotype && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Biotipo</span>
                    <Badge variant="secondary">{details.properties.biotype}</Badge>
                  </div>
                )}
                {details.properties.canonical_transcript && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Locus (Transcrito Canónico)</span>
                    <p className="text-sm font-mono bg-muted p-2 rounded">
                      Chr {details.properties.canonical_transcript.chromosome}: 
                      {details.properties.canonical_transcript.start} - {details.properties.canonical_transcript.end}
                    </p>
                  </div>
                )}

                <div className="pt-4 space-y-2">
                  <h3 className="font-semibold text-sm">Acciones Semánticas</h3>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('ASSOCIATED_WITH', 'DIS')}>
                    <Heartbeat className="w-4 h-4 mr-2 text-emerald-500" />
                    Cargar Enfermedades Asociadas
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('EXPRESSION_PRESENT', 'ANA')}>
                    <Info className="w-4 h-4 mr-2 text-pink-500" />
                    Cargar Tejidos de Expresión
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('', 'PWY')}>
                    <LinkIcon className="w-4 h-4 mr-2 text-fuchsia-500" />
                    Cargar Vías Metabólicas
                  </Button>
                </div>
              </div>
            )}

            {details.label === 'DIS' && (
              <div className="space-y-4">
                {details.properties.description && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Descripción Clínica</span>
                    <p className="text-sm leading-relaxed text-muted-foreground">{details.properties.description}</p>
                  </div>
                )}
                {details.properties.therapeutic_areas && details.properties.therapeutic_areas.length > 0 && (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-2">Áreas Terapéuticas</span>
                    <div className="flex flex-wrap gap-2">
                      {details.properties.therapeutic_areas.map((area: string, i: number) => (
                        <Badge key={i} variant="secondary">{area}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div className="pt-4 space-y-2">
                  <h3 className="font-semibold text-sm">Acciones Semánticas</h3>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('ASSOCIATED_WITH', 'GEN')}>
                    <Dna className="w-4 h-4 mr-2 text-blue-500" />
                    Cargar Genes Asociados
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('INDICATION', 'DRG')}>
                    <Pill className="w-4 h-4 mr-2 text-red-500" />
                    Cargar Fármacos Tratantes
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood('PHENOTYPE_PRESENT', 'PHE')}>
                    <Info className="w-4 h-4 mr-2 text-amber-500" />
                    Cargar Fenotipos
                  </Button>
                </div>
              </div>
            )}

            {/* Fallback for other entities */}
            {!['GEN', 'DRG', 'DIS'].includes(details.label) && (
              <div className="space-y-4">
                {details.properties.description || details.properties.definition ? (
                  <div>
                    <span className="text-sm text-muted-foreground block mb-1">Descripción</span>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                      {details.properties.description || details.properties.definition}
                    </p>
                  </div>
                ) : null}

                <div className="pt-4 space-y-2">
                  <h3 className="font-semibold text-sm">Acciones Semánticas</h3>
                  <Button variant="outline" className="w-full justify-start" onClick={() => onExpandNeighborhood()}>
                    <LinkIcon className="w-4 h-4 mr-2" />
                    Cargar Vecindario Completo
                  </Button>
                </div>
              </div>
            )}

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
