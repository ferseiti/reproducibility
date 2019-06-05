# ia369z
## Data

The data being read within data_management.ipynb, for now, can be found at:
https://figshare.com/s/c6fc5e1fdb95999c9402

All the files from the url above with h5 extension should be downloaded into
the directory data/ia369z/Palito/

The reconstructed tomographies can be found at the following url:
https://figshare.com/s/586be72211bcf4a174cb

The data above should be downloaded into the directory data/ia369z/Palito/recon

### Dependencies

Please set your environment to run on Python3, since this project was written
and tested to run under Python3.

You might need to install the following dependencies in order to run this
project:

- numpy
- h5py
- matplotlib
- scipy==1.1.0
- tensorflow
- keras
- opencv-python

In order to install them, you can simply run:
```
pip3 install -v numpy h5py matplotlib tensorflow keras opencv-python scipy==1.1.0
```

### Running the paper

One must start an instance of jupyter notebook on the root directory of their local copy of this repository.
Then, change directory to 'deliver' and open the file Final_Version.ipynb.
From then on, the notebook should run.

### What the notebook executes

The notebook named Final_Version.ipynb runs the report of the experiments on the data and displays some of the predictions, as well as the ground truth of the test data.

The slice from where the prediction will run can be chosen. An additional of 50 slices will then be also included in the prediction and visualization of the result.

## Workflow

<img src="figures/workflow.png" />
