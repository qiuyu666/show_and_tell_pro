
#!/usr/bin/env bash

export USER=qiuyu
export py2env=/home/dixin/python/py2env/bin/activate
export HOME=/home/${USER}/im2txt

today_time=$(date --date="0 day" +"%m%d")
yesterday_time=$(date --date="-1 day" +"%m%d")
last_time=$(date --date="-2 day" +"%m%d")
visit_date=$(date --date="0 day" +"%Y%m%d")
last_date=$(date --date="-1 day" +"%Y%m%d")


# Directory containing preprocessed MSCOCO data.
MSCOCO_DIR="/home/qiuyu/zhuye_look_comment_data"
if [ ! -d "${MSCOCO_DIR}" ]; then
  mkdir ${MSCOCO_DIR}
fi
# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="${HOME}/im2txt/data/inception_v3/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${HOME}/im2txt/zhuye_look_comment_model"



# JPEG image file to caption.
IMAGE_FILE="/home/qiuyu/zhuye_look_comment_data/val_data/"
OUT_FILE="/home/qiuyu/comment_test/result"
cd ${HOME}




gpu=1


cd  ${HOME}
source ${py2env}

#inference stage
# Run inference to generate captions.
CUDA_VISIBLE_DEVICES=${gpu}  python -m  im2txt.run_inference_origin \
  --checkpoint_path="${MODEL_DIR}/train" \
  --vocab_file="${MSCOCO_DIR}/word_counts.txt" \
  --input_files=${IMAGE_FILE} \
  --output_file="${OUT_FILE}/zhuye_test_result.txt"
