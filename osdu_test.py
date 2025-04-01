import requests

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


access_token=requests.post("http://keycloak.osdu.rewant.cn/realms/osdu/protocol/openid-connect/token", data={
    "client_id": "osdu-admin",
    "client_secret": "b6WYXpyuBuC74fGg",
    "grant_type": "client_credentials",
    "scope": "openid",
}).json()['access_token']
print("access_token:",access_token)
# 初始化 AuthSession 类，传入 headers 和 base_url
auth_backend = AuthSession(
    headers={"Authorization": "Bearer " + access_token},
    # base_url="http://osdu.192-168-31-240.nip.io"
    base_url="http://osdu.osdu.rewant.cn"
)

# 权利-查询组
# entitlements_client = OSDUAPI.client('entitlements', auth_backend=auth_backend)
# response = entitlements_client.get_groups(
#     data_partition_id="osdu",
# )

# 法规-列表查询
# legal_client = OSDUAPI.client('legal', auth_backend=auth_backend)
# response = legal_client.list_legaltags(
#     valid=True,
#     data_partition_id="osdu",
# )

# 法规-创建  legal_client注释掉了验证（验证无法通过日期校验）
# response = legal_client.create_legaltag(
#     name="test-legal",
#     description="this is a test legal tag by osdu",
#     properties={
#         "countryOfOrigin":["US"],
#         "contractId":"No Contract Related",
#         "expirationDate":"2099-01-01",
#         "dataType":"Public Domain Data", 
#         "originator":"OSDU",
#         "securityClassification":"Public",
#         "exportClassification":"EAR99",
#         "personalData":"No Personal Data",
#         "extensionProperties": {
#             "anyCompanySpecificAttributes": "anyJsonTypeOfvalue"
#         }    
#     },
#     data_partition_id="osdu",
# )

# 模式-获取
# schema_client = OSDUAPI.client('schema', auth_backend=auth_backend)
# response = schema_client.get_schema(
#     id="osdu:wks:testwellbore:1.0.0",
#     data_partition_id="osdu",
# )

# 模式-创建
# response = schema_client.create_schema(
#     schema_info={
#         "schemaIdentity": {
#             "source": "wks",
#             "entityType": "testwellbore",
#             "authority": "osdu",
#             "schemaVersionMajor": 1,
#             "schemaVersionMinor": 0,
#             "schemaVersionPatch": 0,
#             "id": "osdu:wks:testwellbore:1.0.0"
#         },
#         "scope": "SHARED",
#         "status": "DEVELOPMENT"
#     },
#     schema={
#         "properties":{
#             "wellname":{
#                 "description":"well name test",
#                 "type":"string",
#                 "title":"well name"
#             },
#             "md":{
#                 "description":"md test",
#                 "type":"string",
#                 "title":"md"
#             },
#             "msg":{
#                 "description":"test msg",
#                 "type":"string",
#                 "title":"Message"
#             }
#         },
#         "required":["wellname"]
#     },
#     data_partition_id="osdu",
# )

# 存储-创建记录 change 添加data字段传递数据
# storage_client = OSDUAPI.client('storage', auth_backend=auth_backend)
# response = storage_client.update_records(
#     data=[
#         {
#             "data": {
#                 "msg": "test data3",
#                 "md": "md test",
#                 "wellname": "wellname test"
#             },
#             "id": "osdu:testwellbore:123456789",
#             "kind": "osdu:wks:tttestwellbore:1.0.0",
#             "acl": {
#                 "owners": ["data.default.owners@osdu.group"],
#                 "viewers": ["data.default.viewers@osdu.group"]
#             },
#             "legal": {
#                 "legaltags": ["osdu-test-legal"],
#                 "otherRelevantDataCountries": ["US"],
#             }
#         },
#     ],
#     data_partition_id="osdu",
# )

# 存储-获取记录
# response = storage_client.get_record(
#     id="osdu:testwellbore:123456789",
#     data_partition_id="osdu",
# )

# print(f"Id: {response['id']}")
# print(f"Kind: {response['kind']}")
# print(f"Version: {response['version']}")
# print(f"Data: {response['data']}")

