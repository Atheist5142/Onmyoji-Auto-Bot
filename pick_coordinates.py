import ctypes
import time

import win32gui


TOTAL_COORDINATES = 12
CAPTURE_KEY = 0x77  # F8
UNDO_KEY = 0x78  # F9
ESCAPE_KEY = 0x1B
GAME_TITLES = ("陰陽師Onmyoji", "阴阳师Onmyoji")


def find_game_window():
    for title in GAME_TITLES:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd and win32gui.IsWindowVisible(hwnd):
            return hwnd
    return None


def is_key_pressed(key):
    return ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000 != 0


def wait_for_key_release(key):
    while is_key_pressed(key):
        time.sleep(0.03)


hwnd = find_game_window()
if not hwnd:
    raise RuntimeError(
        "Không tìm thấy cửa sổ game. Hãy mở game trước và kiểm tra tiêu đề "
        "là 陰陽師Onmyoji hoặc 阴阳师Onmyoji."
    )

client_left, client_top = win32gui.ClientToScreen(hwnd, (0, 0))
client_right, client_bottom = win32gui.ClientToScreen(
    hwnd,
    win32gui.GetClientRect(hwnd)[2:],
)

coordinates = []
print(f"Đã kết nối cửa sổ game: hwnd={hwnd}")
print(f"Vùng client game: ({client_left}, {client_top}) - ({client_right}, {client_bottom})")
print()
print("Đưa chuột tới vị trí cần lấy rồi nhấn F8.")
print("F9 để xóa tọa độ vừa lấy, ESC để kết thúc.")
print("Không cần click chuột vào game; F8 chỉ ghi nhận vị trí con trỏ.")

previous_capture = False
previous_undo = False
while True:
    if is_key_pressed(ESCAPE_KEY):
        wait_for_key_release(ESCAPE_KEY)
        break

    capture_pressed = is_key_pressed(CAPTURE_KEY)
    if capture_pressed and not previous_capture:
        x, y = win32gui.GetCursorPos()
        if client_left <= x < client_right and client_top <= y < client_bottom:
            coordinates.append((x - client_left, y - client_top))
            index = len(coordinates)
            print(f"{index:2}: ({coordinates[-1][0]}, {coordinates[-1][1]})")
            if index == TOTAL_COORDINATES:
                print("\nĐã đủ 12 tọa độ:")
                print(", ".join(f"({x}, {y})" for x, y in coordinates))
                print("Nhấn ESC để thoát.")
        else:
            print(f"Con trỏ đang ngoài vùng game: ({x}, {y})")
    previous_capture = capture_pressed

    undo_pressed = is_key_pressed(UNDO_KEY)
    if undo_pressed and not previous_undo:
        if coordinates:
            removed = coordinates.pop()
            print(f"Đã xóa tọa độ {removed}. Còn lại {len(coordinates)}/12.")
        else:
            print("Chưa có tọa độ để xóa.")
    previous_undo = undo_pressed

    time.sleep(0.03)

print("\nDanh sách tọa độ đã lấy:")
print(", ".join(f"({x}, {y})" for x, y in coordinates) or "(chưa có)")
