import datetime as dt
from typing import Optional

from ..utils import File, make_timestamp
from .base import API

push_asset_query = """
  mutation pushAsset(
    $tenantUuid: UUID!,
    $category: String!,
    $code: String!,
    $make: String,
    $model: String,
    $installationTimestamp: DateTime,
    $expectedLifeYears: Float,
    $photo: String
  ) {
    pushAsset(input: {
      tenantUuid: $tenantUuid,
      category: $category,
      code: $code,
      model: $model,
      make: $make,
      installationTimestamp: $installationTimestamp,
      expectedLifeYears: $expectedLifeYears,
      photo: $photo
    }) {
      asset {
        uuid
      }
    }
  }
"""

update_asset_query = """
  mutation updateAsset(
    $uuid: UUID!,
    $installationTimestamp: DateTime,
    $expectedLifeYears: Float,
    $photo: String
  ) {
    updateAsset(input: {
      uuid: $uuid,
      installationTimestamp: $installationTimestamp,
      expectedLifeYears: $expectedLifeYears,
      photo: $photo
    }) {
      asset {
        uuid
      }
    }
  }
"""

push_remark_query = """
  mutation pushRemark(
    $assetUuid: UUID!,
    $createdTimestamp: DateTime!,
    $resolvedTimestamp: DateTime,
    $description: String,
    $resolution: String
  ) {
    pushRemark(input: {
      assetUuid: $assetUuid,
      createdTimestamp: $createdTimestamp,
      resolvedTimestamp: $resolvedTimestamp,
      description: $description,
      resolution: $resolution
    }) {
      remark {
        uuid
      }
    }
  }
"""

push_service_query = """
  mutation pushService(
    $assetUuid: UUID!,
    $name: String!,
    $createdTimestamp: DateTime!,
    $description: String,
    $dueDate: Date,
    $performedTimestamp: DateTime,
    $result: String
  ) {
    pushService(input: {
      assetUuid: $assetUuid,
      name: $name,
      createdTimestamp: $createdTimestamp,
      description: $description,
      dueDate: $dueDate,
      performedTimestamp: $performedTimestamp,
      result: $result
    }) {
      service {
        uuid
      }
    }
  }
"""


class AssetAPI(API):
    def push_asset(
        self,
        tenant_uuid: str,
        category: str,
        code: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        installation_timestamp: Optional[dt.datetime] = None,
        expected_life_years: Optional[float] = None,
        photo: Optional[File] = None,
    ) -> str:
        photo_file_id = self.upload_file(photo)
        response_data = self.perform_query(
            push_asset_query,
            self.make_variables(
                tenantUuid=tenant_uuid,
                category=category,
                code=code,
                make=make,
                model=model,
                installationTimestamp=make_timestamp(installation_timestamp),
                expectedLifeYears=expected_life_years,
                photo=photo_file_id,
            ),
        )
        return response_data["pushAsset"]["asset"]["uuid"]

    def update_asset(
        self,
        uuid: str,
        installation_timestamp: Optional[dt.datetime] = None,
        expected_life_years: Optional[float] = None,
        photo: Optional[File] = None,
    ) -> str:
        photo_file_id = self.upload_file(photo)
        response_data = self.perform_query(
            update_asset_query,
            self.make_variables(
                uuid=uuid,
                installationTimestamp=make_timestamp(installation_timestamp),
                expectedLifeYears=expected_life_years,
                photo=photo_file_id,
            ),
        )
        return response_data["updateAsset"]["asset"]["uuid"]

    def push_asset_remark(
        self,
        asset_uuid: str,
        created_timestamp: dt.datetime,
        resolved_timestamp: Optional[dt.datetime] = None,
        description: Optional[str] = None,
        resolution: Optional[str] = None,
    ) -> str:
        response_data = self.perform_query(
            push_remark_query,
            self.make_variables(
                assetUuid=asset_uuid,
                createdTimestamp=make_timestamp(created_timestamp),
                resolvedTimestamp=make_timestamp(resolved_timestamp),
                description=description,
            ),
        )
        return response_data["pushRemark"]["remark"]["uuid"]

    def push_asset_service(
        self,
        asset_uuid: str,
        name: str,
        created_timestamp: dt.datetime,
        description: Optional[str] = None,
        due_date: Optional[dt.date] = None,
        performed_timestamp: Optional[dt.datetime] = None,
        result: Optional[str] = None,
    ) -> str:
        response_data = self.perform_query(
            push_service_query,
            self.make_variables(
                assetUuid=asset_uuid,
                name=name,
                description=description,
                createdTimestamp=make_timestamp(created_timestamp),
                dueDate=make_timestamp(due_date),
                performedTimestamp=make_timestamp(performed_timestamp),
                result=result,
            ),
        )
        return response_data["pushService"]["service"]["uuid"]
