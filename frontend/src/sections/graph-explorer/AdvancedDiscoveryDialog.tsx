import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogTrigger } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { MagnifyingGlass, Dna, Pill, Heartbeat, RocketLaunch } from '@phosphor-icons/react';
import { fetchDiscoveryNodes, type DiscoveryParams, type GraphNode } from '@/lib/api';

interface AdvancedDiscoveryDialogProps {
  onInjectNodes: (nodes: GraphNode[]) => void;
}

export function AdvancedDiscoveryDialog({ onInjectNodes }: AdvancedDiscoveryDialogProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<GraphNode[]>([]);
  const [total, setTotal] = useState(0);

  // Form States
  const [activeTab, setActiveTab] = useState('GEN');
  
  // GEN
  const [biotype, setBiotype] = useState('');
  const [chromosome, setChromosome] = useState('');
  
  // DRG
  const [isApproved, setIsApproved] = useState(false);
  const [maxPhase, setMaxPhase] = useState([4]);

  // DIS
  const [therapeuticArea, setTherapeuticArea] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    try {
      const params: DiscoveryParams = { label: activeTab, limit: 50 };
      if (activeTab === 'GEN') {
        if (biotype) params.biotype = biotype;
        if (chromosome) params.chromosome = chromosome;
      } else if (activeTab === 'DRG') {
        params.is_approved = isApproved;
        params.max_phase = maxPhase[0];
      } else if (activeTab === 'DIS') {
        if (therapeuticArea) params.therapeutic_area = therapeuticArea;
      }
      
      const res = await fetchDiscoveryNodes(params);
      setResults(res.items);
      setTotal(res.total);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleInject = () => {
    onInjectNodes(results);
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <div className="w-full justify-start border border-indigo-500/30 hover:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 bg-background flex items-center h-10 px-4 py-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background">
          <MagnifyingGlass className="mr-2 h-4 w-4" />
          Filtros de Descubrimiento
        </div>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Motor de Descubrimiento Global</DialogTitle>
          <DialogDescription>
            Busca cohortes completas de entidades biológicas utilizando filtros avanzados.
          </DialogDescription>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={(val) => { setActiveTab(val); setResults([]); }} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="GEN" className="flex items-center gap-1"><Dna size={16}/> Genes</TabsTrigger>
            <TabsTrigger value="DRG" className="flex items-center gap-1"><Pill size={16}/> Drogas</TabsTrigger>
            <TabsTrigger value="DIS" className="flex items-center gap-1"><Heartbeat size={16}/> Enf.</TabsTrigger>
          </TabsList>
          
          <div className="py-4 space-y-4">
            <TabsContent value="GEN" className="space-y-4 mt-0">
              <div className="space-y-2">
                <Label>Biotipo</Label>
                <Select value={biotype} onValueChange={(val) => setBiotype(val || '')}>
                  <SelectTrigger>
                    <SelectValue placeholder="Ej. protein_coding" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="protein_coding">protein_coding</SelectItem>
                    <SelectItem value="lncRNA">lncRNA</SelectItem>
                    <SelectItem value="miRNA">miRNA</SelectItem>
                    <SelectItem value="snRNA">snRNA</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Cromosoma</Label>
                <Input placeholder="Ej. 21, X, Y" value={chromosome} onChange={(e) => setChromosome(e.target.value)} />
              </div>
            </TabsContent>

            <TabsContent value="DRG" className="space-y-4 mt-0">
              <div className="flex items-center justify-between">
                <Label>Aprobado por FDA/EMA</Label>
                <Switch checked={isApproved} onCheckedChange={setIsApproved} />
              </div>
              <div className="space-y-4 pt-4">
                <div className="flex justify-between">
                  <Label>Fase Clínica Máxima</Label>
                  <span className="text-sm text-muted-foreground">Fase {maxPhase[0]}</span>
                </div>
                <Slider value={maxPhase} onValueChange={(val) => setMaxPhase(Array.isArray(val) ? val as number[] : [val as number])} max={4} min={0} step={1} />
              </div>
            </TabsContent>

            <TabsContent value="DIS" className="space-y-4 mt-0">
              <div className="space-y-2">
                <Label>Área Terapéutica</Label>
                <Input placeholder="Ej. oncology, cardiovascular" value={therapeuticArea} onChange={(e) => setTherapeuticArea(e.target.value)} />
              </div>
            </TabsContent>
          </div>
        </Tabs>

        <div className="flex flex-col gap-4">
          <Button onClick={handleSearch} disabled={loading} className="w-full">
            {loading ? 'Buscando...' : 'Buscar Entidades'}
          </Button>

          {results.length > 0 && (
            <div className="bg-muted/50 rounded-lg p-4 border space-y-3">
              <p className="text-sm font-medium text-center">
                Se encontraron {total} entidades. (Mostrando top {results.length})
              </p>
              <Button onClick={handleInject} variant="default" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
                <RocketLaunch className="mr-2 h-4 w-4" />
                Inyectar Cohorte al Grafo
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
