import pyaudio
import numpy as np

# --- 基本設定 ---
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PITCH_RATE = 1.2  # ★声を変える倍率（この数字を変えて遊んでみよう！）

# PyAudioのインスタンスを作成
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print(f"ピッチを{PITCH_RATE}倍にして出力します。終了するにはCtrl+Cを押してください。")

try:
    while stream.is_active():
        # マイクから音声データを読み込む
        input_data = stream.read(CHUNK)
        
        # --- 声を変える処理 ---
        # 1. 音声データを数値の配列に変換
        np_data = np.frombuffer(input_data, dtype="int16")
        
        # 2. 音の再生位置を計算し直す（リサンプリング）
        x = np.arange(CHUNK)  # 元の再生位置
        x_new = np.linspace(0, CHUNK, int(CHUNK / PITCH_RATE)) # 新しい再生位置
        
        # 3. 新しい再生位置に合わせて音を補間し、新しい音声データを作成
        np_data_new = np.interp(x, x_new, np_data)
        
        # 4. 数値の配列をバイナリデータに戻す
        output_data = np_data_new.astype("int16").tobytes()
        
        # スピーカーに音声データを出力する
        stream.write(output_data)

except KeyboardInterrupt:
    print("終了します。")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()