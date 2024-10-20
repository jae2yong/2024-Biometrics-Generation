import os
import random
from PIL import Image

# 폴더 경로 설정
source_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\handdorsal_mask_sample_result'  # 원본 이미지 폴더 경로
target_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\handdorsal_mask_sample_result_warping_0220'  # 저장할 폴더 경로
log_file = '0220_handdorsal_warping_log.txt'        # 변화 정보를 저장할 텍스트 파일


# 대상 폴더 생성
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 로그 파일 초기화
with open(log_file, 'w') as file:
    file.write('Image Warping Log\n\n')

# 이미지 워핑 함수
def warp_image(image_path, image_name):
    with Image.open(image_path) as img:
        # 랜덤 회전 각도 선택 (-5도에서 5도 사이, 0.5도 단위)
        rotation = random.choice([i * 0.5 for i in range(-10, 11)])  # -5, -4.5, ..., 4.5, 5

        # 이미지 회전 (워핑)
        img = img.rotate(rotation, expand=True)

        # 변형된 이미지 저장
        img.save(os.path.join(target_folder, image_name))

        return rotation

# 폴더 내의 모든 이미지 처리
for image_name in os.listdir(source_folder):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        image_path = os.path.join(source_folder, image_name)
        rotation = warp_image(image_path, image_name)

        # 로그 정보 기록
        with open(log_file, 'a') as file:
            file.write(f'{image_name}: Rotation {rotation:.2f} degrees\n')