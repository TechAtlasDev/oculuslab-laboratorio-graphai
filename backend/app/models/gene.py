from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union

class GeneSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class CanonicalTranscript(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    chromosome: str
    start: int
    end: int
    strand: str

class GenomicLocation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    chromosome: str
    start: int
    end: int
    strand: int

class LabelSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    label: str
    source: str

class SubcellularLocation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    location: str
    source: str
    term_sl: Optional[str] = None
    label_sl: Optional[str] = None

class ConstraintScore(BaseModel):
    model_config = ConfigDict(extra='forbid')
    constraint_type: str
    score: Optional[float] = None
    exp: Optional[float] = None
    obs: Optional[int] = None
    oe: Optional[float] = None
    oe_lower: Optional[float] = None
    oe_upper: Optional[float] = None
    upper_rank: Optional[Union[int, float]] = None
    upper_bin: Optional[Union[int, float]] = None
    upper_bin6: Optional[Union[int, float]] = None

class Homologue(BaseModel):
    model_config = ConfigDict(extra='forbid')
    species_id: str
    species_name: str
    homology_type: str
    target_gene_id: str
    is_high_confidence: Optional[str] = None
    target_gene_symbol: str
    query_percentage_identity: float
    target_percentage_identity: float
    priority: int

class Tractability(BaseModel):
    model_config = ConfigDict(extra='forbid')
    modality: str
    id: str
    value: bool

class TargetEnablingPackage(BaseModel):
    model_config = ConfigDict(extra='forbid')
    target_from_source_id: Optional[str] = None
    description: Optional[str] = None
    therapeutic_area: Optional[str] = None
    url: Optional[str] = None

class Xref(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    source: str

class AssociatedProtein(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    source: str

class GeneProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    symbol: str
    name: Optional[str] = None
    biotype: Optional[str] = None
    sources: Optional[GeneSource] = None
    transcript_ids: Optional[List[str]] = None
    canonical_transcript: Optional[CanonicalTranscript] = None
    canonical_exons: Optional[List[str]] = None
    genomic_location: Optional[GenomicLocation] = None
    alternative_genes: Optional[List[str]] = None
    synonyms: Optional[List[LabelSource]] = None
    symbol_synonyms: Optional[List[LabelSource]] = None
    name_synonyms: Optional[List[LabelSource]] = None
    obsolete_symbols: Optional[List[LabelSource]] = None
    obsolete_names: Optional[List[LabelSource]] = None
    associated_proteins: Optional[List[AssociatedProtein]] = None
    xrefs: Optional[List[Xref]] = None
    homologues: Optional[List[Homologue]] = None
    tractability: Optional[List[Tractability]] = None
    constraint_scores: Optional[List[ConstraintScore]] = None
    subcellular_locations: Optional[List[SubcellularLocation]] = None
    target_enabling_package: Optional[TargetEnablingPackage] = None
    
    hallmarks_attributes: Optional[Any] = None
    cancer_hallmarks: Optional[Any] = None
    chemical_probes: Optional[Any] = None
    safety_liabilities: Optional[Any] = None
    target_class: Optional[Any] = None
    function_descriptions: Optional[List[Any]] = None
    transcription_start_site: Optional[int] = None

class GeneNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: str
    properties: GeneProperties
