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


# 初始化 AuthSession 类，传入 headers 和 base_url
auth_backend = AuthSession(
    headers={"Authorization": "Bearer XYZ"},
    base_url="http://osdu.osdu.rewant.cn"
)

# 使用 OSDUAPI 进行 API 调用
storage_client = OSDUAPI.client('storage', auth_backend=auth_backend)
# response = storage_client.get_record_versions(id="123")
# print(response)
# from osdu_client.client import OSDUAPI
OSDUAPI.print_available_services()



# 1. 搜索记录示例
def search_records():
    query = {
        "kind": "*:work-product-component:*",
        "query": "data.ExistenceKind:existing",
        "returnedFields": ["data.IndividualType", "data.ExistenceKind"]
    }

    response = client.search.query(
        body=query,
        limit=10
    )
    
    print("Search Results:")
    for result in response.results:
        print(f"Record ID: {result['id']}")
        print(f"Type: {result['data']['IndividualType']}")
        print("-" * 40)

# 2. 获取单个记录
def get_single_record(record_id: str):
    record = client.records.get_record(
        record_id=record_id,
        attributes=["all"]
    )
    
    print(f"\nRecord Details ({record_id}):")
    print(f"Kind: {record.kind}")
    print(f"Version: {record.version}")
    print(f"Data: {record.data}")

# 3. 使用示例
if __name__ == "__main__":
    try:
        # 执行搜索
        search_records()
        
        # 获取特定记录（示例ID）
        # get_single_record("opendes:wp:1234567890")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")