README
>[![hackmd-github-sync-badge](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg/badge)](https://hackmd.io/2qQKhR-hRq-62aXKv4n6cg)  

worklog 
>[![hackmd-github-sync-badge](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ/badge)](https://hackmd.io/TX6rpzlaSkuiE9k3Cu-vKQ)
# Google UR multilabel forum's comment dataset
## MileStone
* labeling 1000+ sample data (6/29~)
## File structure
Google_UR_MLFC/  
　　　　|---data/　  
　　　　　　　|---Google_NLP_Crawler/　　　---Crawler script   
　　　　　　　|---raw_data/　　　　　　　　---raw data from crawler   
　　　　　　　|---multi_label_data/　　　　　---labeled data   
　　　　　　　|---utils/　　　　　　　　---utils for sampling the multi_label_data or raw_data   
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
* tips for working with github   
    1.第一次的時候 把project git clone下來->git add->git commit 你的東西->git push推上去   
    2. 之後使用一律先git pull一次 把local的版本更新到最新的 之後才開始工作   
    3. 盡量不要刪除/更改原有的目錄以避免你的版本跟其他人的版本不一致 萬一真的有需要，使用git branch後再進行更動，git branch後要怎麼跟原有的合併對我還是未知領域 *但是在原有目錄下新增目錄應該都是可以的   
    4. 總之最麻煩的就是大家的project版本都不一樣 所以再進行新的更動之前 可以先上來討論一下你的目錄結構會不會有什麼問題，最好就是一開始就把功能設計好，模組化 (但不可能 就是try and error了
