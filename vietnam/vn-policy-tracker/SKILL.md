---
name: vn-policy-tracker
description: Thu thập và tổng hợp các văn bản, chính sách, thông tư, nghị định, dự thảo luật... mới ban hành hoặc công bố của chính phủ Việt Nam trong 14 ngày gần nhất, có ảnh hưởng quan trọng đến kinh tế - xã hội. Kích hoạt khi người dùng yêu cầu "cập nhật chính sách", "tổng hợp văn bản nhà nước", "báo cáo chính sách VN", hoặc tương tự.
version: 1.0.0
author: Albert
license: MIT
metadata:
  hermes:
    tags: [Research, Vietnam, Policy, Government, News, Economy]
    related_skills: []
    requires_toolsets: [web]
    requires_tools: [web_search]
    fallback_for_toolsets: [browser]   # Hide if the browser toolset IS active
    fallback_for_tools: [browser_navigate]  # Hide if browser_navigate IS available
---

# Vietnam Policy Tracker — Thu thập & Báo cáo Chính sách Chính phủ Việt Nam

Thu thập các văn bản pháp luật, chính sách, thông tư, nghị định, quyết định, dự thảo... mới được ban hành/công bố trong **14 ngày gần nhất** (tính theo thời điểm chạy skill — dùng ngày giờ thực tế, không dùng ngày trong dữ liệu huấn luyện), có ảnh hưởng đáng kể đến kinh tế - xã hội Việt Nam, rồi tổng hợp thành một báo cáo xếp hạng, không trùng lặp.

**Bắt buộc:** phải truy vấn **toàn bộ domains** liệt kê trong `references/domains.txt` — không được bỏ sót domain nào, kể cả khi domain đó không cho ra kết quả trong khung 14 ngày. Nếu một domain không có văn bản nào phù hợp hoặc không truy cập được, vẫn phải ghi nhận rõ điều đó trong báo cáo (xem mục "Bắt buộc: theo dõi phạm vi nguồn" bên dưới) — im lặng bỏ qua một domain là lỗi nghiêm trọng của skill này.

## When to Use

- Người dùng yêu cầu tổng hợp/cập nhật văn bản, chính sách, pháp luật mới của Việt Nam.
- Người dùng hỏi "có chính sách/nghị định/thông tư gì mới ảnh hưởng đến kinh tế/doanh nghiệp/thị trường không".

Không dùng skill này cho tin tức chung chung không liên quan chính sách/pháp luật, hoặc phân tích một văn bản luật cụ thể đã có sẵn (đó là việc đọc văn bản, không phải thu thập).

## Quy trình tổng quan

1. **Xác định khung thời gian**: lấy ngày hiện tại thực tế (qua tool sẵn có, ví dụ kết quả `web_search` luôn có ngày, hoặc lệnh `date` nếu có `terminal`). Khung thu thập = [hôm nay - 14 ngày, hôm nay]. Nêu rõ khung thời gian này ở đầu báo cáo.
2. **Thu thập song song theo nhóm nguồn** (xem `references/domains.md`): với mỗi nguồn/nhóm nguồn, dùng `web_search` (query theo mẫu ở dưới) rồi `web_extract`/`web_fetch` các trang kết quả có vẻ phù hợp. Nếu agent framework hỗ trợ chạy nhiều tác vụ con song song (sub-agents/parallel tool calls), hãy tách theo nhóm nguồn ở Bước 3 và chạy đồng thời — mỗi nhóm nguồn là một tác vụ độc lập, không phụ thuộc kết quả của nhóm khác.
3. **Chuẩn hoá dữ liệu thu thập** thành các bản ghi có cấu trúc (xem schema bên dưới).
4. **Khử trùng lặp** giữa các nguồn (cùng một văn bản thường được đưa tin bởi nhiều báo). Có thể dùng `scripts/dedupe_rank.py` để hỗ trợ so khớp gần đúng theo số hiệu văn bản / tiêu đề.
5. **Xếp hạng & phân loại** theo mức độ ảnh hưởng, giải thích lý do.
6. **Viết báo cáo** theo `references/report_template.md`.
7. **Lưu báo cáo vào thư mục `vn-policy-briefings/` trong workspace** với tên file có ngày tháng để theo dõi lịch sử các lần chạy (xem mục "Lưu báo cáo vào workspace" bên dưới).


## Nhóm nguồn thu thập (chạy song song theo nhóm)

