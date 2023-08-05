from .base import API

route_to_tenant_query = """
  mutation routeToTenant($tenantUuid: UUID!, $routeCode: String!) {
    routeToTenant(input: {tenantUuid: $tenantUuid, routeCode: $routeCode}) {
      route {
        id
        uuid
      }
    }
  }
"""

route_to_asset_query = """
  mutation routeToAsset($assetUuid: UUID!, $routeCode: String!) {
    routeToAsset(input: {assetUuid: $assetUuid, routeCode: $routeCode}) {
      route {
        id
        uuid
      }
    }
  }
"""


class RoutingAPI(API):
    def route_to_tenant(self, route_code: str, tenant_uuid: str) -> str:
        result = self.perform_query(
            route_to_tenant_query, {"routeCode": route_code, "tenantUuid": tenant_uuid}
        )
        return result["routeToTenant"]["route"]["uuid"]

    def route_to_asset(self, route_code: str, asset_uuid: str) -> str:
        result = self.perform_query(
            route_to_asset_query, {"routeCode": route_code, "assetUuid": asset_uuid}
        )
        return result["routeToAsset"]["route"]["uuid"]
