# export TESSDATA_PREFIX="$(pwd)/tessdata"
rm -rf tesstrain
git clone https://github.com/tesseract-ocr/tesstrain.git
cd tesstrain
make tesseract-langdata
cp -r "../images/" "data/hsr-ground-truth"
mkdir -p usr/share/tessdata
cp "../tessdata/DIN-Alternate.traineddata" usr/share/tessdata
cp "../tessdata/eng.traineddata" usr/share/tessdata
make training MODEL_NAME=hsr START_MODEL=DIN-Alternate FINETUNE_TYPE=Impact