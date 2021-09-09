unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo "check your enviroment... ${machine}"
echo "mount the remote data..."

sshfs nlp_annotation@140.112.29.193:/home/nlp_annotation/NLP_ANNOTATION ../remote_mount_data -p 47777

echo "execute label.py..."

python3 label.py -dp ./vocab_based/battery_data.json -op ../remote_mount_data/singlelabel_battery.json -ip ../remote_mount_data/annotated_id_battery.json

echo "unmount the remote data..."

if [[ $machine == "Linux" ]]; then
    fusermount -u ../remote_mount_data
elif [[ $machine == "Mac" ]]; then
    umount ../remote_mount_data
else
    echo "unknown OS type, failed to umount"
fi
