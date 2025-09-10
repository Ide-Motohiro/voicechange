import pyaudio
import numpy as np

# --- 基本設定 ---
CHUNK = 1024 * 2             # 一度に処理する音声のサイズ
FORMAT = pyaudio.paInt16     # 音声のフォーマット
CHANNELS = 1                 # チャンネル数 (1:モノラル, 2:ステレオ)
RATE = 44100                 # サンプリングレート (Hz)

# PyAudioのインスタンスを作成
p = pyaudio.PyAudio()

# ストリーム（音声の流れ）を開く
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,         # 入力を有効にする
                output=True,        # 出力を有効にする
                frames_per_buffer=CHUNK)

print("マイクの音をそのまま出力します。終了するにはCtrl+Cを押してください。")

try:
    # ストリームが有効な間、ループを続ける
    while stream.is_active():
        # マイクから音声データを読み込む
        input_data = stream.read(CHUNK)
        
        # --- ここに声を変える処理を書く ---
        # 今回はまだ何もしない
        output_data = input_data
        
        # スピーカーに音声データを出力する
        stream.write(output_data)

except KeyboardInterrupt:
    # Ctrl+Cが押されたら終了
    print("終了します。")

finally:
    # ストリームを閉じる
    stream.stop_stream()
    stream.close()
    p.terminate()