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
      - Board: vẽ quá trình tìm kiếm cách đặt quân.
      - Goal Board: hiển thị trạng thái đích ngẫu nhiên (goal state) cho một vài thuật toán cần thiết.

