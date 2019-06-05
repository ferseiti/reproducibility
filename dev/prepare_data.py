#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import os
import cv2
import h5py
import numpy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.misc as spm

from tensorflow import set_random_seed
set_random_seed(42)
numpy.random.seed(42)

amount_crops = 30 # Quantos patches de cada imagem
patch_size = 32 # Tamanho dos patches das amostras
label_size = 20 # Tamanho dos patches das labels
conv_side = 6 # será a borda da convolução?
scale = 2
# BORDER_CUT = 8
BLOCK_STEP = 16
BLOCK_SIZE = 32


# In[2]:


def load_data(x_file, y_file):
    data = numpy.array((5,5))
    label = numpy.array((5,5))
    with h5py.File(x_file, 'r') as hfx:
        data = numpy.array(hfx['data'])
        print(data.shape)
    with h5py.File(y_file, 'r') as hfy:
        label = numpy.array(hfy['data'])
        print(label.shape)
    return data, label


# In[3]:


def prepare_data(x_path, y_path):
    x_names = sorted(os.listdir(x_path))
    y_names = sorted(os.listdir(y_path))
    
    x_count = len(x_names)
    y_count = len(y_names)

    data = numpy.zeros((nums * amount_crops, 1, patch_size, patch_size), dtype=numpy.uint8)
    label = numpy.zeros((nums * amount_crops, 1, label_size, label_size), dtype=numpy.uint8)

    for i in range(nums):
        name = _path + names[i]
        hr_img = mpimg.imread(name)
        shape = hr_img.shape

        hr_img = hr_img[:, :, 0]

        # two resize operation to produce training data and labels
        lr_img = spm.imresize(lr_img, size=shape, interp='bicubic')

        # produce amount_crops random coordinate to crop training img
        Points_x = numpy.random.randint(0, min(shape[0], shape[1]) - patch_size, amount_crops)
        Points_y = numpy.random.randint(0, min(shape[0], shape[1]) - patch_size, amount_crops)

        for j in range(amount_crops):
            lr_patch = lr_img[Points_x[j]: Points_x[j] + patch_size, Points_y[j]: Points_y[j] + patch_size]
            hr_patch = hr_img[Points_x[j]: Points_x[j] + patch_size, Points_y[j]: Points_y[j] + patch_size]


            lr_patch = lr_patch
            hr_patch = hr_patch

            data[i * amount_crops + j, 0, :, :] = lr_patch
            label[i * amount_crops + j, 0, :, :] = hr_patch[conv_side: -conv_side, conv_side: -conv_side]
            
#             import matplotlib
#             matplotlib.use('TKagg')
            
#             plt.imshow(lr_patch)
#             plt.waitforbuttonpress()
#             plt.imshow(hr_patch)
#             plt.waitforbuttonpress()

            # cv2.imshow("lr", lr_patch)
            # cv2.imshow("hr", hr_patch)
            # cv2.waitKey(0)
#             %matplotlib inline
    return data, label


# In[4]:


def prepare_crop_data(x_path, y_path):
    
    full_data, full_label = load_data(x_path, y_path)

    data = []
    label = []

    # We are using 8-bit deep 256x256 and 512x512 images for the 
    # subsampled and labels, respectively

    for i in range(full_data.shape[0]//2):
        
        subsampled_img = full_data[i, :, :]
        label_img = full_label[i, :, :]
        
        shape = label_img.shape

        # just resizing to produce a bicubic interpolated image, since the image is already subsampled
        subsampled_img = spm.imresize(subsampled_img, size=shape, interp='bicubic')

        width_num = (shape[0] - (BLOCK_SIZE - BLOCK_STEP) * 2) // BLOCK_STEP
        height_num = (shape[1] - (BLOCK_SIZE - BLOCK_STEP) * 2) // BLOCK_STEP
        for k in range(width_num):
            for j in range(height_num):
                x = k * BLOCK_STEP
                y = j * BLOCK_STEP
                hr_patch = label_img[x: x + BLOCK_SIZE, y: y + BLOCK_SIZE]
                lr_patch = subsampled_img[x: x + BLOCK_SIZE, y: y + BLOCK_SIZE]
        
                lr = numpy.zeros((1, patch_size, patch_size), dtype=numpy.uint8)
                hr = numpy.zeros((1, label_size, label_size), dtype=numpy.uint8)

                lr[0, :, :] = lr_patch
                hr[0, :, :] = hr_patch[conv_side: -conv_side, conv_side: -conv_side]

                data.append(lr)
                label.append(hr)

#                 plt.imshow(lr_patch)
#                 plt.waitforbuttonpress()
#                 plt.imshow(hr_patch)
#                 plt.waitforbuttonpress()

#                 # cv2.imshow("lr", lr_patch)
#                 # cv2.imshow("hr", hr_patch)
#                 # cv2.waitKey(0)
#                 %matplotlib inline
    data = numpy.array(data, dtype=float)
    label = numpy.array(label, dtype=float)
    
    return data, label


# In[5]:


def write_hdf5(data, labels, output_filename):
    """
    This function is used to save image data and its label(s) to hdf5 file.
    output_file.h5,contain data and label
    """

    x = data.astype(numpy.uint8)
    y = labels.astype(numpy.uint8)

    with h5py.File(output_filename, 'w') as h:
        h.create_dataset('data', data=x, shape=x.shape)
        h.create_dataset('label', data=y, shape=y.shape)
        # h.create_dataset()


# In[6]:


def read_training_data(file):
    with h5py.File(file, 'r') as hf:
        data = numpy.array(hf.get('data'))
        label = numpy.array(hf.get('label'))
        train_data = numpy.transpose(data, (0, 2, 3, 1))
        train_label = numpy.transpose(label, (0, 2, 3, 1))
        return train_data, train_label

