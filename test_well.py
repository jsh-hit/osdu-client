import requests

# 1. 获取访问令牌
def get_access_token(client_id, client_secret, tenant_id):
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
    return access_token

# 2. 创建Well记录
def create_well(token, partition_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Partition-Id": partition_id
    }
    
    well_data = {
        "kind": "osdu:wks:well--Well:1.0.0",  # 引用OSDU Schema服务定义的Well类型
        "acl": {"viewers": [f"data.default.viewers@{partition_id}"]},  # 访问控制，关联Entitlements服务
        "legal": {
            "legaltags": ["global-public-1"],  # 法律标签，需在Legal服务中预注册
            "otherRelevantDataCountries": ["US"]  # 数据相关国家
        },
        "data": {
            "WellID": "2G163-41",  # 井唯一标识符
            "Name": "Well_A",  # 井名称
            "Location": {
                "WGS84": "POINT(2.35 59.9)",  # WGS84坐标（默认格式）
                "CRS": "EPSG:4326"  # 坐标系，需通过CRS目录服务验证
            }
        }
    }
    
    storage_url = "https://<OSDU_ENDPOINT>/api/storage/v2/records"
    response = requests.post(storage_url, json={"records": [well_data]}, headers=headers)
    
    if response.status_code == 201:
        return response.json()["recordIds"][0]  # 返回生成的Well ID
    else:
        raise Exception(f"创建Well失败: {response.text}")

# 3. 创建Wellbore记录
def create_wellbore(token, partition_id, well_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Partition-Id": partition_id
    }
    
    wellbore_data = {
        "kind": "osdu:wks:wellbore--Wellbore:1.0.0",
        "acl": {"viewers": [f"data.default.viewers@{partition_id}"]},
        "legal": {"legaltags": ["global-public-1"], "otherRelevantDataCountries": ["US"]},
        "data": {
            "WellboreName": "2G163-41-Wellbore-1",
            "WellID": well_id,  # 引用上一步生成的Well ID
            "Status": "Active"
        }
    }
    
    storage_url = "https://<OSDU_ENDPOINT>/api/storage/v2/records"
    response = requests.post(storage_url, json={"records": [wellbore_data]}, headers=headers)
    
    if response.status_code == 201:
        return response.json()["recordIds"][0]  # 返回生成的Wellbore ID
    else:
        raise Exception(f"创建Wellbore失败: {response.text}")

# 4. 主流程
if __name__ == "__main__":
    # 配置参数
    client_id = "<YOUR_CLIENT_ID>"
    client_secret = "<YOUR_CLIENT_SECRET>"
    tenant_id = "<YOUR_TENANT_ID>"
    partition_id = "<DATA_PARTITION_ID>"
    osdu_endpoint = "your-instance.energy.azure.com"  # 替换为实际端点
    
    # 获取令牌
    token = get_access_token(client_id, client_secret, tenant_id)
    
    # 创建Well并获取ID
    well_id = create_well(token, partition_id)
    print(f"Created Well ID: {well_id}")
    
    # 创建Wellbore并关联Well ID
    wellbore_id = create_wellbore(token, partition_id, well_id)
    print(f"Created Wellbore ID: {wellbore_id}")