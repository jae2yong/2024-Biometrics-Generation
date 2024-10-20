import cv2
import os

def stitch_images(original_folder, segmented_folder, output_folder):
    for filename in os.listdir(segmented_folder):
        if not filename.lower().endswith('.png'):
            continue

        # 원본 이미지 파일 이름을 .bmp 확장자로 변경
        original_filename = os.path.splitext(filename)[0] + '.bmp'
        
        original_image_path = os.path.join(original_folder, original_filename)
        print(original_image_path)
        segmented_image_path = os.path.join(segmented_folder, filename)
        print(segmented_image_path)
        output_image_path = os.path.join(output_folder, filename)

        if os.path.exists(original_image_path) and os.path.exists(segmented_image_path):
            # 이미지 로드
            original_image = cv2.imread(original_image_path)
            segmented_image = cv2.imread(segmented_image_path)

            # 이미지 스티칭
            stitched_image = cv2.hconcat([segmented_image, original_image])

            # 결과 저장
            cv2.imwrite(output_image_path, stitched_image)
            print(f"Stitched image saved to {output_image_path}")
        else:
            print(f"Image not found for {filename}")

# 사용 예시
original_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\512_transforms_handpalm_ori'
segmented_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\handpalm_train_mask'
output_folder = '0222_stitched_images_handpalm'
os.makedirs(output_folder, exist_ok=True)

stitch_images(original_folder, segmented_folder, output_folder)