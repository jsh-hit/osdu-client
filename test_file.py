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


def check(token):
    url = f"{OSDU_BASE_URL}/api/file/v2/liveness_check"
    print("url:",url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
         print("服务正常！")
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
    # get_file_upload_url(token=token)
    check(token)

    signed_url = "http://s3.192-168-31-240.nip.io/refi-osdu-staging-area/4c9d13c4-4783-4b06-b019-bd9e2d0631f1/3a51364f9bfd404ea3fdf57649355de0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=fileUser%2F20250331%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250331T120651Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c10f4dbe5a5a3de0ea9a40facab385f82a11dde4584e041c763fb5e38f723433"
    
    file_path = "D:\pyPrjs\osdu\osdu-client\\test_data\\2G163-41.dev"

    try:
        # 以二进制模式读取文件内容
        with open(file_path, "rb") as file:
            print("111")
            response = requests.put(signed_url, files={'File': file})
    
        
        # 发送PUT请求
        
        # 检查响应状态
        if response.status_code == 201:
            print("文件上传成功！")
        else:
            print(f"上传失败，状态码：{response.status_code}，错误信息：{response.text}")

    except FileNotFoundError:
        print(f"错误：文件路径不存在 - {file_path}")
    except Exception as e:
        print(f"请求异常：{str(e)}")
