import pyttsx3			# pip install pyttsx3

# 初始化引擎
engine = pyttsx3.init()

# 设置属性
engine.setProperty('rate', 150)    # 语速
engine.setProperty('volume', 0.9)  # 音量 (0-1)

# 获取可用的语音
voices = engine.getProperty('voices')

# 设置中文语音（如果有的话）
for voice in voices:
    if 'chinese' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# 文本转语音
text = "你好，这是一个文本转语音的示例。"
engine.say(text)
engine.runAndWait()