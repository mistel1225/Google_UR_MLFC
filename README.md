README
>[![hackmd-github-sync-badge](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg/badge)](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg)  

worklog 
>[![hackmd-github-sync-badge](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ/badge)](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ)
# Google UR multi-label forum's comment dataset
## MileStone
* labeling 1000+ sample data (6/29~)
    * working on label.py(7/7~)
        * enter the error correction phase(7/12~7/14)
        * the current funtionality doesn't support more than two people labeling data at the same time(see worklog.md)(done at 7/14)
    * data annotation(7/19~)   

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
    1. Battery / Charging (Draining, Swelling, Percentage)  
    2. Internet (Wifi / LTE / Hotspot)  
    3. Bluetooth (Pair)  
    4. USB/Type-C (Port, 有水在裡面相關的警告訊息)  
    5. Device Connection(TV casting/pc connect/smart device.../external device)(難)  
    6. Software/System Update (Security Update, Android Update)  
    7. Screen/Touch screen (Display, Touch)  
    8. Virtual Assistance  
    9. Headphone (藍芽耳機:3+9, usb耳機:4+9)  
    10. Audio / Voice (microphone/speaker, Volume)  
    11. App (3rd)(難) (或是拆開成google app/ third party app)(email)  
    12. Notification (Do Not Disturb, Alarm, Ringtone, Notification bar)  
    13. Camera/ Multimedia (Lense, Photo, Video)  
    14. SIM/ eSIM  
    15. Communication(Call / Contact/ Text Message/ Voicemail / Screen call)  
    16. Account (同步問題，找帳號)  
    17. Security (Face recognition, Screen Lock, Password)  
    18. Boot (Bootloop, Can't not boot, system failure)  
    19. Storage(File, Drive, SDcard)  
    20. Backup  
    21. Set up(How to ..., 跟上面邏輯不太一樣)  
    22. GPS (Location)  
    23. User Interface(Homescreen, Wallpaper, Swipe)  
    24. Feature Request (Suggestion, Feedback)  
    25. Appearance (power button, )  
    26. Other  
    27. Useless  
## Some note
* sync README.md with hackmd  
https://hackmd.io/c/tutorials-tw/%2Fs%2Flink-with-github-tw
* link to the issue number on Github within a commit message
https://stackoverflow.com/questions/1687262/link-to-the-issue-number-on-github-within-a-commit-message
