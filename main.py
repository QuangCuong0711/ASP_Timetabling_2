import clingo, time, os, sys

# --- Số lõi CPU ---
num_cores = os.cpu_count() or 1
print(f"Chạy ở chế độ song song với {num_cores} nhân.")

# --- Các danh sách file ASP ---
K69_lp_files = [
    "tkbuet2526hki/atoms_course_K69.lp",
    "tkbuet2526hki/atoms_class_course_K69.lp",
    "tkbuet2526hki/atoms_lecturer.lp",
    "tkbuet2526hki/atoms_room_GD3.lp",
    "tkbuet2526hki/atoms_room_GD4.lp",
    "tkbuet2526hki/atoms_mandatory_room.lp",
    "tkbuet2526hki/atoms_teacher_course.lp",
    "tkbuet2526hki/basic_atom.lp",
    "tkbuet2526hki/hard_constraints.lp",
    "tkbuet2526hki/room_building.lp"
]

K68_K69_lp_files = [
    "tkbuet2526hki/atoms_course_K68.lp",
    "tkbuet2526hki/atoms_class_course_K68.lp",
    "tkbuet2526hki/atoms_course_K69.lp",
    "tkbuet2526hki/atoms_class_course_K69.lp",
    "tkbuet2526hki/atoms_lecturer.lp",
    "tkbuet2526hki/atoms_room_GD3.lp",
    "tkbuet2526hki/atoms_room_GD4.lp",
    "tkbuet2526hki/atoms_mandatory_room.lp",
    "tkbuet2526hki/atoms_teacher_course.lp",
    "tkbuet2526hki/basic_atom.lp",
    "tkbuet2526hki/hard_constraints.lp",
    "tkbuet2526hki/room_building.lp"
]

All_lp_files = [
    "tkbuet2526hki/atoms_course_K66.lp",
    "tkbuet2526hki/atoms_class_course_K66.lp",
    "tkbuet2526hki/atoms_course_K67.lp",
    "tkbuet2526hki/atoms_class_course_K67.lp",
    "tkbuet2526hki/atoms_course_K68.lp",
    "tkbuet2526hki/atoms_class_course_K68.lp",
    "tkbuet2526hki/atoms_course_K69.lp",
    "tkbuet2526hki/atoms_class_course_K69.lp",
    "tkbuet2526hki/atoms_lecturer.lp",
    "tkbuet2526hki/atoms_room_GD3.lp",
    "tkbuet2526hki/atoms_room_GD4.lp",
    "tkbuet2526hki/atoms_mandatory_room.lp",
    "tkbuet2526hki/atoms_teacher_course.lp",
    "tkbuet2526hki/basic_atom.lp",
    "tkbuet2526hki/hard_constraints.lp",
    "tkbuet2526hki/room_building.lp"
]

# --- Chọn lp_files dựa vào tham số ---
if len(sys.argv) < 2:
    print("Chưa chỉ định danh sách lp_files. Dùng: 1=K69, 2=K68_K69, 3=All")
    sys.exit(1)

arg = sys.argv[1]
if arg == "1":
    lp_name = "K69"
    lp_files = K69_lp_files
elif arg == "2":
    lp_name = "K68_K69"
    lp_files = K68_K69_lp_files
elif arg == "3":
    lp_name = "All"
    lp_files = All_lp_files
else:
    print("Tham số không hợp lệ. Chỉ được 1, 2 hoặc 3")
    sys.exit(1)

print(f"Chạy với lp_files = {arg}")

# --- Khởi tạo Control ---
ctl = clingo.Control([
    "--warn=none",
    "--configuration=jumpy",
    "--restarts=luby,128",
    "--seed=1",
    f"--parallel-mode={num_cores}"
])

# --- Load file ---
for f in lp_files:
    path = os.path.join(os.path.dirname(__file__), f)
    with open(path, "r", encoding="utf-8") as file:
        ctl.add("base", [], file.read())

# --- Grounding ---
print("Bắt đầu grounding...")
t0 = time.perf_counter()
ctl.ground([("base", [])])
t1 = time.perf_counter()
print(f"Grounding xong: {t1 - t0:.4f} giây")

# --- Hàm xử lý model ---
output_file = os.path.join(os.path.dirname(__file__), f"{lp_name}_result.txt")

def on_model(m):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Đã tìm thấy nghiệm đầu tiên cho {lp_name}\n")
        f.write(" ".join(map(str, m.symbols(shown=True))) + "\n")
    print(f"Đã tìm thấy nghiệm đầu tiên cho {lp_name}. Kết quả ghi vào {output_file}")
    return True

# --- Solve ---
print("Bắt đầu solve...")
t2 = time.perf_counter()
res = ctl.solve(on_model=on_model)
t3 = time.perf_counter()

ground_time = t1 - t0
solve_time  = t3 - t2
total_time  = t3 - t0

print(f"Solve xong: {solve_time:.4f} giây | Tổng: {total_time:.4f} giây")

# --- Ghi thêm thời gian vào file kết quả ---
with open(output_file, "a", encoding="utf-8") as f:
    f.write("\n===== Thời gian chạy =====\n")
    f.write(f"Grounding time: {ground_time:.4f} giây\n")
    f.write(f"Solve time:     {solve_time:.4f} giây\n")
    f.write(f"Total time:     {total_time:.4f} giây\n")

# --- Trạng thái ---
status = "UNKNOWN"
if res.satisfiable: status = "SATISFIABLE"
elif res.exhausted: status = "UNSATISFIABLE"
elif res.interrupted: status = "UNKNOWN (Interrupted)"

print(f"Status: {status}")
