import os
import requests

def download_models():
    # 创建models目录
    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"已创建目录: {models_dir}")

    # 模型文件列表
    models = [
        "ssd_mobilenetv1_model-weights_manifest.json",
        "ssd_mobilenetv1_model-shard1",
        "face_landmark_68_model-weights_manifest.json",
        "face_landmark_68_model-shard1",
        "face_recognition_model-weights_manifest.json",
        "face_recognition_model-shard1",
        "face_recognition_model-shard2",
        "age_gender_model-weights_manifest.json",
        "age_gender_model-shard1",
        "face_expression_model-weights_manifest.json",
        "face_expression_model-shard1"
    ]

    # 基础URL
    base_url = "https://cdn.jsdelivr.net/gh/cgarciagl/face-api.js@0.22.2/weights/"

    # 下载进度计数器
    success_count = 0
    total_count = len(models)

    # 下载每个模型文件
    print("开始下载模型文件...")
    for model in models:
        url = base_url + model
        file_path = os.path.join(models_dir, model)

        # 如果文件已存在，跳过下载
        if os.path.exists(file_path):
            print(f"文件已存在，跳过: {model}")
            success_count += 1
            continue

        try:
            print(f"正在下载: {model}")
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                # 写入文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"✓ 下载成功: {model}")
                success_count += 1
            else:
                print(f"✗ 下载失败: {model} (状态码: {response.status_code})")

        except Exception as e:
            print(f"✗ 下载出错: {model} - {str(e)}")

    print(f"\n下载完成! 成功: {success_count}/{total_count}")

    # 检查是否所有必需文件都已下载
    required_files = [
        "ssd_mobilenetv1_model-weights_manifest.json",
        "ssd_mobilenetv1_model-shard1",
        "face_landmark_68_model-weights_manifest.json",
        "face_landmark_68_model-shard1",
        "face_recognition_model-weights_manifest.json",
        "face_recognition_model-shard1",
        "face_recognition_model-shard2"
    ]

    all_required_exist = True
    for file in required_files:
        if not os.path.exists(os.path.join(models_dir, file)):
            all_required_exist = False
            print(f"缺少必需文件: {file}")

    if all_required_exist:
        print("\n✓ 所有必要模型文件已下载完成!")
    else:
        print("\n⚠️ 部分必需模型文件缺失，请检查网络连接后重试")

if __name__ == "__main__":
    download_models()
