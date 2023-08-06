# VidTrain

Train deep neural networks to analyze video data.

## Installation

1. [Install anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. (Optional) Install a python-capable IDE like [Visual Studio Code](https://code.visualstudio.com/)
3. Open a command line terminal to install `vidtrain`: 
   1. Create a python 3.7 environment: `conda create --name vidtrain`. Note, the python version must be >= 3.7 [[1]](#Notes)
   2. Activate the environment `conda activate vidtrain`
   3. Install tensorflow `conda install tensorflow-gpu`. Note we use conda so that all dependencies are installed as well. If you like you can manually install the tensorflow dependencies instead and skip this step (in that case pip installs tensorflow as a dependency of vidtrain in the next step).
   3. Install vidtrain `pip install vidtrain`
   
## Run

Execute the following code in python:
```python
import vidtrain


if __name__ == '__main__':
    vidtrain.workflow.JunctionAnalysis().run()
```


## Notes
[1]  The code uses some features that were introduced in 3.7 (dictionaries that are ordered by default), meaning it will not work properly with python <3.7.