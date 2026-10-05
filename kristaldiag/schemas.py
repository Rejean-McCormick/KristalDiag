from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import jsonschema

ARTIFACT_SCHEMAS={
 'kristall_manifest':'kristall-manifest.schema.json',
 'kristall_entity_registry':'kristall-entity-registry.schema.json',
 'kristall_property_registry':'kristall-property-registry.schema.json',
 'kristall_assertion_registry':'kristall-assertion-registry.schema.json',
 'kristall_source_registry':'kristall-source-registry.schema.json',
 'kristall_assertion_family_registry':'kristall-assertion-family-registry.schema.json',
 'kristall_mesh':'kristall-mesh.schema.json',
 'kristall_axis_registry':'kristall-axis-registry.schema.json',
 'kristall_projection_recipe':'kristall-projection-recipe.schema.json',
 'kristall_crystallization_record':'kristall-crystallization-record.schema.json',
 'semantic_resonance_set':'semantic-resonance.schema.json',
}

class SchemaStore:
    def __init__(self, repo_root:Path):
        self.root=repo_root
        packaged=Path(__file__).resolve().parent/'resources'/'contracts'
        base=(repo_root/'contracts') if (repo_root/'contracts'/'v7').is_dir() else packaged
        self.v7=base/'v7'
        self.v6=base/'v6'
        self._cache={}
    def _load(self,p:Path):
        key=str(p)
        if key not in self._cache:self._cache[key]=json.loads(p.read_text(encoding='utf-8'))
        return self._cache[key]
    def validate_v7(self,artifact:dict[str,Any]):
        typ=artifact.get('artifact_type'); fn=ARTIFACT_SCHEMAS.get(typ)
        if not fn:return False,[f'no v7 schema mapping for artifact_type={typ!r}']
        return self._validate(self._load(self.v7/fn),artifact)
    def validate_v6(self,artifact:dict[str,Any]):
        return self._validate(self._load(self.v6/'kristal-state.schema.json'),artifact)
    def validate_extension(self,ext:dict[str,Any]):
        return self._validate(self._load(self.v7/'kristal-v7-extension.schema.json'),ext)
    @staticmethod
    def _validate(schema,data):
        validator=jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker())
        errors=sorted(validator.iter_errors(data),key=lambda e:list(e.absolute_path))
        out=[]
        for e in errors:
            path='/'+'/'.join(str(x) for x in e.absolute_path) if e.absolute_path else '/'
            out.append(f'{path}: {e.message}')
        return not out,out
