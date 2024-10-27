import cv2
import numpy as np
import streamlit as st
from PIL import Image

# ส่วนการอัปโหลดภาพ
st.title("ตรวจจับบรรจุภัณฑ์อาหารจากความแตกต่างของสี")

uploaded_file = st.file_uploader("อัปโหลดภาพที่ต้องการตรวจสอบ", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # โหลดภาพจากการอัปโหลดและแปลงเป็น RGB
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # แปลงภาพเป็น Grayscale เพื่อให้ตรวจจับขอบได้ง่ายขึ้น
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # คำนวณค่าเฉลี่ยของสีในภาพเพื่อใช้เป็นสีพื้นหลัง
    background_color = np.mean(gray_image)

    # ตรวจจับบริเวณที่มีสีแตกต่างจากพื้นหลัง
    _, mask = cv2.threshold(gray_image, background_color - 20, 255, cv2.THRESH_BINARY_INV)

    # ใช้การค้นหา Contours เพื่อหาโซนที่แตกต่างจากพื้นหลัง
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ค้นหา contour ที่มีพื้นที่มากที่สุด
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # วาดกรอบสี่เหลี่ยมรอบบริเวณที่ใหญ่ที่สุด
    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # แปลงกลับเป็น RGB เพื่อแสดงใน Streamlit
    image_result = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    st.image(image_result, caption="ผลลัพธ์หลังการตรวจจับบรรจุภัณฑ์ที่ใหญ่ที่สุด", use_column_width=True)
