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

def get_file_upload_url(token):
    
    url = f"{OSDU_BASE_URL}/api/file/v2/files/uploadURL"
    print("url:",url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("file upload url 获取成功！")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"错误 {response.status_code}: {response.text}")

def upload_file_by_url(token,url):
    url = f"{OSDU_BASE_URL}/api/file/v2/files/uploadURL"
    print("url:",url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    
    response = requests.post(url, headers=headers)
    # response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("获取成功！")
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
    get_file_upload_url(token=token)

    signed_url = "http://s3.192-168-31-240.nip.io/refi-osdu-staging-area/07046ace-6c2c-4faf-a978-4e348ee85775/4693ed88974c4b07a87368e323d57b6e?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=fileUser%2F20250324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250324T123950Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0843576382971285249a22cca0ab524f7fe0394d15a7b4be6174800561ad9447"
    

