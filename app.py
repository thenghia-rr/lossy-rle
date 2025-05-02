import streamlit as st
from PIL import Image
import pickle
import os
import io
import matplotlib.pyplot as plt

# --- HÀM NÉN ---
def lossy_rle_compress_with_progress(pixels, threshold, update_progress, base_progress=0):
    compressed = []
    i = 0
    length = len(pixels)
    update_interval = max(length // 100, 1)
    last_update = 0
    while i < length:
        count = 1
        while i + count < length and pixels[i] == pixels[i + count]:
            count += 1
        if count > threshold:
            compressed.append((1, count, pixels[i]))
            i += count
        else:
            raw_values = pixels[i:i+count]
            compressed.append((0, raw_values))
            i += count

        if i - last_update >= update_interval:
            progress_percent = base_progress + (i / length) * (100/3)
            update_progress(min(int(progress_percent), 99))
            last_update = i

    return compressed

# --- HÀM GIẢI NÉN ---
def lossy_rle_decompress(compressed):
    decompressed = []
    for item in compressed:
        if item[0] == 1:
            decompressed.extend([item[2]] * item[1])
        else:
            decompressed.extend(item[1])
    return decompressed

# --- HÀM PHÂN TÍCH (run, raw) ---
def analyze_compression(compressed_data):
    run_count = 0
    raw_count = 0
    for channel in compressed_data:
        for item in channel:
            if item[0] == 1:
                run_count += 1
            else:
                raw_count += 1
    total_segments = run_count + raw_count
    run_ratio = (run_count / total_segments) * 100 if total_segments else 0
    return run_count, raw_count, run_ratio

# --- HÀM TÌM THRESHOLD TỰ ĐỘNG (default = 1) ---
def find_best_threshold(r_data, g_data, b_data, size, thresholds=[1,2,3,4,5]):
    best_threshold = thresholds[0]
    best_size = float('inf')
    for th in thresholds:
        r_comp = lossy_rle_compress_with_progress(r_data, th, lambda x: None)
        g_comp = lossy_rle_compress_with_progress(g_data, th, lambda x: None)
        b_comp = lossy_rle_compress_with_progress(b_data, th, lambda x: None)
        compressed_bytes = io.BytesIO()
        pickle.dump(((r_comp, g_comp, b_comp), size), compressed_bytes)
        current_size = len(compressed_bytes.getvalue())
        if current_size < best_size:
            best_size = current_size
            best_threshold = th
    return best_threshold

# --- Giao diện App ---
st.set_page_config(page_title="Lossy RLE Image Compressor", layout="wide")
st.title("🖼️ Lossy RLE Image Compressor & Decompressor 🤖")

col1, col2 = st.columns(2)

# --- Cột 1: Nén ảnh ---
with col1:
    st.header("📦 Nén ảnh")

    uploaded_file = st.file_uploader("Chọn ảnh cần nén", type=["png", "jpg", "bmp"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert('RGB')
        st.image(img, caption="Ảnh gốc", use_container_width=True)

        uploaded_file.seek(0, os.SEEK_END)
        size_original = uploaded_file.tell()
        uploaded_file.seek(0)

        st.write(f"**Kích thước gốc:** {size_original} bytes")

        threshold_mode = st.radio("Chọn chế độ Threshold:", ["Tự động tìm Threshold", "Nhập Threshold thủ công"])

        manual_threshold = None
        if threshold_mode == "Nhập Threshold thủ công":
            manual_threshold = st.slider("Threshold thủ công (chọn số nguyên):", min_value=1, max_value=20, value=3)

        if st.button("🚀 Bắt đầu nén ảnh"):
            r, g, b = img.split()
            r_data = list(r.getdata())
            g_data = list(g.getdata())
            b_data = list(b.getdata())

            with st.spinner('🔄 Đang nén ảnh, vui lòng chờ...'):
                progress = st.progress(0)

                if manual_threshold is not None:
                    best_threshold = manual_threshold
                    st.write(f"⚙️ **Threshold bạn chọn:** {best_threshold}")
                else:
                    best_threshold = find_best_threshold(r_data, g_data, b_data, img.size)
                    st.write(f"🔍 **Threshold tối ưu tự động:** {best_threshold}")

                r_compressed = lossy_rle_compress_with_progress(r_data, threshold=best_threshold, update_progress=progress.progress, base_progress=0)
                g_compressed = lossy_rle_compress_with_progress(g_data, threshold=best_threshold, update_progress=progress.progress, base_progress=33)
                b_compressed = lossy_rle_compress_with_progress(b_data, threshold=best_threshold, update_progress=progress.progress, base_progress=66)

                progress.progress(100)

            compressed_data = (r_compressed, g_compressed, b_compressed)

            run_count, raw_count, run_ratio = analyze_compression(compressed_data)

            compressed_bytes = io.BytesIO()
            pickle.dump((compressed_data, img.size), compressed_bytes)
            compressed_bytes.seek(0)

            compressed_size = len(compressed_bytes.getvalue())
            compression_ratio = (compressed_size / size_original) * 100

            st.success("🎉 Đã nén xong!")
            st.write(f"**Kích thước sau nén:** {compressed_size} bytes")
            st.write(f"**Tỷ lệ nén:** {compression_ratio:.2f}%")

            st.write(f"📊 Ảnh này có {run_count} đoạn Run-length thành công, {raw_count} đoạn Raw-data.")
            st.write(f"🏆 Tỉ lệ run thành công: {run_ratio:.2f}%")

            # --- Vẽ Pie Chart ---
            fig, ax = plt.subplots()
            labels = ['Run-length', 'Raw-data']
            sizes = [run_count, raw_count]
            colors = ['#4CAF50', '#FF5722']
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')  # Hình tròn
            st.pyplot(fig)

            # Biểu đồ Bar so sánh ảnh gốc và ảnh sau nén
            fig2, ax2 = plt.subplots()
            ax2.bar(['Gốc', 'Đã nén'], [size_original, compressed_size], color=['#2196F3', '#FFC107'])
            ax2.set_ylabel('Bytes')
            ax2.set_title('So sánh kích thước ảnh')

            for i, v in enumerate([size_original, compressed_size]):
                ax2.text(i, v + max(size_original, compressed_size)*0.01, f"{v} bytes", ha='center')

            st.pyplot(fig2)


            st.download_button("⬇️ Tải file nén (.rle)", compressed_bytes, file_name="compressed.rle")

# --- Cột 2: Giải nén ảnh ---
with col2:
    st.header("🛠️ Giải nén ảnh")

    uploaded_rle_file = st.file_uploader("Chọn file .rle để giải nén", type=["rle"], key="decompress")
    if uploaded_rle_file is not None:
        if st.button("📂 Bắt đầu giải nén"):
            try:
                with st.spinner('🔄 Đang giải nén ảnh...'):
                    decompressed_data = pickle.load(uploaded_rle_file)
                    (r_compressed, g_compressed, b_compressed), size = decompressed_data

                    r_data = lossy_rle_decompress(r_compressed)
                    g_data = lossy_rle_decompress(g_compressed)
                    b_data = lossy_rle_decompress(b_compressed)

                    r_img = Image.new('L', size)
                    g_img = Image.new('L', size)
                    b_img = Image.new('L', size)
                    r_img.putdata(r_data)
                    g_img.putdata(g_data)
                    b_img.putdata(b_data)

                    img_restored = Image.merge("RGB", (r_img, g_img, b_img))

                    st.image(img_restored, caption="Ảnh sau giải nén", use_container_width=True)

                    img_bytes = io.BytesIO()
                    img_restored.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    st.download_button("⬇️ Tải ảnh đã giải nén", img_bytes, file_name="restored.png")
            except Exception as e:
                st.error(f"❌ Lỗi khi giải nén: {e}")
