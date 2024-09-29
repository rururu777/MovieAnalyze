import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# 画像とラベルのリスト
image_dir = './data/Movie'
labels = [18.0, 17.5, 20.0, 19.0]  # 計測したスランプ値(cm)のリスト
image_size = (224, 224)  # 画像サイズ（モデルによって異なる）

# 画像を読み込み、配列に変換
images = []
try:
    # "IOHD"で始まるディレクトリを探索
    for sub_dir in sorted(os.listdir(image_dir)):
        sub_dir_path = os.path.join(image_dir, sub_dir)
        if os.path.isdir(sub_dir_path) and sub_dir.startswith("IOHD"):
            # 各サブディレクトリ内のjpgファイルを読み込む
            for filename in sorted(os.listdir(sub_dir_path)):
                if filename.endswith(".jpg"):
                    img_path = os.path.join(sub_dir_path, filename)
                    img = load_img(img_path, target_size=image_size)
                    img_array = img_to_array(img)
                    images.append(img_array)
    
    # 正規化
    images = np.array(images, dtype="float32") / 255.0
    labels = np.array(labels, dtype="float32")

except Exception as e:
    print(f"エラー発生：{e}")
