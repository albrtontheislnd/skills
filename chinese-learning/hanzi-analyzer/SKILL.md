---
name: hanzi-analyzer
description: Phân tích chi tiết chữ Hán (Hán tự) — bộ thủ, âm Hán Việt, mẹo ghi nhớ (chiết tự), thứ tự nét viết — và trực quan hóa hoạt hình thứ tự nét viết bằng thư viện hanzi-writer.
version: 1.1.0
author: Albert
license: MIT
metadata:
  hermes:
    category: chinese-learning
    tags: [Language, Chinese, Education, Hanzi, Visualization]
    related_skills: []
---

# Hanzi Analyzer & Tutor Skill

Khi người dùng cung cấp một hoặc nhiều chữ Hán (ví dụ: `/hanzi-analyzer 爱` hoặc nhập từ/câu tiếng Trung), hãy phân tích theo định dạng chuẩn hóa bên dưới. Nếu người dùng muốn **xem/luyện thứ tự nét viết dưới dạng hình ảnh trực quan** (hoạt hình, quiz viết chữ, xuất GIF), dùng phần **Trực quan hóa nét viết (Stroke Order Visualization)** ở cuối skill này.

## When to Use

- Người dùng đưa vào một hoặc nhiều chữ Hán / một câu tiếng Trung và muốn hiểu nghĩa, bộ thủ, mẹo nhớ, thứ tự nét.
- Người dùng yêu cầu "xem hoạt hình viết chữ", "thứ tự nét viết trực quan", "quiz viết chữ Hán", "xuất GIF/ảnh động nét chữ", hoặc nhắc tới `hanzi-writer`.

## Quick Reference

| Việc cần làm | Cách thực hiện |
|---|---|
| Phân tích bộ thủ, âm Hán Việt, mẹo ghi nhớ | Làm theo mục "Quy trình phân tích" bên dưới, trả lời trực tiếp bằng văn bản |
| Xem hoạt hình / quiz nét viết trong trình duyệt (không cần cài gì) | `python3 ${HERMES_SKILL_DIR}/scripts/generate_stroke_order.py <chữ...> --output stroke_order.html` |
| Xuất file GIF nét viết (cần cài puppeteer) | `node ${HERMES_SKILL_DIR}/scripts/export_stroke_gif.js <chữ> --output out.gif` |

## Quy trình phân tích mỗi chữ Hán

Đối với mỗi chữ Hán được yêu cầu, hãy cung cấp thông tin chi tiết theo cấu trúc sau:

1. **Thông tin cơ bản**:
   - **Chữ Hán (Giản thể / Phồn thể)**
   - **Pinyin (Phiên âm)** + Âm Hán Việt
   - **Nghĩa của từ** (Nghĩa tiếng Việt thông dụng)

2. **Phân tích Bộ thủ & Cấu trúc (Chiết tự)**:
   - Liệt kê các **bộ thủ (Radicals)** hoặc các thành phần cấu tạo nên chữ.
   - Giải thích ý nghĩa của từng bộ thủ đóng góp vào chữ đó như thế nào.

3. **Thứ tự nét viết (Stroke Order)**:
   - Tổng số nét.
   - Nêu thứ tự các nét viết chính dựa trên quy tắc viết chữ Hán chuẩn (Trái sang phải, trên xuống dưới, ngang trước sổ sau, ngoài trước trong sau, vào trước đóng sau...).

4. **Phương pháp & Mẹo ghi nhớ (Mnemonic)**:
   - Tạo câu chuyện chiết tự ngắn gọn, tượng hình hoặc dễ nhớ dựa trên các bộ thủ.
   - Cung cấp từ ghép/ví dụ minh họa thông dụng.

---

## Ví dụ mẫu phản hồi:

### Chữ: **想** (xiǎng)

- **Âm Hán Việt**: Tưởng
- **Nghĩa**: Muốn, nghĩ, nhớ

#### 1. Phân tích cấu trúc & Bộ thủ:
- **Phía trên**: Chữ **相** (Tương/Tương đối) gồm:
  - **木** (Mộc - cây)
  - **目** (Mục - mắt)
- **Phía dưới**: **心** (Tâm - trái tim)

