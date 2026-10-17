## 5. Thuật ngữ chọn theo người đọc

- **Giữ nguyên từng chữ, mọi trường hợp:** tên lệnh, tham số, đường dẫn, biến môi trường, tên metric, tên object Kubernetes, tên model và API, mã ticket, tên branch, mã commit. Những thứ này mà dịch hoặc sửa là sai.
- **Với engineer**, từ kỹ thuật người ta vẫn nói bằng tiếng Anh thì giữ tiếng Anh (deploy, rollback, latency, throughput, checkpoint, pod, cluster…); dịch ra thường gượng.
- **Với người không chuyên**, lần đầu gặp thì giải thích bằng một mệnh đề ngay trong câu ("latency, tức thời gian từ lúc gửi yêu cầu đến lúc nhận kết quả, ở đây là 300 ms"), sau đó dùng từ đó nhất quán. Từ viết tắt phải nói đủ ở lần đầu.
- Mỗi khái niệm một tên, dùng suốt bài. Đừng đổi từ cho đỡ lặp khi hai từ không đồng nghĩa hoàn toàn (ví dụ "bottleneck" và "critical path" là hai khái niệm khác nhau).
- Không tự chế từ tiếng Việt cho khái niệm chưa có từ quen thuộc. Giữ tiếng Anh, hoặc viết thẳng điều kiện bằng số ("yaw từ −18° đến +25°"). Cũng không đổi "suy luận" thành "inference" khi đó là suy luận từ bằng chứng; chỉ dùng inference khi nói về model.

## 6. Tránh văn dịch từ tiếng Anh

Đọc to từng câu. Nếu không ai trong phòng nói như vậy thì viết lại. Bốn nguồn gốc hay gặp:

- **Bị động dịch nguyên:** "được thực hiện bởi", "được xem như là". Chuyển sang chủ động hoặc bỏ "được" khi chủ thể đã rõ: "Sentry bắt được lỗi lúc 14:02", "dự kiến pod sẵn sàng sau 30 giây".
- **Danh từ hóa bằng "việc / sự / quá trình / tính":** "Việc thực hiện tối ưu cơ sở dữ liệu là cần thiết" thành "Cần tối ưu database"; "trong quá trình đo tải" thành "khi đo tải". Chỉ bỏ khi bỏ rồi câu vẫn giữ nguyên nghĩa.
- **Cụm đệm dịch từng chữ:** "đóng một vai trò quan trọng trong việc" thành "quyết định" hoặc "then chốt đối với"; "cung cấp một giải pháp cho" thành "giải quyết"; "nhằm mục đích" thành "để"; "trong trường hợp" thành "nếu"; "tiến hành thực hiện" thành "làm". "Một cách + tính từ" ("chạy một cách ổn định") thành "chạy ổn định". Mở đầu kiểu "Điều quan trọng cần lưu ý là chúng ta có thể thấy rằng…" thì bỏ, Việt ngữ hiếm khi cần "rằng".
- **Gọi người đọc là "bạn"** theo you của tiếng Anh. Dùng anh/chị/em theo quan hệ thực, hoặc bỏ đại từ.

Khi rút gọn, bỏ phần thừa theo nghĩa của câu, không theo mẫu từ. "Đầy đủ và chính xác" trong báo cáo kiểm thử là hai yêu cầu khác nhau (đủ phạm vi, đúng số liệu), nên giữ cả hai. "Đảm bảo" (làm cho chắc chắn xảy ra) và "lưu ý" (nhắc chú ý) không thay nhau được. Nếu bỏ một chữ làm câu mất sắc thái, mất điều kiện hay mất mức chắc chắn thì giữ lại.
