export interface GeneProperties {
  symbol?: string;
  name?: any;
  biotype?: any;
  sources?: any;
  transcript_ids?: any;
  canonical_transcript?: any;
  canonical_exons?: any;
  genomic_location?: any;
  alternative_genes?: any;
  synonyms?: any;
  symbol_synonyms?: any;
  name_synonyms?: any;
  obsolete_symbols?: any;
  obsolete_names?: any;
  associated_proteins?: any;
  xrefs?: any;
  homologues?: any;
  tractability?: any;
  constraint_scores?: any;
  subcellular_locations?: any;
  target_enabling_package?: any;
  hallmarks_attributes?: any;
  cancer_hallmarks?: any;
  chemical_probes?: any;
  safety_liabilities?: any;
  target_class?: any;
  function_descriptions?: any;
  transcription_start_site?: any;
}

export interface DrugProperties {
  name?: any;
  inchi_key?: any;
  type?: any;
  synonyms?: any;
  description?: any;
  accession_numbers?: any;
  canonical_smiles?: any;
  chemical_abstracts_service_number?: any;
  unique_ingredient_identifier?: any;
  black_box_warning?: any;
  year_of_first_approval?: any;
  maximum_clinical_trial_phase?: any;
  has_been_withdrawn?: any;
  is_approved?: any;
  trade_names?: any;
  sources?: any;
  source_ids?: any;
  cd_id?: any;
  cd_formula?: any;
  cd_mol_weight?: any;
  calculated_log_p?: any;
  alogs?: any;
  tpsa?: any;
  lipinski?: any;
  number_of_formulations?: any;
  mol_file_base64?: any;
  mol_image_base64?: any;
  mrdef?: any;
  enhanced_stereo?: any;
  aromatic_carbons?: any;
  sp3_count?: any;
  sp2_count?: any;
  sp_count?: any;
  halogen_count?: any;
  hetero_sp2_count?: any;
  rotatable_bonds?: any;
  o_n?: any;
  oh_nh?: any;
  inchi?: any;
  rgb?: any;
  fda_labels?: any;
  status?: any;
  struct_id?: any;
}

export interface DiseaseProperties {
  name?: string;
  description?: any;
  code?: any;
  umls_cui?: any;
  cui_semantic_type?: any;
  parents?: any;
  children?: any;
  ancestors?: any;
  descendants?: any;
  therapeutic_areas?: any;
  is_leaf?: any;
  exact_synonyms?: any;
  related_synonyms?: any;
  narrow_synonyms?: any;
  broad_synonyms?: any;
  xrefs?: any;
  obsolete_terms?: any;
  obsolete_xrefs?: any;
  concept_ids?: any;
  concept_names?: any;
  snomed_full_names?: any;
  snomed_concept_ids?: any;
  sources?: any;
}

export interface PharmacologicalProperties {
  source_ids?: any;
  source_urls?: any;
  mechanisms_of_action?: any;
  sources?: any;
}

export interface ClinicalProperties {
  highest_clinical_trial_phase?: any;
  reference_ids?: any;
  sources?: any;
  structure_id?: any;
  drug_disease_id?: any;
}

export interface AssociationProperties {
  evidence_score?: any;
  evidence_count?: any;
  disgenet_score?: any;
  disease_specificity_index?: any;
  disease_pleiotropy_index?: any;
  evidence_index?: any;
  year_initial?: any;
  year_final?: any;
  sources?: any;
}

export interface BaseNode {
  id: string;
  display_name: string;
}

export interface GeneNode extends BaseNode {
  label: 'GEN';
  properties?: GeneProperties;
}

export interface DrugNode extends BaseNode {
  label: 'DRG';
  properties?: DrugProperties;
}

export interface DiseaseNode extends BaseNode {
  label: 'DIS';
  properties?: DiseaseProperties;
}

export interface GenericNode extends BaseNode {
  label: string;
  properties?: Record<string, any>;
}

export type GraphNode = GeneNode | DrugNode | DiseaseNode | GenericNode;

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
  properties?: PharmacologicalProperties | ClinicalProperties | AssociationProperties | Record<string, any>;
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

export type NodeDetails = GraphNode;

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
  
  const data = await response.json();
  
  // Transform 'from' and 'to' from the backend into 'source' and 'target'
  if (data.edges) {
    data.edges = data.edges.map((e: any) => ({
      ...e,
      source: e.from || e.source,
      target: e.to || e.target
    }));
  }
  
  return data;
}

export async function fetchMetrics(nodeId: string): Promise<MetricsResponse> {
  const response = await fetch(`${API_BASE_URL}/graph/nodes/${nodeId}/metrics`);
  if (!response.ok) {
    throw new Error('Failed to fetch metrics');
  }
  return response.json();
}

export interface RepurposingCandidate {
  disease: {
    id: string;
    label: string;
    display_name: string;
  };
  intermediate_nodes: {
    id: string;
    label: string;
    display_name: string;
  }[];
  evidence_count: number;
}

export interface DrugRepurposingResponse {
  drug_id: string;
  candidates: RepurposingCandidate[];
}

export async function fetchDrugRepurposing(drugId: string, limit: number = 10): Promise<DrugRepurposingResponse> {
  const url = new URL(`${API_BASE_URL}/analysis/repurpose/drug/${drugId}`);
  url.searchParams.append('limit', limit.toString());
  
  const response = await fetch(url.toString());
  if (!response.ok) throw new Error('Failed to fetch drug repurposing candidates');
  return response.json();
}

export interface DiscoveryParams {
  label?: string;
  biotype?: string;
  chromosome?: string;
  is_approved?: boolean;
  max_phase?: number;
  therapeutic_area?: string;
  limit?: number;
}

export interface DiscoveryResponse {
  items: GraphNode[];
  total: number;
}

export async function fetchDiscoveryNodes(params: DiscoveryParams): Promise<DiscoveryResponse> {
  const url = new URL(`${API_BASE_URL}/graph/discovery/nodes`);
  if (params.label) url.searchParams.append('label', params.label);
  if (params.biotype) url.searchParams.append('biotype', params.biotype);
  if (params.chromosome) url.searchParams.append('chromosome', params.chromosome);
  if (params.is_approved !== undefined) url.searchParams.append('is_approved', params.is_approved.toString());
  if (params.max_phase !== undefined) url.searchParams.append('max_phase', params.max_phase.toString());
  if (params.therapeutic_area) url.searchParams.append('therapeutic_area', params.therapeutic_area);
  if (params.limit) url.searchParams.append('limit', params.limit.toString());

  const response = await fetch(url.toString());
  if (!response.ok) throw new Error('Failed to fetch discovery nodes');
  return response.json();
}
