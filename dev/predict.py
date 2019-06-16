from keras.models import Sequential
from keras.layers import Conv2D, Input
from keras.callbacks import ModelCheckpoint, Callback
from keras.optimizers import SGD, Adam
from keras.utils.training_utils import multi_gpu_model
from keras.preprocessing.image import ImageDataGenerator
from keras import initializers

import h5py

from skimage import data, img_as_float
from skimage.measure import compare_ssim as ssim

import prepare_data as pd
import numpy
import math
import scipy.misc as spm

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from lr_multiplier import LearningRateMultiplier

import matplotlib
matplotlib.rc('image', cmap='gray')

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
from keras.backend.tensorflow_backend import set_session
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.2
# set_session(tf.Session(config=config))


def mse(x, y):
    return numpy.linalg.norm(x - y)



def psnr(target, ref):

    target_data = numpy.array(target, dtype=float)
    ref_data = numpy.array(ref, dtype=float)

    diff = ref_data - target_data
    diff = diff.flatten('C')

    rmse = math.sqrt(numpy.mean(diff ** 2.))

    return 20 * math.log10(255. / rmse)


def predict_model(network='9-3-5'):

    sgd = SGD(lr=0.0001)
    
    if network == '9-1-5':
        k = 1
    elif network == '9-3-5':
        k = 3
    else:
        k = 5
    
    SRCNN = Sequential()
    SRCNN.add(Conv2D(filters=128, kernel_size=(9, 9), 
                     kernel_initializer='glorot_uniform', bias_initializer='random_uniform',
                     activation='relu', padding='valid', use_bias=True, input_shape=(None, None, 1), name='conv2d_1'))
    
    SRCNN.add(Conv2D(filters=64, kernel_size=(k, k), 
                     kernel_initializer='glorot_uniform', bias_initializer='random_uniform',
                     activation='relu', padding='same', use_bias=True, name='conv2d_2'))
        
    
    SRCNN.add(Conv2D(filters=1, kernel_size=(5, 5), 
                     kernel_initializer='glorot_uniform', bias_initializer='random_uniform',
                     activation='linear', padding='valid', use_bias=True,  name='conv2d_3'))
    adam = Adam(lr=0.0003)
    sgd_last = SGD(lr=0.00001)

    SRCNN.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])
    return SRCNN


def read_data(file):
    with h5py.File(file, 'r') as hf:
        data = numpy.array(hf.get('data'))
        return data


def remove_keymap_conflicts(new_keys_set):

    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)
                
def multi_slice_viewer(volume1, volume2):

    remove_keymap_conflicts({'up', 'down', 'j', 'k'})
    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.set_figheight(5)
    fig.set_figwidth(8)
    
    ax[0].volume = volume1
    ax[0].index = volume1.shape[0] // 2
    ax[0].imshow(volume1[ax[0].index])
    
    ax[1].volume = volume2
    ax[1].index = volume2.shape[0] // 2
    ax[1].imshow(volume2[ax[1].index])
    
    fig.canvas.mpl_connect('scroll_event', process_key)
    fig.canvas.mpl_connect('key_press_event', process_key)

def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0], fig.axes[1]
    if event.key == 'k' or event.button == 'up':
        previous_slice(ax[0])
        previous_slice(ax[1])
    elif event.key == 'j' or event.button == 'down':
        next_slice(ax[0])
        next_slice(ax[1])
    fig.canvas.draw()

def previous_slice(ax):
    volume = ax.volume
    plt.title('Slice {}'.format(ax.index))
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    ax.images[0].set_array(volume[ax.index])

def next_slice(ax):
    volume = ax.volume
    plt.title('Slice {}'.format(ax.index))
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])
    
def show_slice(slice_num=256, amount_slices=20, gt_data='../data/ground_data/ground_data_pen.h5', data='../data/sub_data/sub_data_pen.h5'):

    first_slice = slice_num
    last_slice = slice_num + amount_slices
    
    srcnn_model = predict_model('9-3-5')
    srcnn_model.load_weights("../data/model/64-9-3-5_128-64-SRCNN_model_at_epoch_300.h5")

    data = read_data(data)

    label = read_data(gt_data)

    interpolated_data = numpy.empty((512, 512, 512, 1))
    for i in range(data.shape[0]):
        interpolated_data[i,:,:,0] = spm.imresize(data[i,:,:], size=(512, 512), interp='bicubic')

    data_shape = interpolated_data.shape
    label_shape = label.shape

    prediction = srcnn_model.predict(interpolated_data[first_slice:last_slice, data_shape[1]//4:-(data_shape[1]//4), data_shape[2]//4:-(data_shape[2]//4),:])
    
    plt.figure(figsize=[15, 13])
    plt.subplot(221)
    plt.title('Prediction')
    plt.imshow(prediction[0, :, :, 0])
    plt.subplot(222)
    plt.title('Interpolated')
    plt.imshow(interpolated_data[slice_num, data_shape[1]//4:-(data_shape[1]//4), data_shape[2]//4:-(data_shape[2]//4),0])
    plt.subplot(223)
    plt.title('Ground truth')
    plt.imshow(label[slice_num, label_shape[1]//4:-(label_shape[1]//4), label_shape[2]//4:-(label_shape[2]//4)])
    plt.show()

    return prediction, label[first_slice:last_slice, label_shape[1]//4:-(label_shape[1]//4), label_shape[2]//4:-(label_shape[2]//4)], interpolated_data[first_slice:last_slice ,data_shape[1]//4:-(data_shape[1]//4), data_shape[2]//4:-(data_shape[2]//4),0]

def bigshow(img=numpy.zeros((100,100)), title='Image', size=12):
    plt.figure(figsize=[size, size])
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.show()
