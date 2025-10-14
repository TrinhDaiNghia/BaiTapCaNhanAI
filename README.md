# Bài tập cá nhân "Áp dụng các thuật toán tìm kiếm vào 8 quân xe"
**Tên sinh viên:** Trịnh Đại Nghĩa

**Mã số sinh viên:** 23110131

**Môn học/lớp:** Trí tuệ Nhân tạo/ARIN330585_05CLC

**Ngày nộp:** 15/10/2025

---
## Search Algorithms Solve 8 Rooks

### Tổng Quan

Ứng dụng này là một UI mô phỏng trực quan cách các thuật toán tìm kiếm đăt 8 quân xe cho bài toán 8-Rooks (quân xe), được xây dựng bằng ngôn ngữ lập trình Python với `Customtkinter` và `tkinter`.
Người dùng có chọn 1 thuật toán tìm kiếm bất kỳ trong 5 nhóm thuật toán: Uninformed, Informed, Local, Non-deterministic, Constraint Satisfaction Problem.

---

### 1. Mục đích xây dựng

Bài tập cá nhân này nhằm mục đích ứng dụng những kiến thức đã học về các thuật toán tìm kiếm trong môn học Trí tuệ Nhân tạo vào trò chơi đặt 8 quân xe.
Có 5 nhóm thuật toán tìm kiếm được sử dụng, các thuật toán tìm kiếm được sử dụng xếp theo 5 nhóm sau: 

- `Uninformed Search`: Nhóm thuật toán tìm kiếm không có thông tin gồm Breadth-First Search (BFS), Depth-First Search (DFS), Depth-Limited Search (DLS), Iterative Deeping Search (IDS)
- `Informed Search`: Nhóm thuật toán tìm kiếm có thông tin gồm Greedy Best-First Search, A* Search, Uniform Cost Search (UCS)
- `Local Search`: Nhóm thuật toán tìm kiếm cục bộ gồm Hill Climbing, Simulated Annealing, Beam Search, Genetic
- `Non-deterministic`: Nhóm thuật toán tìm kiếm trong môi trường phức tạp: AND-OR Search, Belief State Search, Comformant Search
- `Constraint Satisfaction Problem Search`: Nhóm thuật toán tìm kiếm có ràng buộc: Backtracking, Forward-Checking, Look-Ahead (AC-3)

---

### 2. Tính năng chính

- Giao diện trực quan: Hai bảng 8x8 được hiển thị song song:
  -   Board: vẽ quá trình tìm kiếm cách đặt quân.
  -   Goal Board: hiển thị trạng thái đích ngẫu nhiên (goal state) cho một vài thuật toán cần thiết. Goal Board sẽ sinh ngẫu nhiên với mỗi lần chạy chương trình.
- Hiển thị kết quả thuật toán:
  Các quân xe sẽ được vẽ dần sau mỗi bước duyệt ngầm, chi phí - cost sẽ được cập nhật ngay sau mỗi bước đặt quân và thời gian - time sẽ được cập nhật mới khi chạy xong một quá trình đặt quân.
- Các thuật toán được sử dụng:
  - `Uninformed Search`: Breadth-First Search (BFS), Depth-First Search (DFS), Depth-Limited Search (DLS), Iterative Deeping Search (IDS)
  - `Informed Search`: Greedy Best-First Search, A* Search, Uniform Cost Search (UCS)
  - `Local Search`: Hill Climbing, Simulated Annealing, Beam Search, Genetic
  - `Non-deterministic`: AND-OR Search, Belief State Search, Comformant Search
  - `Constraint Satisfaction Problem Search`: Backtracking, Forward-Checking, Look-Ahead (AC-3)
- Nút Clear Board: Dùng để xóa toàn bộ quân xe trên Board và reset lại các lựa chọn thuật toán.
- Nút Run: Chạy thuật toán đã chọn để tiến hành quá trình đặt quân xe.

---

### 3. Yêu cầu
- Ngôn ngữ lập trình: `Python`
- Các thư viện được xài: `customtkinter`, `tkinter`, `math`, `random`.
- Thư viện cần cài đặt: Customtkinter
    Cài trong Command hoặc PowerShell: `pip install customtkinter`

---

### 4. Cách sử dụng

- Chạy ứng dụng có tên file: `23110131_TrinhDaiNghia_BaitapCanhan.py`
- Chọn thuật toán: có tất cả 5 combobox cho 5 nhóm thuật toán.
  - Chọn 1 thuật toán trong 5 nhóm thuật toán.
  - Khi chọn xong, các combobox còn lại sẽ tự động khóa
- Chạy thuật toán:
  - Nhấn nút `Run` để bắt đầu chạy thuật toán.
  - Quá trình vẽ đặt quân sẽ hiển thị trên Board (bàn cơ bên trái UI).
  - Cost sẽ cập nhật liên tục sau mỗi lần đặt quân. Sau khi hoàn tất sẽ hiển thị thời gian - Time chạy thuật toán.
- Xóa kết quả và chạy lại:
  - Nhấn `Clear Board` để xóa bàn cờ hiện tại và có thể chạy lại thuật toán hoặc chọn lại 1 thuật toán khác.

 ---

### 5. Cấu trúc file `23110131_TrinhDaiNghia_BaitapCanhan.py`

- Khởi tạo, cấu hình UI với `Customtkinter`.
- Vẽ bảng 8x8 gồm BoardA - bàn cờ dùng để vẽ và Goal Board - bàn cờ mục tiêu (goal state).
- Các hàm tiện ích: vẽ quân xe, update cost/time, clear board.
- Định nghĩa các hàm thuật toán tìm kiếm (BFS, DFS, UCS, A*, Hill Climbing, v.v…) và các hàm con cần thiết.
- Khởi tạo các comboBox dùng để chứa và xếp các thuật toán theo đúng nhóm thuật toán.
- Khởi tạo 2 nút `Run` và `Clear Board`
