# ia369z

## Environment

This work was mostly developed and executed within the following environment settings:

```
Python 3.6.5

pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)

Distributor ID:	Ubuntu
Description:	Ubuntu 18.04 LTS
Release:	18.04
Codename:	bionic

Docker version 17.12.1-ce, build 7390fc6
```

This repository was also tested in mybinder environment, but did not run, due to its heavy processing. You could give it a try!

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ferseiti/reproducibility/master)

## Data

The notebook within deliver/Final_Version.ipynb downloads the data in a tarball and extracts it within the working directory. If that does not work, one can try and download them manually from figshare, using one of the following sources:

* The data.tar.gz that contains plotting info and 2 samples (basically this repository's data directory):
https://ndownloader.figshare.com/files/15483431

* If one wishes to download the h5 separately, the data are all available within this project in figshare:
https://figshare.com/account/home#/projects/64340

The files named ground* must be downloaded within data/ground_data/ and the ones named sub*, within data/sub_data/

If you are using the docker environment, it contains the data.tar.gz, so there is no need to download it.

## Dependencies

Please set your environment to run on Python3, since this project was written
and tested to run under Python3.

You might need to install the following dependencies in order to run this
project:

- scikit-image
- numpy
- h5py
- matplotlib
- scipy==1.1.0
- tensorflow
- keras
- opencv-python
- requests

In order to install them, you can simply run:
```
pip3 install -v requests numpy h5py matplotlib tensorflow keras opencv-python scikit-image scipy==1.1.0
```

## Running the paper

One must start an instance of jupyter notebook on the root directory of their local copy of this repository.
Then, change directory to 'deliver' and open the file Final_Version.ipynb.
From then on, the notebook should run.

## What the notebook executes

The notebook named deliver/Final_Version.ipynb runs the report of the experiments on the data and displays some of the predictions, as well as the ground truth of the test data.

The slice from where the prediction will run can be chosen. As default, an additional of 20 slices will then be also included in the prediction and visualization of the result. This can also be changed, but be aware that it might be demanding on your hardware.

For the following configuration:

```
Intel(R) Core(TM) i7-3630QM CPU @ 2.40GHz
              total        used        free      shared  buff/cache   available
Mem:           7,7G        2,4G        3,4G        744M        1,9G        4,3G
Swap:           14G        2,0G         12G
```
The program was not able to run for more than 25 additional slices.

### Training the Network

It is possible to run the training. The notebook within deliver/train-9-3-5-64.ipynb does so for the results presented.

The training was executed on a server with 8 NVIDIA V100-32GB and the following setup:
```
Intel(R) Xeon(R) Gold 6134 CPU @ 3.20GHz

              total        used        free      shared  buff/cache   available
Mem:           1.0T        2.8G         96G         35M        908G        1.0T
Swap:          975M        3.5M        972M
```

## Docker

This work can be executed in a docker environment, with no previous dependencies, other than docker-ce (or docker.io) on your machine.

In order to run in a docker, with docker installed on your machine, this can be run like so:

```
docker run -it --rm -p 12345:8888 -v $PWD:/home ferseiti/jupyter:reproducible
```

Then, just access, through your browser, the address http://localhost:12345.

Note that the port 12345 can be changed if 1234 is already in use by your OS.

## Workflow

<img src="figures/workflow.png" />
