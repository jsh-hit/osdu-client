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

def create_records(token):

    with open("traces.json") as f:
        well_data = json.load(f)

    url =  f"{OSDU_BASE_URL}/api/storage/v2/records"
    print("url:",url)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }

    records_boby = {
        "kind": "osdu:demo-test:wks:wellbore:1.0.0",
        "acl": {
            "viewers": ['data.default.viewers@common.[osdu.opengroup.org]'],
            "owners": ['data.default.owners@common.[osdu.opengroup.org]']
        },
        "legal": {
            "legaltags": ['demo-legaltag-001'],
            "otherRelevantDataCountries": ["US","CN"]
        },
        "data": {
            "MD": 150.0,
            "X": 648557.0,
            "Y": 5162508.0,
            "Z": 1.1,
            "TVD": 150.0,
            "DX": 0.0,
            "DY": 0.0,
            "AZIM": 183.67,
            "INCL": 0.5,
            "DLS": 0.0
        }
    }

    response = requests.put(url, headers=headers, json=records_boby)
    if response.status_code == 200:
        print("records创建成功！")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"错误 {response.status_code}: {response.text}")

if __name__ == "__main__":
    # 配置参数
    # 配置 Keycloak 信息
    auth_url = "http://keycloak.osdu.rewant.cn/realms/osdu/protocol/openid-connect/token"
    client_id = "osdu-admin"
    client_secret = "hsN7IM8AGLTSBksQ"
    partition_id = "osdu"
    OSDU_BASE_URL = "http://osdu.osdu.rewant.cn"  
    
    # 获取令牌
    token = get_access_token(auth_url, client_id, client_secret)
    print(token)
    create_records(token=token)

