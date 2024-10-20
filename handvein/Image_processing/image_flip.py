from PIL import Image
import os

# 이미지가 있는 폴더 경로
folder_path = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\new_transforms_handpalm_M1_R'

# 폴더 내의 모든 파일을 순회
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # 이미지 파일 경로
        image_path = os.path.join(folder_path, filename)

        # 이미지 열기
        with Image.open(image_path) as img:
            # 이미지를 좌우로 플립
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

            # 플립된 이미지 저장 (원본을 덮어쓰거나 새 파일로 저장 가능)
            flipped_img.save(os.path.join(folder_path, f'{filename}'))

print("모든 이미지가 플립되었습니다.")