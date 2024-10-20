import cv2
import numpy as np
import os
import random
import re

# 이미지 파일 경로 설정
src_path = r"C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\new_maskmap\new_transforms_handdorsal_M1/"
dst_path = r"C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\new_maskmap\01_Handdorsal_diffusion_sample/"
save_path = "mask_sample_result/"

# 저장할 폴더가 없으면 생성
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 결과 기록을 위한 텍스트 파일 생성
log_file_path = "hand_palm_image_processing_log1.txt"

# 파일 이름에서 회전 정보, X 이동 정보, Y 이동 정보를 추출하는 함수
def extract_rotation_and_translation(filename):
    match = re.search(r'_r(-?\d+)_x(-?\d+)_y(-?\d+)', filename)
    if match:
        rotation = int(match.group(1))
        x_translation = int(match.group(2))
        y_translation = int(match.group(3))
        return rotation, x_translation, y_translation
    else:
        return None, None, None

# 특정 문자열이 포함된 파일들을 랜덤으로 선택하는 함수
def select_random_files_with_substring(file_list, substring, count):
    files_with_substring = [file for file in file_list if substring in file]
    return random.sample(files_with_substring, min(count, len(files_with_substring)))

# dst 파일에 대한 처리
for dst_file_name in os.listdir(dst_path):
    dst_file_path = os.path.join(dst_path, dst_file_name)
    dst_image = cv2.imread(dst_file_path)

    if dst_image is None:
        continue

    # dst 파일 이름에서 회전 정보, X 이동 정보, Y 이동 정보 추출
    dst_rotation, dst_x_translation, dst_y_translation = extract_rotation_and_translation(dst_file_name)

    # _N_, _S_, _W_가 포함된 파일 각각 10개씩 선택
    N_files = select_random_files_with_substring(os.listdir(src_path), "_N_", 10)
    S_files = select_random_files_with_substring(os.listdir(src_path), "_S_", 10)
    W_files = select_random_files_with_substring(os.listdir(src_path), "_W_", 10)

    # 각 파일 그룹에 대해 처리
    for file_group, group_label in zip([N_files, S_files, W_files], ['_N_', '_S_', '_W_']):
        for j, src_file_name in enumerate(file_group, start=1):
            src_file_path = os.path.join(src_path, src_file_name)
            seg_image = cv2.imread(src_file_path)

            # 이미지 크기 확인 및 조정
            if seg_image.shape[:2] != dst_image.shape[:2]:
                seg_image = cv2.resize(seg_image, (dst_image.shape[1], dst_image.shape[0]))

            # 이미지 처리 로직
            for y in range(seg_image.shape[0]):
                for x in range(seg_image.shape[1]):
                    if np.all(seg_image[y, x] == [255, 255, 255]):  # 흰색 픽셀이면
                        seg_image[y, x] = np.array([255, 0, 0], dtype=np.uint8)  # 파란색으로 변경

            for y in range(dst_image.shape[0]):
                for x in range(dst_image.shape[1]):
                    if np.all(dst_image[y, x] > 9):  # 특정 조건에 따라
                        dst_image[y, x] = np.array([0, 255, 255], dtype=np.uint8)  # 노란색으로 변경

            result = cv2.add(dst_image, seg_image)

            for y in range(result.shape[0]):
                for x in range(result.shape[1]):
                    if np.all(result[y, x] == [0, 255, 255]):  # 노란색
                        result[y, x] = np.array([0, 0, 0], dtype=np.uint8)  # 검은색으로 변경
                    if np.all(result[y, x] == [255, 255, 255]):
                        result[y, x] = np.array([0, 255, 255], dtype=np.uint8)

            # 결과 이미지 저장
            result_file_name = f"{dst_file_name[:-4]}{group_label}{j}.png"
            result_file_path = os.path.join(save_path, result_file_name)
            cv2.imwrite(result_file_path, result)

            # 로그 파일에 기록
            with open(log_file_path, "a") as log_file:
                log_file.write(f"{dst_file_name} combined with {src_file_name} to create {result_file_name}\n")

            print(f"Created file: {result_file_name}")