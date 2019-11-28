#!/bin/sh
#SBATCH -N 1  # nodes requested
#SBATCH -n 1  # tasks requested
#SBATCH --job-name=multi_meta_array
#SBATCH --gres=gpu:1
#SBATCH --mem=14000  # memory in Mb
#SBATCH --time=1-13:00:00
#SBATCH --array=1-1%1

export CUDA_HOME=/opt/cuda-9.0.176.1/

export CUDNN_HOME=/opt/cuDNN-7.0/

export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

mkdir -p /disk/scratch/${STUDENT_ID}


export TMPDIR=/disk/scratch/${STUDENT_ID}/
export TMP=/disk/scratch/${STUDENT_ID}/

mkdir -p ${TMP}/datas/
export DATASET_DIR=${TMP}/datas/
# Activate the relevant virtual environment:

source /home/${STUDENT_ID}/miniconda3/bin/activate meta_learning_pytorch_env

export DATASET_DIR="datas/"

CONFIGS=(
miniimagenet-5_way-5_shot-v0
)

echo ${CONFIGS[SLURM_ARRAY_TASK_ID-1]}

echo "---------------------Train---------------------"
# python train.py --dataset miniImagenet --model Conv4 --method relationnet_softmax --train_aug
python train.py --name_of_args_json_file configs/${CONFIGS[SLURM_ARRAY_TASK_ID-1]}.json

echo "---------------------Save features---------------------"
# python save_features.py --dataset miniImagenet --model Conv4 --method relationnet_softmax --train_aug
python save_features.py --name_of_args_json_file configs/${CONFIGS[SLURM_ARRAY_TASK_ID-1]}.json

echo "---------------------Test---------------------"
# python test.py --dataset miniImagenet --model Conv4 --method relationnet_softmax --train_aug
python test.py --name_of_args_json_file configs/${CONFIGS[SLURM_ARRAY_TASK_ID-1]}.json