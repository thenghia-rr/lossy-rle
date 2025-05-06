from PIL import Image

# # # Tạo ảnh 500x500
# img = Image.new('RGB', (500, 500), color=(56, 186, 207))

# # Lưu ra file
# img.save('test_images/moss.png')

# ----------Convert image to grayscale----------

# img = Image.open("test_images/1.jpg").convert("L")
# img.save("test_images/1.bmp", format="BMP")
# print("Saved mode:", Image.open("test_images/1.bmp").mode)

# -------------Check mode-------------

img1 = Image.open("test_images/moss.png")
img2 = Image.open("test_images/brave.bmp")

print("Mode moss: ", img1.mode)
print("Mode moss grayscale: ", img2.mode)