Chi tiết đầy đủ về từng domain (loại nội dung, cách tìm kiếm hiệu quả) nằm trong `references/domains.md`. Danh sách phẳng tất cả domain bắt buộc nằm trong `references/domains.txt` (dùng trực tiếp với `scripts/dedupe_rank.py --expected-domains`). Tóm tắt 4 nhóm để phân việc song song — **cả 4 nhóm và toàn bộ domain trong mỗi nhóm đều bắt buộc phải xử lý, không được lược bớt vì lý do trùng lặp nội dung hay tiết kiệm thời gian:**

| Nhóm | Domains | Vai trò |
|---|---|---|
| A — Nguồn chính thức/pháp lý | `xaydungchinhsach.chinhphu.vn`, `chinhphu.vn`, `baochinhphu.vn`, `congbao.chinhphu.vn` | Văn bản gốc, dự thảo, tin chính thức từ Chính phủ |
| B — Ngân hàng/Tài chính | `sbv.gov.vn` | Chính sách tiền tệ, tín dụng, ngân hàng |
| C — Cơ sở dữ liệu pháp luật | `luatvietnam.vn` | Tra cứu văn bản mới ban hành, có số hiệu, ngày hiệu lực rõ ràng |
| D — Báo chí kinh tế/tổng hợp | `vnexpress.net`, `nhandan.vn`, `cafef.vn`, `tuoitre.vn`, `vneconomy.vn` | Diễn giải, đánh giá tác động, phản ứng thị trường/dư luận |

Với mỗi nhóm, thực hiện các truy vấn dạng:

```
site:xaydungchinhsach.chinhphu.vn chính sách mới [tháng/năm hiện tại]
site:luatvietnam.vn văn bản mới ban hành [tháng/năm hiện tại]
site:sbv.gov.vn thông tư quyết định [tháng/năm hiện tại]
site:cafef.vn OR site:vneconomy.vn chính sách kinh tế mới nghị định thông tư
```

Ưu tiên trang chuyên mục/nguồn liệt kê (ví dụ `xaydungchinhsach.chinhphu.vn/chinh-sach-moi.htm`, `sbv.gov.vn/vi/tin-tuc-su-kien`) trước khi tìm kiếm tự do, vì các trang này đã liệt kê theo thời gian.

**Loại văn bản cần thu thập**: Luật, Nghị định, Nghị quyết, Thông tư, Quyết định, Chỉ thị, Công điện, Dự thảo (đang lấy ý kiến), sửa đổi/bổ sung văn bản hiện hành.

**Tiêu chí "ảnh hưởng quan trọng đến kinh tế - xã hội"**: tác động đến thuế/phí, lãi suất/tín dụng, thị trường bất động sản/chứng khoán/vàng, doanh nghiệp (điều kiện kinh doanh, thủ tục), lao động - tiền lương - bảo hiểm, đất đai, xuất nhập khẩu, an sinh xã hội, hoặc phạm vi áp dụng toàn quốc/nhiều tỉnh thành. Bỏ qua văn bản hành chính nội bộ, nhân sự, hoặc phạm vi rất hẹp (một địa phương/một ngành nhỏ) trừ khi có tác động lan toả rõ.

## Schema cho mỗi bản ghi thu thập được

```
- title: Tên đầy đủ văn bản (kèm số hiệu nếu có, VD "Nghị định 12/2026/NĐ-CP")
- doc_type: Luật | Nghị định | Nghị quyết | Thông tư | Quyết định | Chỉ thị | Dự thảo | Khác
- issuing_body: Cơ quan ban hành (Chính phủ, NHNN, Bộ Tài chính...)
- issue_date: Ngày ban hành (nếu là dự thảo: ngày công bố lấy ý kiến)
- effective_date: Ngày hiệu lực (nếu biết)
- status: Đã ban hành | Dự thảo | Đang lấy ý kiến | Sắp có hiệu lực
- summary: Tóm tắt nội dung chính bằng lời văn của agent (5 câu, KHÔNG chép nguyên văn dài từ nguồn)
- impact_areas: [thuế, bất động sản, ngân hàng, lao động, doanh nghiệp, ...]
- sources: danh sách URL đã thu thập được bản tin/văn bản này (để khử trùng lặp và trích dẫn)
```

## Khử trùng lặp

Một văn bản thường xuất hiện trên nhiều báo/nguồn. Gộp các bản ghi có:
- cùng số hiệu văn bản, HOẶC
- tiêu đề/nội dung giống nhau ở mức cao (cùng loại văn bản + cùng chủ đề + ngày ban hành gần nhau)

Khi gộp, giữ `sources` là danh sách hợp nhất tất cả URL liên quan, và ưu tiên lấy `summary` chi tiết nhất hoặc tổng hợp từ nguồn chính thức (Nhóm A/B/C) làm nguồn sự thật, dùng Nhóm D (báo chí) để bổ sung phần đánh giá tác động.

