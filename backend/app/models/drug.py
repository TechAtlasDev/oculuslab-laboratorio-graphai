from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union, Literal

class DrugSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class DrugProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: Optional[str] = None
    inchi_key: Optional[str] = None
    type: Optional[str] = None
    synonyms: Optional[List[str]] = None
    description: Optional[str] = None
    accession_numbers: Optional[List[str]] = None
    canonical_smiles: Optional[str] = None
    chemical_abstracts_service_number: Optional[str] = None
    unique_ingredient_identifier: Optional[str] = None
    black_box_warning: Optional[bool] = None
    year_of_first_approval: Optional[int] = None
    maximum_clinical_trial_phase: Optional[float] = None
    has_been_withdrawn: Optional[bool] = None
    is_approved: Optional[bool] = None
    trade_names: Optional[List[str]] = None
    sources: Optional[DrugSource] = None
    source_ids: Optional[List[str]] = None
    
    cd_id: Optional[Union[str, int]] = None
    cd_formula: Optional[str] = None
    cd_mol_weight: Optional[float] = None
    calculated_log_p: Optional[float] = None
    alogs: Optional[float] = None
    tpsa: Optional[float] = None
    lipinski: Optional[float] = None
    number_of_formulations: Optional[int] = None
    mol_file_base64: Optional[str] = None
    mol_image_base64: Optional[str] = None
    mrdef: Optional[str] = None
    enhanced_stereo: Optional[bool] = None
    aromatic_carbons: Optional[int] = None
    sp3_count: Optional[int] = None
    sp2_count: Optional[int] = None
    sp_count: Optional[int] = None
    halogen_count: Optional[int] = None
    hetero_sp2_count: Optional[int] = None
    rotatable_bonds: Optional[int] = None
    o_n: Optional[int] = None
    oh_nh: Optional[int] = None
    inchi: Optional[str] = None
    rgb: Optional[float] = None
    fda_labels: Optional[int] = None
    status: Optional[str] = None
    struct_id: Optional[Union[str, int]] = None

class DrugNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["DRG"]
    display_name: str
    properties: DrugProperties
