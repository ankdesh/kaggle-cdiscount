# README #

### What is this repository for? ###

This repo contains all the code, original or copied(respecting the License conditions) that I used for competing for 
Kaggle's Cdiscount competition (https://www.kaggle.com/c/cdiscount-image-classification-challenge)

### How do I get set up? ###
I used the docker shared at DevSetup/Dockerfiles/cuda-py/Dockerfile.cuda.bash as the setup environment. TF and Keras
are the major requirements

### Some results ###

|Base Model Name |Approach	| Num Epochs to train | Dataset description | Training acc | Val Acc |
| --- | --- | --- | --- | --- | --- |
| Inception V3 | Change top layer only | 5 | 10% random data with 80-20% val split | 0.388 | 0.371 |
| Inception V3 | Finetune with 2 top 2 inception blocks | 5 | 10% random data with 80-20% val split | 0.479 | 0.429 |
| Inception V3 | Full Retrain | 10 | 10% random data with 80-20% val split | 0.633 | 0.516 |
| Mobilenet    | Full Retrain | 10 | 10% random data with 80-20% val split | 0.58  | 0.52  |
| Mobilenet    | Finetune with 2 dense layer | 4 | 50% random data with 90-10% val split | 0.58  | 0.52  |
| Mobilenet    | Finetune with 2 dense layer | 10 | 50% random data with 90-10% val split | 0.52  | 0.52  |
| Resnet-50    | Full Retrain | 5 | 10% random data with 80-20% val split | 4.97 loss  | 4.85 (loss) |  
| Resnet-50    | Finetune with 2 dense layer | 3 | 50% random data with 90-10% val split | 0.43  | 0.44 |  
| Resnet-101   | Finetune with 2 dense layer | 7 | 50% random data with 90-10% val split | 0.55  | 0.55 |
| Resnet-101   | Finetune with last few Conv layers | 6 | 50% random data with 90-10% val split | 0.65  | 0.61 |
