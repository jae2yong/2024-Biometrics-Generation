import cv2
import numpy as np
import os

def find_contour_center(segmentation_path):
    img = cv2.imread(segmentation_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # 모든 윤곽선의 중심점을 찾아 평균을 계산
    x_sum, y_sum, count = 0, 0, 0
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            x_sum += int(M["m10"] / M["m00"])
            y_sum += int(M["m01"] / M["m00"])
            count += 1

    if count == 0:
        return None

    return x_sum // count, y_sum // count

def crop_image(original_path, center, output_path):
    if center is None:
        return

    img = cv2.imread(original_path, cv2.IMREAD_COLOR)
    img_height, img_width = img.shape[:2]

    center_x, center_y = center
    left = max(center_x - 256, 0)
    right = min(center_x + 256, img_width)
    top = max(center_y - 256, 0)
    bottom = min(center_y + 256, img_height)

    cropped_img = img[top:bottom, left:right]
    cv2.imwrite(output_path, cropped_img)

# def crop_images_based_on_segmentation(original_folder, segmentation_folder, output_folder):
#     for filename in os.listdir(segmentation_folder):
#         if filename.lower().endswith('.bmp'):  # 세그멘테이션 파일의 확장자 체크
#             base_filename = filename.replace('_M2.bmp', '.png')  # 원본 이미지 파일 이름으로 변환
#             original_path = os.path.join(original_folder, base_filename)
#             segmentation_path = os.path.join(segmentation_folder, filename)
#             output_path = os.path.join(output_folder, base_filename)

#             if os.path.exists(original_path):
#                 center = find_contour_center(segmentation_path)
#                 crop_image(original_path, center, output_path)
#                 print(f"Cropped image saved to {output_path}")
#             else:
#                 print(f"Original image not found for {filename}")
def crop_images_based_on_segmentation(original_folder, segmentation_folder, output_folder):
    for filename in os.listdir(segmentation_folder):
        if filename.lower().endswith('.bmp'):  # 세그멘테이션 파일의 확장자 체크
            base_filename = filename.replace('_M2.bmp', '.png')  # 원본 이미지 파일 이름으로 변환
            original_path = os.path.join(original_folder, base_filename)
            segmentation_path = os.path.join(segmentation_folder, filename)
            output_path = os.path.join(output_folder, base_filename)

            if os.path.exists(original_path):
                center = find_contour_center(segmentation_path)
                crop_image(original_path, center, output_path)
                print(f"Cropped image saved to {output_path}")
            else:
                print(f"Original image not found for {filename}")
  

# 사용 예시
original_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\512_crop_images\crop_palm_skel_L'
segmentation_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\handdorsal_palm_seg_M2\palm_L_M2_erosion'
output_folder = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\512_crop_images\512_crop_palm_skel_L'
os.makedirs(output_folder, exist_ok=True)
crop_images_based_on_segmentation(original_folder, segmentation_folder, output_folder)