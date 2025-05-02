# ĐỒ ÁN KẾT THÚC MÔN KHAI PHÁ DỮ LIỆU

Đề tài: Áp dụng kĩ thuật Lossy RLE trong nén ảnh và giải nén ảnh

Mô tả: Dự án này cung cấp giao diện web đơn giản để **nén** và **giải nén ảnh RGB** bằng kỹ thuật **Run-Length Encoding (RLE)** được tùy chỉnh, gọi là **Lossy RLE**.

## Tính năng chính (Core functionality)

- Nén ảnh RGB thành định dạng `.rle` với thuật toán Lossy RLE.
- Giải nén file `.rle` và phục hồi lại ảnh gốc.
- Hiển thị thông tin kích thước và tỷ lệ nén.
- Tải ảnh sau nén hoặc ảnh đã giải nén.
- Giao diện dễ sử dụng [Streamlit](https://streamlit.io/).

## Công nghệ sử dụng (Tech stack)

- Python 3.10
- [Streamlit](https://streamlit.io/)
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
- Pickle (lưu file nhị phân)

## Cấu trúc dự án (Folder structure)

```bash
📂 lossy-rle/
├── app.py                  # File chính chạy ứng dụng Streamlit
├── create_img_test.py      # File tạo ảnh sample theo RGB
├── README.md               # Tài liệu mô tả dự án
├── 📁 test_images/         # Thư mục chứa ảnh mẫu
├── 📁 compressed_images/   # Ảnh đã nén (.rle)
│   📁 restored_images/     # Ảnh đã giải nén (.png, .jpg, ...)
└── requirements.txt        # Danh sách thư viện cần cài đặt
```

## Giao diện (GUI)
### 1. Giao diện chứa chức năng nén và giải nén
![](test_images\projects\1.png)

### 2. Giao diện kết quả sau khi nén
![](test_images\projects\2.png)

### 3. Giao diện visualize trực quan
![](test_images\projects\3.png)

## Cách dùng (Usage)

1. Cài đặt môi trường
```
  pip install -r requirements.txt
```
2. Chạy ứng dụng
```
  streamlit run app.py
```
## Tham khảo (References)
1. [Docs Lossy RLE wiki](https://en.wikipedia.org/wiki/Run-length_encoding)
2. [Lossy Image Compression of stoimen](http://stoimen.com/2012/05/03/computer-algorithms-lossy-image-compression-with-run-length-encoding/)
3. [Docs Streamlit](https://docs.streamlit.io/)