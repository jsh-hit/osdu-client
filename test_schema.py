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

def search_schema(token):
    url = f"{OSDU_BASE_URL}/api/schema-service/v1/schema"
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


def create_schema(token):
    url = f"{OSDU_BASE_URL}/api/schema-service/v1/schema"
    print("url:",url)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "data-partition-id": partition_id
    }

    schema_boby = {
        "schemaInfo": {
            "schemaIdentity": {
                "authority": "demo-test",
                "source": "wks",
                "entityType": "wellbore",
                "schemaVersionMajor": 1,
                "schemaVersionMinor": 0,
                "schemaVersionPatch": 0,
                "id": "demo-test:wks:wellbore:1.0.0"
            },
            "status": "DEVELOPMENT",
            "createdBy": "demo-user-001"
        },
        "schema": {
            "description": "A test demo for dev data.",
            "title": "WELL TRACE FROM PETREL",
            "type": "object",
            "properties": {
                "MD": {
                    "title": "Measured Depth",
                    "description": "沿井轨迹测量的深度，参考井基准面(KB)，单位：米",
                    "type": "number"
                },
                "X": {
                    "title": "X Coordinate",
                    "description": "横坐标值，坐标系未定义，单位：米",
                    "type": "number",
                    "format": "float"
                },
                "Y": {
                    "title": "Y Coordinate",
                    "description": "纵坐标值，坐标系未定义，单位：米",
                    "type": "number",
                    "format": "float"
                },
                "Z": {
                    "title": "True Vertical Depth",
                    "description": "真实垂直深度（相对于基准面），单位：米",
                    "type": "number"
                },
                "TVD": {
                    "title": "True Vertical Depth (Duplicate)",
                    "description": "真实垂直深度的重复字段（可能需要验证数据一致性），单位：米",
                    "type": "number"
                },
                "DX": {
                    "title": "Delta X",
                    "description": "X坐标变化量（单位未明确定义），建议单位：米",
                    "type": "number"
                },
                "DY": {
                    "title": "Delta Y",
                    "description": "Y坐标变化量（单位未明确定义），建议单位：米",
                    "type": "number"
                },
                "AZIM": {
                    "title": "Azimuth",
                    "description": "方位角（参考系未定义），单位：度",
                    "type": "number"
                },
                "INCL": {
                    "title": "Inclination",
                    "description": "井斜角，单位：度",
                    "type": "number"
                },
                "DLS": {
                    "title": "Dog Leg Severity",
                    "description": "狗腿度（井眼曲率），单位：度/30米",
                    "type": "number"
                }
            }
        }
    }

    response = requests.post(url, headers=headers, json=schema_boby)
    if response.status_code == 201:
        print("Test schema创建成功！")
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

    # search_schema(token=token)

    create_schema(token)