Có thể dùng script hỗ trợ (khuyến nghị luôn dùng kèm `--expected-domains` để tự động kiểm tra bỏ sót nguồn):

```
python3 ${HERMES_SKILL_DIR}/scripts/dedupe_rank.py input.json \
  --expected-domains ${HERMES_SKILL_DIR}/references/domains.txt
```

Script nhận vào một file JSON là danh sách bản ghi theo schema trên (agent tự tạo file này sau khi thu thập), in ra:
1. (stdout) Danh sách đã gộp trùng lặp — gộp theo số hiệu văn bản chuẩn hoá hoặc độ tương đồng tiêu đề, sắp theo `issue_date` giảm dần. Khi gộp, trường `sources` được hợp nhất (union), **không bị mất** — nhờ đó vẫn biết một văn bản từng xuất hiện trên (những) domain nào dù đã gộp trùng.
2. (stderr) Bảng thống kê số bản ghi theo từng domain nguồn, và **cảnh báo rõ domain nào trong `domains.txt` không có bản ghi nào** — agent phải đọc phần cảnh báo này và xử lý theo mục "Bắt buộc: theo dõi phạm vi nguồn" bên dưới, không được bỏ qua.

Đây chỉ là công cụ hỗ trợ gộp/sắp thứ tự thời gian/theo dõi phạm vi nguồn — việc **xếp hạng theo mức độ quan trọng** vẫn do agent thực hiện bằng lý giải (xem bên dưới), vì mức độ ảnh hưởng kinh tế-xã hội cần đánh giá định tính.

## Bắt buộc: theo dõi phạm vi nguồn (source coverage)

Mỗi bản ghi trong schema đã có trường `sources` — đây **không phải trường tuỳ chọn**: mọi văn bản đưa vào báo cáo bắt buộc phải có ít nhất 1 URL nguồn thật (đã fetch/search được), không được tự suy diễn hay bỏ trống.

Trước khi viết báo cáo cuối, agent phải tự lập một **bảng theo dõi phạm vi nguồn** gồm toàn bộ tất cả domains trong `references/domains.txt`, mỗi domain một trong 3 trạng thái:
- **Có kết quả** — tìm được ít nhất 1 văn bản trong khung 14 ngày, kèm số lượng.
- **Không có kết quả phù hợp** — đã truy vấn domain này (nêu rõ query/URL đã thử) nhưng không có văn bản nào trong khung 14 ngày hoặc không đạt tiêu chí ảnh hưởng kinh tế-xã hội.
- **Không truy cập được** — domain chặn truy cập/lỗi kỹ thuật khi search/fetch (nêu rõ lỗi gặp phải).

Bảng này **bắt buộc phải xuất hiện trong báo cáo cuối** (mục "Ghi chú phương pháp" của `references/report_template.md`). Không được nộp báo cáo nếu có domain trong danh sách bắt buộc chưa từng được truy vấn lần nào — thiếu một dòng trong bảng này đồng nghĩa với bỏ sót nguồn, là lỗi cần sửa trước khi hoàn tất.

## Xếp hạng mức độ quan trọng

Xếp mỗi văn bản vào 1 trong 3 mức, kèm giải thích ngắn gọn vì sao:

- **Cao**: Ảnh hưởng toàn quốc, tác động trực tiếp đến số đông (thuế, lãi suất điều hành, lương tối thiểu, đất đai, giá điện/xăng dầu), hoặc thay đổi lớn về khung pháp lý một ngành.
- **Trung bình**: Ảnh hưởng một nhóm ngành/đối tượng cụ thể (VD điều kiện kinh doanh một lĩnh vực, thủ tục hải quan một nhóm hàng).
- **Thấp**: Mang tính kỹ thuật, hành chính, hoặc phạm vi hẹp nhưng vẫn đáng ghi nhận.

Trong phần giải thích, nêu: đối tượng bị/được tác động, cơ chế tác động (VD "tăng room tín dụng → tăng khả năng tiếp cận vốn của doanh nghiệp"), và mức độ chắc chắn (đã ban hành/hiệu lực vs. còn là dự thảo).

## Viết báo cáo

Dùng cấu trúc trong `references/report_template.md`. Báo cáo gồm:
1. Khung thời gian & phạm vi nguồn đã thu thập
2. Tóm tắt điều hành (3-5 điểm nổi bật nhất)
3. Danh sách văn bản xếp theo mức độ quan trọng (Cao → Trung bình → Thấp), mỗi mục có đầy đủ trường trong schema + giải thích xếp hạng + nguồn
4. (Nếu có) Mục riêng cho các dự thảo đang lấy ý kiến — vì đây chưa phải chính sách chính thức, cần ghi rõ

