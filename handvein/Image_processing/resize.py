from PIL import Image
import os

# 폴더 경로 설정
folder_path = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\512_crop_images\512_crop_palm_skel_L'  # 여기에 실제 폴더 경로를 입력하세요.

# 해당 폴더 내의 모든 파일들을 순회
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 이미지 파일 확장자 체크
        try:
            with Image.open(os.path.join(folder_path, filename)) as img:
                # 이미지 크기를 512x512로 변경
                img = img.resize((512, 512))
                # 변경된 이미지 저장
                img.save(os.path.join(folder_path, filename))
                print(f"Resized {filename}")
        except Exception as e:
            print(f"Error resizing {filename}: {e}")