import os
import shutil

# 폴더 경로 설정
source_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\CVLab2023-Hand-renamed'  # 원본 파일이 있는 폴더 경로
target_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221_작업1'  # 파일을 이동시킬 폴더 경로

# 대상 폴더 생성 (없는 경우)
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 폴더 내의 "_M2"가 포함된 파일들 복사
for file_name in os.listdir(source_folder):
    if "_M2" in file_name:
        source_path = os.path.join(source_folder, file_name)
        target_path = os.path.join(target_folder, file_name)
        shutil.copy2(source_path, target_path) 