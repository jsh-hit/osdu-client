import json

def convert_traces(input_file):
    traces = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            # 跳过所有注释行和空行
            if line.startswith('#') or not line:
                continue
            
            parts = line.split()
            
            # 检测是否为数据行：第一个元素是否能转为浮点数
            try:
                float(parts[0])  # 测试首元素是否为数字
            except (ValueError, IndexError):
                continue  # 跳过列标题行
            
            # 正式转换数据
            if len(parts) == 10:
                traces.append({
                    "MD": round(float(parts[0]), 4),
                    "X": round(float(parts[1]), 4),
                    "Y": round(float(parts[2]), 4),
                    "Z": round(float(parts[3]), 4),
                    "TVD": round(float(parts[4]), 4),
                    "DX": round(float(parts[5]), 6),
                    "DY": round(float(parts[6]), 6),
                    "AZIM": round(float(parts[7]), 4),
                    "INCL": round(float(parts[8]), 4),
                    "DLS": round(float(parts[9]), 4)
                })
    
    return {"traces": traces}

# 使用示例
output = convert_traces("./test_data/2G163-41.dev")
with open("traces.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)