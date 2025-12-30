import os
import requests
import time
import urllib.parse

def download_with_retry(url, file_path, max_retries=3, timeout=30):
    """带重试机制的下载函数"""
    for attempt in range(max_retries):
        try:
            print(f"尝试下载 (第{attempt+1}次): {os.path.basename(file_path)}")
            response = requests.get(url, stream=True, timeout=timeout)

            if response.status_code == 200:
                # 写入文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"✓ 下载成功: {os.path.basename(file_path)}")
                return True
            else:
                print(f"✗ 下载失败: {os.path.basename(file_path)} (状态码: {response.status_code})")

        except Exception as e:
            print(f"✗ 下载出错: {os.path.basename(file_path)} - {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # 递增等待时间
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)

    return False

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

    # 多个下载源
    base_urls = [
        "https://cdn.jsdelivr.net/gh/cgarciagl/face-api.js@0.22.2/weights/",
        "https://unpkg.com/face-api.js@0.22.2/weights/",
        "https://raw.githubusercontent.com/cgarciagl/face-api.js/master/weights/"
    ]

    # 下载进度计数器
    success_count = 0
    total_count = len(models)

    # 下载每个模型文件
    print("开始下载模型文件...")
    for model in models:
        file_path = os.path.join(models_dir, model)

        # 如果文件已存在，跳过下载
        if os.path.exists(file_path):
            print(f"文件已存在，跳过: {model}")
            success_count += 1
            continue

        # 尝试从不同源下载
        downloaded = False
        for base_url in base_urls:
            url = base_url + model
            if download_with_retry(url, file_path):
                downloaded = True
                success_count += 1
                break

        if not downloaded:
            print(f"✗ 所有源均下载失败: {model}")

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
        print("\n下一步: 请修改2.html文件中的MODEL_URL为'./models/'")
    else:
        print("\n⚠️ 部分必需模型文件缺失")
        print("\n建议:")
        print("1. 检查网络连接后重新运行脚本")
        print("2. 或者手动下载缺失的文件:")
        for file in required_files:
            if not os.path.exists(os.path.join(models_dir, file)):
                print(f"   - {base_urls[0]}{file}")

if __name__ == "__main__":
    download_models()
