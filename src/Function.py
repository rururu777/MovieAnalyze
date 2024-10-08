def ExtractToFrame(movie_path, start_time, end_time):
    import cv2
    import os   

    try:    
        # 抽出したフレームを保存するディレクトリパスを定義
        basesname = os.path.splitext(os.path.basename(movie_path))[0]
        arg_dirname, arg_filename = os.path.split(movie_path)
        output_dir = os.path.join(arg_dirname, basesname)
        # ディレクトリ作成
        os.makedirs(output_dir, exist_ok=True)

        # 動画を読み込む
        capture = cv2.VideoCapture(movie_path)
        # 動画のフレームレートを取得
        fps = capture.get(cv2.CAP_PROP_FPS)
        # 開始フレームと終了フレームを定義
        start_frame = int(fps * start_time)
        end_frame = int(fps * end_time)
        # 開始フレームにシーク
        capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # フレームを切り抜いて保存
        for frame_count in range(start_frame, end_frame):
            # フレームを1つ読み込み
            ret, frame = capture.read()
            if not ret:
                break

            # 画像ファイル名を作成
            image_filename = os.path.join(output_dir, f'frame_{frame_count}.jpg')
            # フレームを画像として保存
            cv2.imwrite(image_filename, frame)
        
        # リソースの解放
        capture.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"ExtractToFrame関数でエラーが発生しました：{e}")

def ExtractFramesFromMultipleVideos(sec_ranges):
    import os

    try:
        # 動画が保存されいてるディレクトリのパス
        directory = "../data/Movie"
        # ディレクトリ内の動画ファイルを取得
        video_files = sorted([f for f in os.listdir(directory) if f.endswith(".MP4")])
        # 引数の秒数リストと動画ファイルの数が一致しているかを確認
        if len(video_files) != len(sec_ranges):
            print("動画の数と秒数のリストの要素数が一致していません")
            print(f"動画の数：{len(video_files)}、秒数のリスト：{len(sec_ranges)}")
            return
        
        # 各動画に対してフレームを抽出
        for video_file, (start_time, end_time) in zip(video_files, sec_ranges):
            video_path = os.path.join(directory, video_file)
            ExtractToFrame(video_path, start_time, end_time)
            
    except Exception as e:
        print(f"ExtractFramesFromMultipleVideos関数でエラーが発生しました：{e}")

def PrepareData():
    import os
    import numpy as np
    from tensorflow.keras.preprocessing.image import load_img, img_to_array

    # 画像とラベルのリスト
    image_dir = '../data/Movie'
    labels = [18.0, 17.5, 20.0, 19.0]  # 計測したスランプ値(cm)のリスト
    input_shape = [256, 256, 3]  # 縦横256pxのカラー画像を入力形式として定義

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
                        img = load_img(img_path, target_size=input_shape)
                        img_array = img_to_array(img)
                        images.append(img_array)
        
        # 正規化
        images = np.array(images, dtype="float32") / 255.0
        labels = np.array(labels, dtype="float32")

    except Exception as e:
        print(f"PrepareData()関数でエラーが発生しました：{e}")

def LoadToModel(model_dir):
    from tensorflow.keras.models import model_from_json
    from tensorflow.keras import optimizers
    import os

    try:
        model_path = os.path.join(model_dir, "model.json")
        param_path = os.path.join(model_dir, "weight.weights.h5")
        # モデルの読み込み
        model = model_from_json(open(model_path, "r").read())
        # 重みの読み込み
        model.load_weights(param_path)
        # Sequentialオブジェクトのコンパイル
        model.compile(loss="binary_crossentropy",
                        optimizer=optimizers.Adam(0.001), metrics=["accuracy"])
        
        return model
    
    except Exception as e:
        print(f"LoadToModel()関数でエラーが発生しました：{e}")
    
def ResultToPredict(target_dir, model):
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    import numpy as np
    import os

    try:
        # 入力データの形状
        input_shape = [256, 256, 3]
        # 画像データの数値データを格納する配列
        target_array = []

        # ディレクトリ内のjpgファイルを読み込む
        for filename in sorted(os.listdir(target_dir)):
            if filename.endswith(".jpg"):
                img_path = os.path.join(target_dir, filename)
                img = load_img(img_path, target_size=input_shape)
                img_array = img_to_array(img) 
                img_array = np.expand_dims(img_array, axis=0)
                img_array /= 255.0
                target_array.append(img_array)

        target_array = np.array(target_array, dtype="float32")

        # カウンタ
        cnt_True = 0
        cnt_False = 0

        # 対象ディレクトリの画像全てを予測
        for i in range(len(target_array)):
            prediction = model.predict(target_array[i])
            if(prediction[0][0] > 0.5):
                cnt_True += 1
            else:
                cnt_False += 1

        # 予測結果の出力
        print(f"True：{cnt_True}")
        print(f"False：{cnt_False}")
    except Exception as e:
        print(f"ResultToPredict()関数でエラーが発生しました：{e}")