#Handdorsal & handpalm
- PyCharm
- Python > 3.5
- Torch > 2.0.0
- Other packages:
- torchvision
- Opencv-python
- pythonnet
- 
**1. Diffusion+Enhancement(thumbnail)**
- 지문,지정맥과 동일 방식 적용 그러나 원본이미지가 아닌 Skeleton image를 생성
- Generate_sample_diffusion.py 실행(생성시 ckpt 경로 입력)
- Handdorsal: diffusion_handdorsal_0202_1499.pt, handvein_enhancement_ckpt_epoch000300
- Handpalm: diffusion_handpalm_0204_1499.pt, handpalm_enhacnement_ckpt_epoch000260
- ![image](https://github.com/user-attachments/assets/8698ce9a-58e6-4887-920a-5842dfdace62)

**2. Image processing**
- extract_skeleton.py, Add_segmap_skeleton.py 파일 사용
- 원본 세그멘테이션 이미지에서 회전, x 이동, y 이동을 통해 변화를 준 후 512X512로 크롭함
- 변화된 정보는 세그멘테이션 이름에 저장 (dorsal_R_F990715_N_S1_01_r2_x29_y5.bmp)
- 최종 이미지 생성 시 이름(r2_x29_y5 : 회전 2도, x: 29 이동, y: 5이동) 파싱하여 skeleton image 에 적용 후 마스크맵 생성
- ![image](https://github.com/user-attachments/assets/b4c5b235-3c7b-4c32-bf36-a94936b948ba)

**3. IDPreserving**
- 지정맥과 동일 방식으로 이미지 학습
- Pair쌍 이미지에 대해 생성 시 손목 부분이 잘리지 않도록 검수 후 샘플 생성
- ![image](https://github.com/user-attachments/assets/7ab67c6d-351d-4d5e-b857-ea5d0a4d2178)

- R_Enhancement 샘플 생성
2_generate_sample_enhancement.py

- ID_preserveing network 샘플 생성
Command : python 3_generate_sample_handdorsal_ID_preserving.py --ckpt_path_idpreserve checkpoints/handdorsal_ckpt_epoch003000.pth
![image](https://github.com/user-attachments/assets/b5d1b939-f9d1-486b-be9d-0cce8ca405af)


