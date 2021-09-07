sshfs nlp_annotation@140.112.29.193:/home/nlp_annotation/NLP_ANNOTATION ../remote_mount_data -p 47777
python3 label.py
fusermount -u ../remote_mount_data