## Lưu báo cáo vào workspace
 
Sau khi hoàn tất báo cáo, **bắt buộc lưu file vào thư mục `vn-policy-briefings/` trong workspace** (không chỉ trả lời trong chat) để có thể tra cứu lại và so sánh giữa các lần chạy.

Workspace ở đây là **workspace do Hermes agent xác định tại thời điểm chạy**, không mặc định là thư mục mã nguồn của skill hoặc thư mục repository đang chứa skill. Thư mục mã nguồn skill chỉ chứa mã nguồn và tài liệu của skill, không chứa dữ liệu do agent tạo ra. Tạo thư mục `vn-policy-briefings/` trong workspace nếu thư mục này chưa tồn tại.
 
**Quy ước đặt tên file** (bắt buộc theo đúng mẫu để dễ sắp xếp theo thời gian):
 
```
vn-policy-report_<ngay-bat-dau>_den_<ngay-ket-thuc>_<thoi-diem-chay>.md
```
 
Trong đó:
- `<ngay-bat-dau>` và `<ngay-ket-thuc>` là khung 14 ngày đã thu thập, định dạng `YYYY-MM-DD` (VD `2026-07-30`, `2026-08-13`).
- `<thoi-diem-chay>` là dấu thời gian lúc tạo báo cáo, định dạng `YYYYMMDD-HHmm` (giờ địa phương hoặc UTC, ghi rõ trong file), dùng để phân biệt khi chạy nhiều lần cho cùng một khung thời gian.
Ví dụ tên file đầy đủ:
 
```
vn-policy-report_2026-07-30_den_2026-08-13_20260813-0700.md
```
 
Nếu môi trường có `terminal`, có thể lấy dấu thời gian bằng:
 
```
date -u +%Y%m%d-%H%M
```
 
Ghi rõ ở đầu file báo cáo (đã có sẵn placeholder trong `references/report_template.md`) cả khung thời gian thu thập lẫn thời điểm chạy skill, để không phải mở tên file mới biết được.
 
Nếu skill được chạy lặp lại nhiều lần (kể cả qua blueprint theo lịch), **không ghi đè lên báo cáo cũ** — mỗi lần chạy tạo một file mới theo quy ước trên, giữ lại toàn bộ lịch sử báo cáo trong thư mục `vn-policy-briefings/` để tiện theo dõi/so sánh theo thời gian.

## Pitfalls

- **Đừng chỉ tìm trên báo chí (Nhóm D)** — báo chí diễn giải có thể sai lệch hoặc chậm hơn nguồn gốc. Luôn đối chiếu với Nhóm A/B/C khi có thể.
- **Đừng liệt kê văn bản ngoài khung 14 ngày** — kiểm tra kỹ ngày ban hành/công bố, không phải ngày bài báo được index.
- **Đừng trộn dự thảo với văn bản đã ban hành** mà không ghi chú rõ trạng thái — sai lệch này gây hiểu nhầm nghiêm trọng về tính chính thức.
- **Đừng chép nguyên văn dài** từ nguồn báo chí có bản quyền — luôn diễn giải lại bằng lời văn riêng, trích dẫn nguồn qua URL.
- Nếu một domain chặn truy cập/không lấy được nội dung, ghi nhận rõ trong báo cáo (nguồn X không truy cập được) thay vì bỏ qua âm thầm.

## Verification

Trước khi gửi báo cáo, kiểm tra:
- [ ] Mỗi văn bản có ít nhất 1 URL nguồn hợp lệ, thật (đã fetch/search được, không tự suy diễn)
- [ ] Không có 2 mục trùng nhau (cùng văn bản xuất hiện 2 lần)
- [ ] Tất cả ngày ban hành nằm trong khung 14 ngày đã nêu (hoặc là dự thảo có ngày công bố trong khung)
- [ ] Mỗi mục có mức xếp hạng + lý do
- [ ] **Tất Cả domain trong `references/domains.txt` đều đã được truy vấn ít nhất 1 lần** — không có domain nào bị bỏ sót hoàn toàn
- [ ] Báo cáo có đầy đủ bảng theo dõi phạm vi nguồn (theo dòng, mỗi domain 1 trạng thái: Có kết quả / Không có kết quả phù hợp / Không truy cập được)
- [ ] Báo cáo đã được lưu thành file trong thư mục `vn-policy-briefings/` của workspace do Hermes agent xác định, đúng quy ước đặt tên có ngày tháng (không chỉ trả lời trong chat và không lưu vào thư mục mã nguồn skill)