from PIL import Image

# Tạo ảnh 500x500
img = Image.new('RGB', (500, 500), color=(56, 186, 207))

# Lưu ra file
img.save('test_images/moss_image.png')
