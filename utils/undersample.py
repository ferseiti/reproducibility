import h5py
import numpy as np
import argparse
import sys
import os

def subsample_sample(input_dir_name, output_dir_name):

    file_name = input_dir_name + 'tomo.h5'
    new_file_name = output_dir_name + 'new_tomo.h5'
    with h5py.File(file_name, 'r') as h5:
        new_h5 = h5py.File(new_file_name, 'w')
        full_data = h5['images']
        print(full_data.shape)

        new_data = full_data[::2,::4,::4]
        print(new_data.shape)
        new_h5.create_dataset('images', data=new_data)
        new_h5.close()

def subsample_support_files(input_dir_name, output_dir_name):

    file_names = os.listdir(input_dir_name)
    tomos = []

    os.makedirs(output_dir_name, exist_ok=True)

    for f in file_names:
        if 'h5' in f and not f == 'tomo.h5':
            tomos.append(f)

    print(tomos)
    for g in tomos:
        with h5py.File(input_dir_name + g, 'r') as h5:
            key = list(h5.keys())[0]
            print(h5[key].shape)

            new_h5 = h5py.File(output_dir_name + g, 'w')
            full_data = h5[key]
            new_data = full_data[:,::4,::4]

            print(new_data.shape)
            new_h5.create_dataset(key, data=new_data)
            new_h5.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Subsample tomography raw files \
                               to 1/4 of the original image sizes and half the angles.')
    parser.add_argument('-i', '--input', help='Input directory \
                        where the original file is located.', required=True)
    parser.add_argument('-o', '--output', help='Output directory \
                        where the result will be written to.', required=True)
    arguments = parser.parse_args()

    subsample_support_files(arguments.input, arguments.output)
    subsample_sample(arguments.input, arguments.output)
