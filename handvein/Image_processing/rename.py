# import os

# # 폴더 경로 설정
# folder_path = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\handdorsal_crop'  # 여기에 폴더 경로를 입력하세요.

# # 폴더 내의 모든 파일에 대해
# for filename in os.listdir(folder_path):
#     if 'cropped_' in filename:
#         # 새 파일 이름 생성: '_HD' 제거
#         new_filename = filename.replace('cropped_', '')
#         # 파일 이름 변경
#         os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
#         print(f'파일 이름 변경: {filename} -> {new_filename}')

# print('모든 파일 이름 변경 완료.')

import os

# 폴더 경로 설정
folder_path = r'C:\Users\CVlab\Documents\01_2023\01_2023_BiosyntheticData\hand_dorsal\0221\transform_handpalm_seg_M1_R'

# 폴더 안의 모든 파일을 순회
for filename in os.listdir(folder_path):
    if '_M1' in filename:
        # 새 파일 이름 생성
        new_filename = filename.replace('_M1', '')
        # 파일 이름 변경
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

print("파일 이름 변경 완료!")