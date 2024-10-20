import cv2
import numpy as np
import torch
from models.D_IDPreserve import IDPreserveGAN
from datasets import IDPreserveDataset
import os
import random
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ckpt_path_idpreserve', type=str, required=True)
    parser.add_argument('--gpu_ids', type=str, default='0', help='List IDs of GPU available. ex) --gpu_ids=0,1,2,3 , Use -1 for CPU mode')
    args = parser.parse_args()

    manualSeed = 99999999999999
    random.seed(manualSeed)
    torch.manual_seed(manualSeed)

    gpu_ids = [int(n) for n in args.gpu_ids.split(',') if int(n) >= 0]
    device = torch.device('cuda:{}'.format(gpu_ids[0]) if (torch.cuda.is_available() and gpu_ids) else 'cpu')
    torch.set_default_device(device)

    ckpt_idpreserve = torch.load(args.ckpt_path_idpreserve, map_location=device)
    Gen_idpreserve = IDPreserveGAN(2, 1, gpu_ids)
    Gen_idpreserve.net_G.load_state_dict(ckpt_idpreserve['modelG_state_dict'])
    Gen_idpreserve.net_G.to(device)
    Gen_idpreserve.net_G.eval()

    image_folder_path = os.path.join('..','..','make_maskmap', 'handdorsal_0228','handdorsal_sample')
    output_folder = 'generate_handdorsal_sample_rotation_0304_ori_3000'
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(image_folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder_path, file_name)
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)

            # Process the image as per the original code
            b, g, r = cv2.split(image)
            img_condis = np.stack([b, r], axis=2)  # "r" is same as "g"
            idpreserve_A = IDPreserveDataset.tf_condi(img_condis)
            idpreserve_B = Gen_idpreserve.net_G(idpreserve_A.unsqueeze(0).to(device))

            # visualization
            img_idpreserve_B = idpreserve_B.detach().cpu().permute(0, 2, 3, 1).numpy()
            img_IDPre = cv2.normalize(img_idpreserve_B.squeeze(), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F).astype(np.uint8)
            img_IDPre = cv2.resize(img_IDPre, (512, 512))

            output_path = os.path.join(output_folder, file_name)
            cv2.imwrite(output_path, img_IDPre)
            print(f"Processed and saved: {output_path}")