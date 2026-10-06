from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .utils import json_files,read_json,relpath

@dataclass
class JsonArtifact:
    path:Path
    rel:str
    data:dict[str,Any]
    artifact_type:str|None
    schema_version:str|None

@dataclass
class Inventory:
    root:Path
    artifacts:list[JsonArtifact]=field(default_factory=list)
    parse_errors:list[tuple[str,str]]=field(default_factory=list)
    by_type:dict[str,list[JsonArtifact]]=field(default_factory=dict)
    manifests:list[JsonArtifact]=field(default_factory=list)
    implementation_manifest:JsonArtifact|None=None
    is_standard_repo:bool=False
    scan_limit_reached:bool=False
    def get(self,typ):return self.by_type.get(typ,[])

def discover(root:Path, *, max_files:int=10000)->Inventory:
    root=root.resolve(); inv=Inventory(root=root)
    scan_root=root if root.is_dir() else root.parent
    inv.is_standard_repo=(scan_root/'schemas'/'v7').is_dir() and (scan_root/'schemas'/'v9').is_dir() and (scan_root/'schemas'/'v6'/'kristal-state.schema.json').is_file()
    scanned=0
    for p in json_files(root,max_files=max_files+1):
        scanned+=1
        if scanned>max_files:
            inv.scan_limit_reached=True
            break
        try:data=read_json(p)
        except Exception as e:
            inv.parse_errors.append((relpath(p,scan_root),f'{type(e).__name__}: {e}'));continue
        if not isinstance(data,dict):continue
        art=JsonArtifact(p,relpath(p,scan_root),data,data.get('artifact_type'),str(data.get('schema_version')) if data.get('schema_version') is not None else None)
        inv.artifacts.append(art)
        if art.artifact_type:inv.by_type.setdefault(art.artifact_type,[]).append(art)
        if art.artifact_type=='kristall_manifest':inv.manifests.append(art)
        if data.get('schema')=='kristaldiag.implementation.v1':inv.implementation_manifest=art
    return inv
