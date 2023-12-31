import os
import random
from PIL import Image
from torchvision.transforms import v2
import torch

class RandomBackground:
    def __init__(self):
        # get all images path from folder ./caltech256 
        # and save to self.images
        self.olddataset_path = "./background_generator/caltech256"
        self.image_size = 384
        self.__list_images()

        self.transform = v2.Compose([
            v2.ToImage(),
            v2.ToDtype(torch.float32, scale=True),
            v2.RandomRotation(360),
            v2.RandomPerspective(distortion_scale=0.1),
            v2.RandomChannelPermutation(),
            v2.RandomHorizontalFlip(),
            v2.RandomVerticalFlip(),
            v2.RandomInvert(),
            v2.RandomPosterize(bits=6),
            v2.RandomAutocontrast(),
            v2.RandomEqualize(),
        ])
        # gaussian_noise quasicrystal

    def __list_images(self):
        self.images = []
        for root, dirs, files in os.walk(self.olddataset_path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    self.images.append(os.path.join(root, file))

    def __get_random_image(self):
        return random.choice(self.images)

    def getImage(self, width, height):
        image_path = self.__get_random_image()
        with Image.open(image_path) as img:
            img = self.transform(img)
            img = v2.RandomResizedCrop((height, width), ratio=(1, 3), antialias=True)(img)
        return img

# test
if __name__ == "__main__":
    randombackground = RandomBackground()
    img = randombackground.getImage(300,100)
    # save image to test.jpg
    v2.ToPILImage()(img).save("test.jpg")


