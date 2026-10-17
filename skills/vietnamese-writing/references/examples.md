## 7. Hai đoạn mẫu (sự việc bịa chỉ để minh họa, không dùng lại)

**Gửi quản lý, bản cụt và rời ý:**
> Cache mới: p95 giảm. Chưa test prod. Còn lỗi eviction. Cần review. Dự kiến tuần sau.

**Cùng nguồn, viết cho người đọc cần quyết định:**
> Cache mới có vẻ giảm được thời gian phản hồi, nhưng chưa đủ cơ sở để bật trên prod. Trên môi trường staging với 2.000 request mô phỏng, p95 giảm từ 480 ms xuống 310 ms; chưa có số đo trên lưu lượng thật. Ngoài ra còn một lỗi eviction (cache xóa nhầm mục còn dùng) chưa sửa, nên trước mắt chỉ cần anh duyệt phần code để nhóm sửa tiếp. Việc bật trên prod sẽ xin duyệt riêng sau khi có số đo thật. Tuần sau là thời điểm nhóm dự kiến, chưa phải cam kết.

Điểm khác nhau: bản sau nói kết luận trước, giữ mẫu số và môi trường, tách việc cần duyệt khỏi việc chưa quyết, giữ mức "dự kiến", và nối các ý bằng "nhưng", "nên", "sau khi".

**Giải thích cho PO, bản nhiều thuật ngữ:**
> Throughput bị cap do pool exhaustion nên p99 spike.

**Cùng nguồn, cho người không chuyên:**
> Khi lượng yêu cầu tăng, hệ thống hết "chỗ" để xử lý song song (connection pool, tức số kết nối tối đa được mở cùng lúc). Các yêu cầu đến sau phải xếp hàng, nên nhóm 1% chậm nhất (p99) bị chờ lâu hơn hẳn.
