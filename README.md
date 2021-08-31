README
>[![hackmd-github-sync-badge](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg/badge)](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg)  

# Google UR with NTU BDS Lab: multi-label forum's comment dataset

## MileStone
* labeling 1000+ sample data (6/29~)
    * working on label.py(7/7~7/16)
        * enter the error correction phase(7/12~7/14)
        * the current funtionality doesn't support more than two people labeling data at the same time(see worklog.md)(done at 7/14)
    * data annotation(7/19~8/1)  
* use rule-based method to collect data
     * currently collect 20000+ labeled data based on rule-based method(please refer to the weekly progress slide on 8/17 [here](https://docs.google.com/presentation/d/12pQ2_DL7lQkqaZgFKNTR70FIpBuVj78-EhZLm5ak6fk/edit#slide=id.gec59da25bc_0_10))
## Important Link
* proposal  
    * [Multi-Label Classification for Forum Comments](https://docs.google.com/document/d/1zJ4aa-ic6tEgruDsbcMaHiqyLOqGNLlz90la3FaVBCo/edit)
*  weekly progress slide
    *  [Google UR with NTU BDS Lab - NLP](https://docs.google.com/presentation/d/12pQ2_DL7lQkqaZgFKNTR70FIpBuVj78-EhZLm5ak6fk/edit#slide=id.p)

## Bug report
To report any bug or suggestion, please post an issue and apply following format.  
* program bug  
    1. error program or code.
    2. the input that leads to the bug.
    3. the output coming with the input.
* problem of label  
    1. the wrong data id
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
    * dependency: sshfs
        * Linux, Mac, Windows: https://blog.gtwang.org/linux/sshfs-ssh-linux-windows-mac-os-x/   
    * In this version, we expect the data is located at 140.112.29.201:/home/NLP_annotation/NLP_DATA, and label.py should have to provide multiple annotation at the same time without corruption or overwriting.  
    * For labeling, please follow the instruction below  
    ```bash
    ##usage:
    cd data/utils
    bash ./sshfs.sh
    python3 ./label.py
    ##for labeling on local site
    cd data/utils
    python3 label.py -dp ../raw_data/data1000.json -ip ./annotated_id.json -lp ./data_label.json -op ../multi_label_data/data1000label.json
    ```
* Label verfication(not available yet)
    * usage: python3 ./data/utils/label.py --mode verify
## Directory structure
Google_UR_MLFC/  
　　　　|---data/　  
　　　　　　　|---Google_NLP_Crawler/　　　---Crawler script   
　　　　　　　|---raw_data/　　　　　　　　---raw data from crawler   
　　　　　　　　　　|---data35000.json   
　　　　　　　　　　|---reddit5843.csv   
　　　　　　　　　　|---samsungdata.json   
　　　　　　　|---multi_label_data/　　　　　---labeled data   
　　　　　　　|---utils/　　　　　　　　---utils for sampling the multi_label_data
        or raw_data   
　　　　　　　　　　|---label.py  
　　　　|---baseline_model/  
　　　　|---README.md  
　　　　|---.gitignore  
## Multi-label Dataset
* label structure  
    * Hardware Components  
        1. battery (Draining, Swelling, Percentage)  
        2. internet (Wifi / LTE / Hotspot)  
        3. bluetooth (Pair)  
        4. usb/type-c (Port, warning about water in port)  
        5. camera (Lense, Photo, Video)  
        6. sIM/ eSIM  
        7. screen(Display, Touch)  
        8. appearance (power button, )  
        9. storage(File, Drive, SDcard, transfer)  
        10. speaker  
        11. headphone (bluetooth headphone=3+9, usb headphone=4+9)  
    * Software App && Services
        1. software/system Update (Security Update, Android Update)
        2. google app(virtual assistance, chrome, gmail, map, youtube...)
        3. third party app (whatsapp...)
        4. account(sync, find account)
        5. boot(bootloop, can't boot, system failure...)
        6. backup
        7. virtual assistance
    * Function Feature
        1. communication(Call / Contact/ Text Message/ Voicemail / Screen call)  
        2. multimedia (photo, video, video playing...)  
        3. audio / Voice (volume/music player)  
        4. security (Face recognition, Screen Lock, Password)  
        5. gps (Location)  
        6. device connection(TV casting/pc connect/smart device.../external device)  
        7. system service(settings, launcher, keyboard, ui, screenshot)  
        8. notification  
    * Feedback type  
        1. setup(how to...)  
        2. feature request and suggestion(suggestion, feedback)  
        3. customer service  
    * Stability  
        1. stability(crash for no reason, shutdown, overheat)  
    * other  
        1. other  
        2. useless  
## Some note  
* sync README.md with hackmd  
https://hackmd.io/c/tutorials-tw/%2Fs%2Flink-with-github-tw
* link to the issue number on Github within a commit message
https://stackoverflow.com/questions/1687262/link-to-the-issue-number-on-github-within-a-commit-message
