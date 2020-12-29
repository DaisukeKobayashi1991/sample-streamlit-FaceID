import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
import io

st.title("顔認識アプリ")

# 顔認識の準備
subscription_key = "e6dfced49c5b46ffa47f5ac198b7a09c"
assert subscription_key
face_api_url = "https://201213kobayashi.cognitiveservices.azure.com/face/v1.0/detect"

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:

    # 画像の読み込み
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリデータの取得

    headers = {
        "Content-Type" : "application/octet-stream",
        "Ocp-Apim-Subscription-Key" : subscription_key
    }
    params = {
        "returnFaceId" : "true",
        "returnFaceAttributes" : "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"   
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()

    for result in results:
        rect = result["faceRectangle"]

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect["left"], rect["top"]),(rect["left"]+rect["width"], rect["top"]+rect["height"])],fill=None, outline="red", width=3)

    # 認識した画像を出力
    st.image(img, caption="Uploded Image.", use_column_width=True)
