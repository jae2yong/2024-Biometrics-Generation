import argparse
import cv2
import numpy as np
import torch
from PIL import Image
from torchvision.utils import make_grid
import torchvision.transforms as transforms
from train_ridgepatternGAN import RidgePatternGenerator
from diffusers import UNet2DModel, DDPMPipeline, DDPMScheduler
import os

# import random
import time

# Create a grid of images using PIL
def make_image_grid(images, rows, cols):
    w, h = images[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))
    for i, image in enumerate(images):
        grid.paste(image, box=(i % cols * w, i // cols * h))
    return grid

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('--ckpt_path_ridgepattern', type=str, default='ckpt_epoch260.pth')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--gpu_id', type=int, default=0)
    # parser.add_argument('--ckpt_num', type=int, default=0)
    args = parser.parse_args()
    bs = args.batch_size

    gpu_id = args.gpu_id

    device = torch.device('cuda:%d' % gpu_id if torch.cuda.is_available() else 'cpu')
    torch.set_default_device(device)

    print(device)


    # Initialize UNet2DModel from sample_gpu.py
    model_checkpoint_path = "diffusion_fingerprint/handpalm_0204_1449.pt"
    checkpoint = torch.load(model_checkpoint_path)
    loaded_model = UNet2DModel(
        sample_size=64,
        in_channels=3,
        out_channels=3,
        layers_per_block=2,
        block_out_channels=(128, 128, 256, 256, 512, 512),
        down_block_types=("DownBlock2D", "DownBlock2D", "DownBlock2D", "DownBlock2D", "AttnDownBlock2D", "DownBlock2D"),
        up_block_types=("UpBlock2D", "AttnUpBlock2D", "UpBlock2D", "UpBlock2D", "UpBlock2D", "UpBlock2D"),
    ).to(device)
    loaded_model.load_state_dict(checkpoint['model_state_dict'])
    loaded_model = loaded_model.to(device)

    loaded_noise_scheduler = checkpoint['noise_schedule']

    pipeline = DDPMPipeline(unet=loaded_model, scheduler=loaded_noise_scheduler)
    pipeline = pipeline.to(device)

    image_size = 256
    tf = transforms.Resize(image_size, antialias=True)

    # out_path = 'iris_gen_ckpt%04d' % int(model_checkpoint_path.split('/')[-1].split('_')[-1].split('.')[0])
    out_path = 'handpalm_0204%d' % gpu_id
    os.makedirs(out_path, exist_ok=True)

#    for i in range(1,9999):
#        # Generate sample images using UNet2DModel from sample_gpu.py
#        generated_images = pipeline(
#            batch_size=bs,
#            generator=torch.manual_seed(time.time()),
#        ).images

#        image_grid = make_image_grid(generated_images, rows=1, cols=bs)
#        image_grid_np = np.array(image_grid)
#        image_grid_gray_np = cv2.cvtColor(image_grid_np, cv2.COLOR_RGB2GRAY)
        # image_grid_gray = Image.fromarray(image_grid_gray_np)
        # Process through RidgePatternGenerator
        # image_grid_tensor = transforms.ToTensor()(image_grid_gray).unsqueeze(0).to(device) # Convert the PIL Image to tensor
        #real_A = tf(image_grid_tensor)
        #img_fake_B = Gen_ridgepattern(real_A).detach().cpu()
        #montage_fake_B = make_grid(img_fake_B, nrow=int(bs ** 0.5), normalize=True).permute(1, 2, 0).numpy()
        #montage_fake_B = cv2.normalize(montage_fake_B, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F).astype(np.uint8)
        
#        cv2.imwrite(out_path+'/'+str(i).zfill(4)+'.png', image_grid_gray_np)
#        print(f"Generated and processed sample {i}")
for i in range(1, 2001):
    # Generate sample images using UNet2DModel from sample_gpu.py
    generated_images = pipeline(
        batch_size=bs,
        generator=torch.manual_seed(time.time()),
    ).images

 
    for j, image in enumerate(generated_images):
        image_np = np.array(image)
        image_gray_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        cv2.imwrite(f"{out_path}/{str(i).zfill(4)}.png", image_gray_np)

    print(f"Generated and processed batch {i}")