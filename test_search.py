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

def search_query(token):
    record_id = "osdu:wellbore:389595731c6141d2992fe23723b69170"
    url = f"{OSDU_BASE_URL}/api/search/v2/query"
    # url = f"{OSDU_BASE_URL}/api/storage/v2/records/{record_id}"
    print("url:",url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    search_body = {
        "kind": "demo-test:wks:wellbore:1.0.0",
    }
    
    response = requests.post(url, headers=headers, json=search_body)
    # response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("search api查询成功！")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"错误 {response.status_code}: {response.text}")

if __name__ == "__main__":
    # 配置参数
    # 配置 Keycloak 信息
    auth_url = "http://keycloak.osdu.rewant.cn/realms/osdu/protocol/openid-connect/token"
    client_id = "osdu-admin"
    client_secret = "b6WYXpyuBuC74fGg"
    partition_id = "osdu"
    OSDU_BASE_URL = "http://osdu.osdu.rewant.cn"  
    
    # 获取令牌
    token = get_access_token(auth_url, client_id, client_secret)
    print(token)
    search_query(token=token)
    

