import os
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def rename_files_in_folder(folder_path, new_prefix, start_number):
    """
    Hàm đổi tên hàng loạt file trong một thư mục dựa trên thứ tự số cũ.
    In ra kết quả vào console để theo dõi.
    """
    # 1. Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(folder_path):
        messagebox.showerror("Lỗi", f"Thư mục được chọn không tồn tại:\n{folder_path}")
        return

    print("--- BẮT ĐẦU QUÁ TRÌNH ĐỔI TÊN ---")
    print(f"Thư mục xử lý: {folder_path}")
    print(f"Định dạng tên mới: {new_prefix}<số>{'<phần mở rộng>'}")
    print(f"Bắt đầu từ số: {start_number}")
    print("-" * 35)

    # 2. Lấy danh sách các file trong thư mục
    try:
        files = os.listdir(folder_path)
    except OSError as e:
        messagebox.showerror("Lỗi", f"Không thể truy cập thư mục:\n{e}")
        return

    # 3. Sắp xếp các file theo thứ tự số trong tên file cũ
    def get_number_from_filename(filename):
        # Tìm số cuối cùng trong tên file để sắp xếp đúng (abc_1.txt trước abc_10.txt)
        match = re.search(r'(\d+)(?!.*\d)', filename)
        if match:
            return int(match.group(1))
        return -1 # Nếu file không có số, xếp xuống cuối

    files.sort(key=get_number_from_filename)

    # 4. Vòng lặp đổi tên
    rename_count = 0
    error_count = 0
    current_number = start_number
    for old_filename in files:
        old_full_path = os.path.join(folder_path, old_filename)

        # Chỉ xử lý file, bỏ qua thư mục con
        if not os.path.isfile(old_full_path):
            continue
        
        # Tách phần tên và phần mở rộng file (ví dụ: '.txt', '.jpg')
        _, file_extension = os.path.splitext(old_filename)

        # Tạo tên file mới
        new_filename = f"{new_prefix}{current_number}{file_extension}"
        new_full_path = os.path.join(folder_path, new_filename)

        # Thực hiện đổi tên
        try:
            # Kiểm tra nếu tên mới đã tồn tại để tránh ghi đè
            if os.path.exists(new_full_path):
                print(f"CẢNH BÁO: Tên file mới '{new_filename}' đã tồn tại. Bỏ qua file '{old_filename}'.")
                error_count += 1
                continue

            os.rename(old_full_path, new_full_path)
            print(f"Thành công: '{old_filename}'  ->  '{new_filename}'")
            rename_count += 1
            current_number += 1
        except OSError as e:
            print(f"LỖI khi đổi tên '{old_filename}': {e}")
            error_count += 1

    # 5. Thông báo kết quả cuối cùng
    print("-" * 35)
    print("--- HOÀN TẤT ---")
    summary_message = (
        f"Đã đổi tên thành công: {rename_count} file.\n"
        f"Số file bị lỗi hoặc bỏ qua: {error_count} file."
    )
    print(summary_message)
    messagebox.showinfo("Hoàn Tất", summary_message)

def main():
    """
    Hàm chính điều khiển luồng giao diện người dùng (GUI).
    """
    # Tạo một cửa sổ tkinter chính và ẩn nó đi
    root = tk.Tk()
    root.withdraw()

    # 1. Mở hộp thoại để người dùng chọn thư mục
    messagebox.showinfo("Bắt đầu", "Vui lòng chọn thư mục chứa các file bạn muốn đổi tên.")
    folder_selected = filedialog.askdirectory(title="Chọn thư mục cần đổi tên file")
    
    # Nếu người dùng không chọn thư mục nào (nhấn Cancel) -> thoát
    if not folder_selected:
        print("Hủy thao tác: Người dùng không chọn thư mục.")
        return

    # 2. Mở hộp thoại để người dùng nhập định dạng tên mới (tiền tố)
    new_prefix = simpledialog.askstring(
        "Định dạng tên file",
        "Nhập phần đầu của tên file mới (ví dụ: 'hinhanh_', 'tailieu-2023_'):",
        parent=root
    )

    # Nếu người dùng nhấn Cancel
    if new_prefix is None:
        print("Hủy thao tác: Người dùng không nhập định dạng tên.")
        return

    # 3. Mở hộp thoại để người dùng nhập số bắt đầu
    start_number = simpledialog.askinteger(
        "Số thứ tự bắt đầu",
        "Nhập số thứ tự bạn muốn bắt đầu (ví dụ: 1, 11, 101):",
        parent=root,
        minvalue=0 # Có thể đặt giá trị nhỏ nhất
    )

    # Nếu người dùng nhấn Cancel
    if start_number is None:
        print("Hủy thao tác: Người dùng không nhập số bắt đầu.")
        return

    # 4. Hiển thị hộp thoại xác nhận cuối cùng
    confirmation_text = (
        f"Bạn có chắc chắn muốn thực hiện không?\n\n"
        f"Thư mục: {folder_selected}\n"
        f"Tên mới sẽ có dạng: {new_prefix}{start_number}, {new_prefix}{start_number+1}, ...\n\n"
        f"CẢNH BÁO: Thao tác này không thể hoàn tác!"
    )
    is_confirmed = messagebox.askyesno("Xác nhận lần cuối", confirmation_text)

    # 5. Nếu người dùng xác nhận, gọi hàm đổi tên
    if is_confirmed:
        rename_files_in_folder(folder_selected, new_prefix, start_number)
    else:
        print("Người dùng đã hủy thao tác ở bước xác nhận cuối cùng.")

# --- Chạy chương trình ---
if __name__ == "__main__":
    main()