# 文件-获取signed url change  api/file/v2/files/uploadURL
# file_client = OSDUAPI.client('file', auth_backend=auth_backend)
# response = file_client.get_files_upload_url(
#     data_partition_id="osdu",
# )

## return data {'FileID': 'cf5ce59a7d3843cabbdbd8216ee83b6e', 'Location': {'SignedURL': 'http://s3.192-168-31-240.nip.io/refi-osdu-staging-area/440dd71b-5c7a-4719-93cc-9d85683aefcd/cf5ce59a7d3843cabbdbd8216ee83b6e?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=fileUser%2F20250324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250324T120825Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=6c4a7dd4e40b61647640e4004fd017b03430d723b911abf3c923040d3cec04c6', 'FileSource': '/440dd71b-5c7a-4719-93cc-9d85683aefcd/cf5ce59a7d3843cabbdbd8216ee83b6e'}}

# 文件-上传文件
# signed_url = 'http://s3.192-168-31-240.nip.io/refi-osdu-staging-area/4c9d13c4-4783-4b06-b019-bd9e2d0631f1/3a51364f9bfd404ea3fdf57649355de0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=fileUser%2F20250331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250331T120651Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c10f4dbe5a5a3de0ea9a40facab385f82a11dde4584e041c763fb5e38f723433'
# file_path = 'D:\pyPrjs\osdu\osdu-client\\test_data\\2G163-41.dev'  # 待上传的文件路径
 
# with open(file_path, 'rb') as file:
#     response = requests.put(signed_url, files={'File': file})
 
# print(response.status_code, response.text)

# 文件-创建元数据 change  api/file/v2/files/metadata
# response = file_client.create_files_metadata(
#     data = {
#         "Endian": "BIG",
#         "Description": "Example for Data Loading guide",
#         "DatasetProperties": {
#             "FileSourceInfo": {

#                 "FileSource": '/440dd71b-5c7a-4719-93cc-9d85683aefcd/cf5ce59a7d3843cabbdbd8216ee83b6e',
#                 "Name": "SLB Well Raster log",
#                 "PreLoadFilePath": "",
#                 "PreloadFileCreateUser": "jztest",
#                 "PreloadFileModifyDate": "25-03-21",
#                 "PreloadFileModifyUser": "Data Loading Team"
#             }
#         },
#         "TotalSize": "13245217273",
#         "Source": "Example Data Source",
#         "Name": "Dataset X221/15"
#     },
#     kind = "osdu:wks:dataset--File.Generic:1.0.0",
#     acl = {
#         "viewers": ["data.default.viewers@osdu.group"],
#         "owners": ["data.default.owners@osdu.group"]
#     },
#     legal = {
#         "legaltags": ["osdu-test-legal"],
#         "otherRelevantDataCountries": ["US"]
#     },

#     data_partition_id="osdu"
# )

# return data {'id': 'osdu:dataset--File.Generic:9453d2bf-f36e-462f-9a0e-bd74ec725c99'}

# 文件-下载文件url change  api/file/v2/files/downloadURL
# response = file_client.gets_url_to_download_file(
#     id="osdu:dataset--File.Generic:9453d2bf-f36e-462f-9a0e-bd74ec725c99",
#     data_partition_id="osdu",
# ) 


# 搜索-查询
search_client = OSDUAPI.client('search', auth_backend=auth_backend)
response = search_client.query(
    kind="demo-test:wks:wellbore:1.0.0",
    data_partition_id="osdu"
)

