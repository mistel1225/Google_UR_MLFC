README
>[![hackmd-github-sync-badge](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg/badge)](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg)  

worklog 
>[![hackmd-github-sync-badge](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ/badge)](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ)
# Google UR multi-label forum's comment dataset
## MileStone
* labeling 1000+ sample data (6/29~)
    * working on label.py(7/7~)
        * enter the error correction phase(7/12~7/14)
        * the current funtionality doesn't support more than two people labeling data at the same time(see worklog.md)
    * data annotation(7/14~)   

## Bug report
To report any bug or suggestion, please post an issue and apply following format.  
* program bug  
    1. error program or code.
    2. the input that leads to the bug.
    3. the output coming with the input.
* problem of label  
    1. the data id that you think is wrong
    2. the label that should be corrected
    3. the recommendation label
    4. the recommendation span
* recommendation
    1. anything that you recommend to improve.
## Contribute to this project
here is some way to contribute this project
* Bug report
    * please refer to the Bug report segmentation.
* Label annotation
    * usage: python3 ./data/utils/label.py
* Label verfication(not available yet)
    * usage: python3 ./data/utils/label.py --mode verify
## Directory structure
Google_UR_MLFC/  
　　　　|---data/　  
　　　　　　　|---Google_NLP_Crawler/　　　---Crawler script   
　　　　　　　|---raw_data/　　　　　　　　---raw data from crawler   
　　　　　　　|---multi_label_data/　　　　　---labeled data   
　　　　　　　|---utils/　　　　　　　　---utils for sampling the multi_label_data
        or raw_data   
　　　　　　　　　　|---label.py  
　　　　|---baseline_model/  
　　　　|---README.md  
　　　　|---.gitignore  
## Multi-label Multi-span Dataset
* formation  
 multi-label  
 multi-span
* label  

## Some note
* sync README.md with hackmd  
https://hackmd.io/c/tutorials-tw/%2Fs%2Flink-with-github-tw
* link to the issue number on Github within a commit message
https://stackoverflow.com/questions/1687262/link-to-the-issue-number-on-github-within-a-commit-message
