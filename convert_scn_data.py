import os
import glob
import numpy as np
from PIL import Image
from PIL import ImageOps

dataset_dir = '/Users/suzukiay/workspace/models/research/slim/scn'
train_num = 2200
validation_num = 300

def horizontal_flip(image):
  image = image[:, ::-1, :]
  return image

def augmentation(classname):
  target_dir =  os.path.join(dataset_dir, classname)
  files = glob.glob(target_dir+'/*.jpg')
  totaldata_num = train_num + validation_num

  if len(files)>totaldata_num:
    return
  generate_num = totaldata_num - len(files)
  random_filelist = np.random.permutation(files)[:generate_num]

  for f in random_filelist:
    image = Image.open(f)
    image_mirror = ImageOps.mirror(image)
    newfilename = os.path.basename(f).split('.')[0]+'_c.jpg'
    image_mirror.save(os.path.join(target_dir, newfilename))

def get_filenames_and_classes(dataset_dir):
  directories = []
  class_names = []
  for filename in os.listdir(dataset_dir):
    path = os.path.join(dataset_dir, filename)
    if os.path.isdir(path):
      directories.append(path)
      class_names.append(filename)
  photo_filenames = []
  for directory in directories:
    for filename in os.listdir(directory):
      path = os.path.join(directory, filename)
      photo_filenames.append(path)
  return photo_filenames, sorted(class_names)

 

#augmentation('flower')
_, c = get_filenames_and_classes(dataset_dir)
print(c)