# return data {'results': [{'data': {'Endian': 'BIG', 'DatasetProperties.FileSourceInfo.Checksum': 'a7dcd3fed1e659f6b226374890cde97d', 'DatasetProperties.FileSourceInfo.FileSource': '/440dd71b-5c7a-4719-93cc-9d85683aefcd/cf5ce59a7d3843cabbdbd8216ee83b6e', 'DatasetProperties.FileSourceInfo.Name': 'SLB Well Raster log', 'Description': 'Example for Data Loading guide', 'VirtualProperties.DefaultName': 'Dataset X221/15', 'DatasetProperties.FileSourceInfo.ChecksumAlgorithm': 'MD5', 'DatasetProperties.FileSourceInfo.PreloadFileCreateUser': 'jztest', 'DatasetProperties.FileSourceInfo.PreloadFileModifyUser': 'Data Loading Team', 'Source': 'Example Data Source', 'Name': 'Dataset X221/15'}, 'kind': 'osdu:wks:dataset--File.Generic:1.0.0', 'source': 'wks', 'acl': {'viewers': ['data.default.viewers@osdu.group'], 'owners': ['data.default.owners@osdu.group']}, 'type': 'dataset--File.Generic', 'version': 1742818227471311, 'tags': {'normalizedKind': 'osdu:wks:dataset--File.Generic:1'}, 'createTime': '2025-03-24T12:10:27.509Z', 'authority': 'osdu', 'namespace': 'osdu:wks', 'legal': {'legaltags': ['osdu-test-legal'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'}, 'createUser': 'osdu-admin@service.local', 'id': 'osdu:dataset--File.Generic:9453d2bf-f36e-462f-9a0e-bd74ec725c99'}, {'createTime': '2025-03-24T12:06:21.604Z', 'kind': 'osdu:wks:tttestwellbore:1.0.0', 'authority': 'osdu', 'namespace': 'osdu:wks', 'legal': {'legaltags': ['osdu-test-legal'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'}, 'createUser': 'osdu-admin@service.local', 'source': 'wks', 'acl': {'viewers': ['data.default.viewers@osdu.group'], 'owners': ['data.default.owners@osdu.group']}, 'id': 'osdu:tttestwellbore:1234567', 'type': 'tttestwellbore', 'version': 1742817981514895, 'tags': {'normalizedKind': 'osdu:wks:tttestwellbore:1'}}, {'createTime': '2025-03-24T12:06:31.995Z', 'kind': 'osdu:wks:tttestwellbore:1.0.0', 'authority': 'osdu', 'namespace': 'osdu:wks', 'legal': {'legaltags': ['osdu-test-legal'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'}, 'createUser': 'osdu-admin@service.local', 'source': 'wks', 'acl': {'viewers': ['data.default.viewers@osdu.group'], 'owners': ['data.default.owners@osdu.group']}, 'id': 'osdu:testwellbore:1234567', 'type': 'tttestwellbore', 'version': 1742817991964326, 'tags': {'normalizedKind': 'osdu:wks:tttestwellbore:1'}}, {'createTime': '2025-03-24T12:06:57.388Z', 'kind': 'osdu:wks:tttestwellbore:1.0.0', 'authority': 'osdu', 'namespace': 'osdu:wks', 'legal': {'legaltags': ['osdu-test-legal'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'}, 'createUser': 'osdu-admin@service.local', 'source': 'wks', 'acl': {'viewers': ['data.default.viewers@osdu.group'], 'owners': ['data.default.owners@osdu.group']}, 'id': 'osdu:testwellbore:12345678', 'type': 'tttestwellbore', 'version': 1742818017341002, 'tags': {'normalizedKind': 'osdu:wks:tttestwellbore:1'}}, {'createTime': '2025-03-24T12:07:16.723Z', 'kind': 'osdu:wks:tttestwellbore:1.0.0', 'authority': 'osdu', 'namespace': 'osdu:wks', 'legal': {'legaltags': ['osdu-test-legal'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'}, 'createUser': 'osdu-admin@service.local', 'source': 'wks', 'acl': {'viewers': ['data.default.viewers@osdu.group'], 'owners': ['data.default.owners@osdu.group']}, 'id': 'osdu:testwellbore:123456789', 'type': 'tttestwellbore', 'version': 1742818036689898, 'tags': {'normalizedKind': 'osdu:wks:tttestwellbore:1'}}], 'aggregations': None, 'phraseSuggestions': [], 'totalCount': 5}

print(response)


# # 打印所有可用的服务
# OSDUAPI.print_available_services()

