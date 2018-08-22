
#!/usr/bin/env bash

export USER=qiuyu
export py2env=/home/dixin/python/py2env/bin/activate
export HOME=/home/${USER}/im2txt/

today_time=$(date --date="0 day" +"%m%d")
yesterday_time=$(date --date="-1 day" +"%m%d")
last_time=$(date --date="-2 day" +"%m%d")
visit_date=$(date --date="0 day" +"%Y%m%d")
last_date=$(date --date="-1 day" +"%Y%m%d")


# Directory containing preprocessed MSCOCO data.
MSCOCO_DIR="/home/qiuyu/textcnn_generate_data"
if [ ! -d "${MSCOCO_DIR}" ]; then
  mkdir ${MSCOCO_DIR}
fi
# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="${HOME}/im2txt/data/inception_v3/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${HOME}/im2txt/generate_model"



# JPEG image file to caption.
IMAGE_FILE="${HOME}/im2txt/data/mscoco/val2014/COCO_val2014_000000224477.jpg"


gpu=2


cd  ${HOME}
source ${py2env}
#evaluate
CUDA_VISIBLE_DEVICES=${gpu} python -m im2txt.evaluate \
  --input_file_pattern="${MSCOCO_DIR}/tfrecord_data/val-?????-of-00004" \
  --checkpoint_dir="${MODEL_DIR}/train" \
  --eval_dir="${MODEL_DIR}/eval"


#inference stage
# Run inference to generate captions.
#CUDA_VISIBLE_DEVICES=${gpu}  python -m  im2txt.run_inference \
#  --checkpoint_path=${CHECKPOINT_PATH} \
#  --vocab_file=${VOCAB_FILE} \
#  --input_files=${IMAGE_FILE}
