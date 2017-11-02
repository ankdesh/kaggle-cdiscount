# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Some results###

|Base Model Name |Approach	| Num Epochs to train | Dataset description | Training acc | Val Acc |
| --- | --- | --- | --- | --- | --- |
| Inception V3 | Change top layer only | 5 | 10% random data with 80-20% val split | 0.388 | 0.371 |
| Inception V3 | Finetune with 2 top 2 inception blocks | 5 | 10% random data with 80-20% val split | 0.479 | 0.429 |
| Inception V3 | Full Retrain | 10 | 10% random data with 80-20% val split | 0.633 | 0.516 |
| Mobilenet    | Full Retrain | 10 | 10% random data with 80-20% val split | 0.58  | 0.52  |
| Mobilenet    | Finetune with 2 dense layer | 4 | 50% random data with 90-10% val split | 0.58  | 0.52  |
| Mobilenet    | Finetune with 2 dense layer | 10 | 50% random data with 90-10% val split | 0.52  | 0.52  |
| Resnet-50    | Full Retrain | 5 | 10% random data with 80-20% val split | 4.97 loss  | 4.85 (loss) |  

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact