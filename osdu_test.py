from osdu_client.client import OSDUAPI
from osdu_client.auth import AuthBackendInterface

class AuthSession(AuthBackendInterface):
    def __init__(self, headers, base_url):
        self._authorization_header = headers  # 私有变量存储 headers
        self._base_url = base_url  # 私有变量存储 base_url
        self._default_data_partition_id = "osdu"  # 默认的 partition id

    @property
    def authorization_header(self):
        return self._authorization_header

    @property
    def base_url(self):
        return self._base_url

    @property
    def default_data_partition_id(self):
        return self._default_data_partition_id

    def get_sd_connection_params(self):
        return {}


# 获取token
import requests
# 配置 Keycloak 信息
auth_url = "http://keycloak.osdu.rewant.cn/realms/osdu/protocol/openid-connect/token"
client_id = "osdu-admin"
client_secret = "hsN7IM8AGLTSBksQ"
# 发送请求
try:
    response = requests.post(
        auth_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
    )
    response.raise_for_status()
    access_token = response.json().get("access_token")
    # print("Access Token:", access_token)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    print("Response Content:", response.text)



# 初始化 AuthSession 类，传入 headers 和 base_url
auth_backend = AuthSession(
    headers={"Authorization": f"Bearer {access_token}"},
    base_url="http://osdu.osdu.rewant.cn"
)

# 打印可用服务
OSDUAPI.print_available_services()

# 使用 OSDUAPI 进行 API 调用
# 调用 storage 服务
storage_client = OSDUAPI.client('storage', auth_backend=auth_backend)
res = storage_client.get_info(data_partition_id="123")
print(res)
# result = storage_client.update_records(data_partition_id="osdu")
# print(result)
# response = storage_client.get_record_versions(id="osdu")
# print(response)

# 2. 查询数据分区列表
def list_partitions(access_token):
    url = "http://osdu.osdu.rewant.cn/api/partition/v1/partitions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
list_partitions(access_token=access_token)

# # 1. 搜索记录示例
# def search_records():
#     query = {
#         "kind": "*:work-product-component:*",
#         "query": "data.ExistenceKind:existing",
#         "returnedFields": ["data.IndividualType", "data.ExistenceKind"]
#     }

#     response = OSDUAPI.client.search.query(
#         body=query,
#         limit=10
#     )
    
#     print("Search Results:")
#     for result in response.results:
#         print(f"Record ID: {result['id']}")
#         print(f"Type: {result['data']['IndividualType']}")
#         print("-" * 40)

# # 2. 获取单个记录
# def get_single_record(record_id: str):
#     record = OSDUAPI.client.records.get_record(
#         record_id=record_id,
#         attributes=["all"]
#     )
    
#     print(f"\nRecord Details ({record_id}):")
#     print(f"Kind: {record.kind}")
#     print(f"Version: {record.version}")
#     print(f"Data: {record.data}")

# # 3. 使用示例
# if __name__ == "__main__":
#     try:
#         # 执行搜索
#         search_records()
        
#         # 获取特定记录（示例ID）
#         # get_single_record("opendes:wp:1234567890")
        
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")