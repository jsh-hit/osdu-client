import requests
import json



# 1. 获取访问令牌
def get_access_token(auth_url, client_id, client_secret):
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


def create_legal_tag(token,partition_id):
    url = f"{OSDU_BASE_URL}/api/legal/v1/legaltags"
    print("url:",url)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    
    legal_tag_body = {
        "name": "demo-legaltag-001",  # Legal Tag名称
        "description": "Demo legal tag for test well data",
        "properties": {
            "contractId": "123456",
            "countryOfOrigin": ["US"],           # 合规性国家代码
            "expirationDate": "2025-12-25",      # 失效日期
            "dataType": "Public Domain Data",
            "originator": "demo-user-001",       # 创建者标识, 发起人
            "securityClassification": "Private", # 保密等级
            "exportClassification": "EAR99", 
            "personalData": "No Personal Data",
        }
    }

    response = requests.post(url, headers=headers, json=legal_tag_body)
    
    if response.status_code == 201:
        print("Legal Tag创建成功！")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"错误 {response.status_code}: {response.text}")

# 查询LegalTag
def get_legal_tag(token,partition_id):
    url = f"{OSDU_BASE_URL}/api/legal/v1/legaltags"
    print("url:",url)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Legal Tag查询成功！")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"错误 {response.status_code}: {response.text}")




if __name__ == "__main__":
    # 配置参数
    # 配置 Keycloak 信息
    auth_url = "http://keycloak.osdu.rewant.cn/realms/osdu/protocol/openid-connect/token"
    client_id = "osdu-admin"
    client_secret = "adkjeNmF0sstdFOT"
    partition_id = "osdu"
    OSDU_BASE_URL = "http://osdu.osdu.rewant.cn"  
    
    # 获取令牌
    token = get_access_token(auth_url, client_id, client_secret)
    print(token)

    # 执行创建
    create_legal_tag(token,partition_id)

    # 查询legalTag
    # get_legal_tag(token,partition_id)