#### 2. Mẹo ghi nhớ (Chiết tự):
> *"Dựa vào gốc cây (**木**), mắt (**目**) nhìn về phương xa, trong lòng (**心**) tràn ngập thương nhớ."* -> Đó chính là chữ **Nghĩ/Nhớ (想)**.

#### 3. Thứ tự & Quy tắc nét viết (13 nét):
1. Viết bộ **木** (Mộc) bên trên trái trước: Ngang, sổ, phẩy, chấm.
2. Viết bộ **目** (Mục) bên trên phải: Sổ, ngang gập, ngang, ngang, ngang.
3. Viết bộ **心** (Tâm) phía dưới cùng: Chấm, nằm móc, chấm, chấm.
*Quy tắc áp dụng*: Trên trước dưới sau, trái trước phải sau.

#### 4. Từ ghép thông dụng:
- **想法** (xiǎngfǎ): Ý tưởng, cách nghĩ.
- **想念** (xiǎngniàn): Nhớ nhung.

---

## Trực quan hóa nét viết (Stroke Order Visualization)

Sau khi phân tích văn bản như trên, sử dụng thư viện JS [`hanzi-writer`](https://hanziwriter.org/) thông qua các script hỗ trợ có sẵn trong `scripts/`. Không tự viết lại logic gọi hanzi-writer bằng tay — luôn dùng script.

### Procedure

1. **Trường hợp mặc định (xem trong trình duyệt, không cần cài dependency):**

   ```
   python3 ${HERMES_SKILL_DIR}/scripts/generate_stroke_order.py 想 爱 --output stroke_order.html
   ```

   Script này (chỉ dùng Python stdlib) sinh ra **một file HTML độc lập**, nhúng thư viện `hanzi-writer` qua CDN (jsdelivr). Khi mở file bằng trình duyệt có Internet, mỗi chữ hiển thị trong một ô lưới với:
   - Nút **"Xem lại (Animate)"**: phát lại hoạt hình thứ tự nét.
   - Nút **"Đố vui (Quiz)"**: chế độ luyện viết — người dùng vẽ từng nét, hệ thống chấm đúng/sai.
   - Nút **"Hiện/Ẩn khung nét"**: bật/tắt outline mờ của chữ.

   Các tùy chọn thường dùng:

   | Cờ | Ý nghĩa | Mặc định |
   |---|---|---|
   | `--output <path>` | Đường dẫn file HTML xuất ra | `stroke_order.html` |
   | `--mode animate\|quiz\|both` | Hành vi tự động khi mở trang | `both` |
   | `--loop` | Lặp lại hoạt hình liên tục (chỉ với `--mode animate`) | tắt |
   | `--delay <ms>` | Độ trễ giữa các nét | `800` |
   | `--size <px>` | Kích thước mỗi ô chữ | `200` |

   Có thể truyền nhiều chữ cùng lúc, hoặc cả một chuỗi (script tự tách từng ký tự Hán riêng lẻ):

   ```
   python3 ${HERMES_SKILL_DIR}/scripts/generate_stroke_order.py 你好吗 --mode quiz --output quiz.html
   ```

2. Sau khi tạo file, thông báo đường dẫn file cho người dùng và tóm tắt ngắn gọn nội dung (số chữ, chế độ đã dùng).

### Pitfalls

- `hanzi-writer` cần tải dữ liệu nét vẽ (`hanzi-writer-data`) từ CDN **ngay trong trình duyệt** khi mở file HTML — nếu máy mở file không có Internet, hoạt hình sẽ không hiển thị (trạng thái báo lỗi ngay trên giao diện).
- Một số chữ hiếm/dị thể có thể không có trong bộ dữ liệu `hanzi-writer-data`; khi đó script báo "Không tìm thấy dữ liệu nét" ngay trên từng ô thay vì lỗi toàn trang.
- Không nhầm giữa phần **phân tích văn bản** (luôn trả lời trực tiếp, không cần script) và phần **trực quan hóa** (chạy script).

### Verification

- Với `generate_stroke_order.py`, output ra console dòng `Da tao file: ...` kèm danh sách chữ đã xử lý — đối chiếu số chữ này khớp với yêu cầu ban đầu.
