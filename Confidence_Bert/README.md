# Text Classification Model for Phone Comment Category
## Traning
```
python3 train.py
```
**paramter:**
```
--dataset {G_Community, G_Community_c60}
--model {BERT, Confidence_BERT}
--batch_size 4
--epochs 5
--seed 0
--learning_rate 5e-5
--weight_decay 1e-4
#for Confidence_BERT
--lmbda 0.1
--beta 0.3
```
For example, if we want to train the BERT-Classify model with Google Community Forum Data:
```
python3 train.py --dataset G_Community --model BERT
```


## Inference
```
python3 inference.py
```
**paramter:**
```
--train_dataset {G_Community, G_Community_c60}
--model {BERT, Confidence_BERT}
--inference_data_path
```
The file you want to inference must be a csv file containing two columns("title", "content"). And the program will output a result file to ./results

If "inference_data_path" is not given, the program will evaluate the model with test.csv in "train_dataset" and print result in terminal.


## Dataset
There are two dataset in folders by default.
### G_Community
The data is crawled from [Google Pixel Community](https://support.google.com/pixelphone/community?hl=en), and we choose 7 categories as label.
#### Categories
- Battery and Power(19.11%)
- Camera(14.18%)
- Connectivity, Network, Bluetooth(25.72%)
- Contacts, Calls, Voicemail(14.46%)
- Google Assistant and Voice Actions(5.68%)
- Homescreen and Launcher(7.88%)
- Setting up and Personalizing your Device(12.97%)
#### Format
We divide the data into 3 splits (80%train, 10% validate, 10% test), which are csv file contain 3 columns("title", "content", "category")

### G_Community_c60
It's a subset of G_Community, We deduct data which confidence inference by Confidence_BERT is lower than 0.6 in G_Community.

#### Categories
- Battery and Power(21.19%)
- Camera(15.33%)
- Connectivity, Network, Bluetooth(30.79%)
- Contacts, Calls, Voicemail(17.35%)
- Google Assistant and Voice Actions(6.25%)
- Homescreen and Launcher(5.07%)
- Setting up and Personalizing your Device(4.03%)

train/val/test = 7559/895/877

### Add new Dataset
```
datasets  
│
└───G_Community
│   └── ...
│   
└───new_dataset
    ├── train.csv
    ├── validate.csv
    └── test.csv
```
In .csv file, There must be "title", "content", "category" in columns

## Model
### BERT
Stacking a linear layer to hiddenstate from [CLS] tokens
### Confidence_BERT
Reference the model architecture in <<[DeVries, Terrance, and Graham W. Taylor. "Learning confidence for out-of-distribution detection in neural networks." arXiv preprint arXiv:1802.04865 (2018).](https://arxiv.org/abs/1802.04865)>>

By adding the capability of calculating confidence score on BERT model, we successfully clean OOD/noisy data from G_Community dataset