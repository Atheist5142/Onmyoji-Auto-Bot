# Onmyoji Auto Bot

Tool tự động hóa một số thao tác trong Onmyoji bằng nhận diện hình ảnh và thao tác cửa sổ nền trên Windows.

## Tính năng

- Tự động chạy các task:
  - **Realm Raid** — được chọn mặc định khi mở tool.
  - **Farm Souls**.
- Nhận diện nút bằng template matching với OpenCV.
- Gửi click trực tiếp tới cửa sổ game bằng Windows message, không di chuyển chuột thật.
- Nút **Ẩn game** đưa cửa sổ game ra ngoài màn hình nhưng không minimize.
- Nút **Hiện game** khôi phục vị trí/kích thước cũ và đưa game lên foreground.
- Khi dừng hoặc đóng tool, game đang bị ẩn sẽ được hiện lại.
- Kiểm tra phiên bản mới từ GitHub Releases.

## Yêu cầu

- Windows.
- Python 3.10 trở lên.
- Onmyoji bản desktop/emulator có cửa sổ mà tool tìm thấy được.
- Cửa sổ game nên chạy ở chế độ cửa sổ, với client khoảng `1136x640`.

## Cài đặt

Mở PowerShell tại thư mục dự án và chạy:

```powershell
python -m pip install -r requirements.txt
```

## Chạy tool

```powershell
python main.py
```

Sau khi GUI mở:

1. Mở Onmyoji và đăng nhập.
2. Chọn task nếu cần. Mặc định là **Realm Raid**.
3. Bấm **BẮT ĐẦU**.
4. Khi muốn không nhìn thấy game, bấm **Ẩn game**.
5. Bấm **Hiện game** để đưa game về vị trí cũ.
6. Bấm **DỪNG** để dừng bot và hiện lại game.

## Build file `.exe` trên GitHub

Repository có workflow tại `.github/workflows/build-windows.yml`.

- Vào tab **Actions** trên GitHub.
- Chọn workflow **Build Windows executable**.
- Bấm **Run workflow** để build thủ công.
- Sau khi build xong, tải artifact **OnmyojiAutoBot-windows** ở phần Artifacts.

Workflow cũng tự build khi push tag có dạng `v*`, ví dụ:

```text
v1.0.0
```

Bản build là dạng thư mục portable, không phải một file `.exe` độc lập. Khi chạy, giữ nguyên toàn bộ thư mục và mở `OnmyojiAutoBot.exe`. Thư mục `templates` đã được đóng gói vào bản build, nên không được xóa các file đi kèm trong thư mục artifact.

Khi có release mới, tool sẽ tự kiểm tra cập nhật khi mở và có thể kiểm tra lại bằng nút **Cập nhật**. Nếu có phiên bản mới, tool mở trang GitHub Release để tải file `.zip`. Phiên bản đầu tiên không tự ghi đè file `.exe` đang chạy.

## Template hình ảnh

Template được lưu trong thư mục:

```text
templates/
├── Realm_Raid/
└── souls/
```

Tên template phải khớp với các file có sẵn trong thư mục tương ứng. Nếu tool báo thiếu template, kiểm tra:

- File có tồn tại không.
- Tên file có đúng không.
- File có định dạng `.png`, `.PNG`, `.jpg` hoặc `.jpeg` không.
- Ảnh template có được chụp ở cùng độ phân giải/kích thước game không.

Template được nạp khi bot khởi động và khi bắt đầu task.

## Log và debug

Log được ghi tại:

```text
logs/bot-debug.log
```

Ảnh capture gần nhất được lưu tại:

```text
logs/debug_view.png
```

Nếu bot không click, kiểm tra log để biết tool đang:

- Không tìm thấy cửa sổ game.
- Không capture được ảnh.
- Không tìm thấy template.
- Tìm thấy ảnh nhưng confidence thấp hơn ngưỡng.

## Chạy nền và ẩn game

Nút **Ẩn game** không minimize cửa sổ. Tool di chuyển cửa sổ ra ngoài màn hình để game tiếp tục render, sau đó dùng `PrintWindow` để capture ảnh nền.

Một số bản Unity/DirectX có thể không render khi bị minimize hoàn toàn. Vì vậy không nên minimize game trong lúc bot đang chạy. Nếu capture vẫn không hoạt động khi ẩn, thử:

- Chạy game ở chế độ cửa sổ.
- Không dùng fullscreen độc quyền.
- Đảm bảo game đã render đầy đủ trước khi bấm **Ẩn game**.
- Kiểm tra `logs/debug_view.png`.

## Cấu trúc chính

```text
main.py                 Điểm khởi chạy ứng dụng
gui.py                  Giao diện điều khiển
bot.py                  Capture, nhận diện và điều khiển game
tasks.py                Danh sách task
onmyoji_realm_raid.py   Script Realm Raid độc lập cũ
templates/              Ảnh template
logs/                   Log và ảnh debug
requirements.txt        Dependency Python
```

## Lưu ý

- Không chia sẻ thông tin đăng nhập hoặc file chứa dữ liệu tài khoản.
- Tool cần tìm được đúng tiêu đề cửa sổ Onmyoji. Tiêu đề mặc định được cấu hình trong `bot.py`.
- Nếu chạy bản đóng gói `.exe`, cần build lại executable sau khi thay đổi source.
