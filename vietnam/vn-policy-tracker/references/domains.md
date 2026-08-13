# Chi tiết nguồn thu thập

Ghi chú cách khai thác hiệu quả từng domain. Dùng `web_search` với `site:domain ...`, sau đó `web_extract`/`web_fetch` các URL kết quả có khả năng liên quan cao.

## Nhóm A — Nguồn chính thức Chính phủ

### `xaydungchinhsach.chinhphu.vn`
- Trang chuyên mục chính sách mới: `xaydungchinhsach.chinhphu.vn/chinh-sach-moi.htm` — liệt kê theo thời gian, ưu tiên fetch trực tiếp trang này trước.
- Nội dung: chính sách mới ban hành, dự thảo đang lấy ý kiến, phân tích tác động chính sách.
- Đáng tin cậy cao nhất cho việc xác nhận một văn bản có tồn tại và trạng thái (dự thảo/đã ban hành).

### `chinhphu.vn`
- Cổng thông tin điện tử Chính phủ. Tìm mục Văn bản chỉ đạo điều hành, Tin tức.
- Query mẫu: `site:chinhphu.vn nghị định OR thông tư OR quyết định [tháng năm]`

### `baochinhphu.vn`
- Báo điện tử Chính phủ — tin chính thức, thường có bài giải thích chính sách dễ hiểu hơn văn bản gốc.

### `congbao.chinhphu.vn`
- Công báo — nơi đăng văn bản quy phạm pháp luật chính thức, có số hiệu, ngày ký, ngày hiệu lực chuẩn xác. Dùng để **xác minh** số hiệu/ngày khi các nguồn khác không thống nhất.

## Nhóm B — Ngân hàng Nhà nước

### `sbv.gov.vn`
- Trang tin tức sự kiện: `sbv.gov.vn/vi/tin-tuc-su-kien` — liệt kê theo thời gian.
- Nội dung: thông tư/quyết định về lãi suất điều hành, room tín dụng, tỷ giá, quản lý ngoại hối, chính sách tiền tệ.
- Đây là nguồn bắt buộc phải kiểm tra riêng vì chính sách tiền tệ ảnh hưởng kinh tế vĩ mô rất lớn nhưng có thể không lên báo ngay.

## Nhóm C — Cơ sở dữ liệu pháp luật

### `luatvietnam.vn`
- Cơ sở dữ liệu văn bản pháp luật cập nhật nhanh, có bộ lọc theo ngày ban hành/hiệu lực, số hiệu rõ ràng, tóm tắt "điểm mới" sẵn có.
- Query mẫu: `site:luatvietnam.vn văn bản mới [tháng năm]` hoặc tìm mục "Tin văn bản mới" nếu truy cập được.
- Rất hữu ích để đối chiếu số hiệu, ngày hiệu lực khi khử trùng lặp.

## Nhóm D — Báo chí kinh tế/tổng hợp

### `vnexpress.net`
- Mục Kinh doanh/Pháp luật. Tin nhanh, diễn giải dễ hiểu, có phản ứng dư luận/doanh nghiệp.

### `nhandan.vn`
- Báo Đảng — góc nhìn chính thống, thường đưa tin đầy đủ về các nghị quyết/chủ trương lớn.

### `cafef.vn`
- Chuyên sâu tài chính - chứng khoán - bất động sản. Tốt cho chính sách ảnh hưởng thị trường vốn, doanh nghiệp niêm yết.

### `tuoitre.vn`
- Tin tức tổng hợp, mục Kinh tế/Pháp luật, tiếp cận đại chúng, tốt để đánh giá mức độ quan tâm xã hội.

### `vneconomy.vn`
- Chuyên về kinh tế vĩ mô, chính sách tài khoá/tiền tệ, đầu tư. Phân tích tác động chính sách khá sâu.

## Ghi chú chung

- Khi `site:` search không ra kết quả trong khung 14 ngày, thử bỏ `site:` và thêm tên domain vào query, hoặc fetch trực tiếp trang chuyên mục/danh sách của domain đó rồi lọc theo ngày.
- Một số trang có thể chặn scraping tự động qua `web_extract` — nếu vậy, dùng nội dung snippet từ `web_search` và ghi chú "không truy cập được toàn văn, dựa trên tóm tắt tìm kiếm".
- Luôn ưu tiên đối chiếu số hiệu văn bản (VD "Nghị định 12/2026/NĐ-CP") giữa các nguồn — đây là khoá chính xác nhất để khử trùng lặp, chính xác hơn so khớp tiêu đề.
