from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class PlateCreate:
    """  """

    barcode: Optional[str] = None
    container_schema_id: Optional[str] = None
    fields: Optional[Dict[Any, Any]] = None
    name: Optional[str] = None
    parent_storage_id: Optional[str] = None
    project_id: Optional[str] = None
    schema_id: Optional[str] = None
    wells: Optional[Dict[Any, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        container_schema_id = self.container_schema_id
        fields = self.fields if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        schema_id = self.schema_id
        wells = self.wells if self.wells else None

        return {
            "barcode": barcode,
            "containerSchemaId": container_schema_id,
            "fields": fields,
            "name": name,
            "parentStorageId": parent_storage_id,
            "projectId": project_id,
            "schemaId": schema_id,
            "wells": wells,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateCreate":
        barcode = d.get("barcode")

        container_schema_id = d.get("containerSchemaId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        schema_id = d.get("schemaId")

        wells = None
        if d.get("wells") is not None:
            wells = d.get("wells")

        return PlateCreate(
            barcode=barcode,
            container_schema_id=container_schema_id,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema_id=schema_id,
            wells=wells,
        )
