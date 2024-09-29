'''
1フレーム抽出するだけでよいのか疑問アリ。1秒間にも複数枚のフレームがあるから。
しかし、そのくらいの粒度でもよいのであれば問題ない（1秒程度ではスランプ値に変動がない場合）
'''
def ExtractToFrame(movie_path, sec_time):
    import cv2
    import os   

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
    # 対象フレームの定義
    target_frame = int(fps * sec_time)
    # 対象フレームにシーク
    capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    # フレームを1つ読み込み
    ret, frame = capture.read()
    if ret:
        # 画像ファイル名を作成
        image_filename = os.path.join(output_dir, f'frame_{target_frame}.jpg')
        # フレームを画像として保存
        cv2.imwrite(image_filename, frame)
        print(f"フレーム {target_frame} を画像として保存しました: {image_filename}")
    else:
        print(f"フレーム {target_frame} を読み込むことができませんでした。")
    
    # リソースの解放
    capture.release()
    cv2.destroyAllWindows()
