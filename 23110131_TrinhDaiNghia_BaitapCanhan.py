import math
import random
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox


import time

from collections import deque
from heapq import heappop, heappush

# ================== Setup CustomTkinter ==================
ctk.set_appearance_mode("light")       # "dark", "light", "system"
ctk.set_default_color_theme("blue")   # "blue", "green", "dark-blue"

# ================== Root ==================
root = ctk.CTk()
root.title("Search Algorithms Solve 8 Rooks")
root.geometry("1660x900")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


# ================== Main frame (lưu ý: không dùng padx/pady trong constructor) ==================
main = ctk.CTkFrame(root, corner_radius=20, width = 1000, height = 700)
main.grid(sticky="nsew", padx=20, pady=20)
main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
main.pack_propagate(False)

# ================== Hai bảng (frames + label + canvas) ==================

left_side = ctk.CTkFrame(main, corner_radius=8)
left_side.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
left_side.rowconfigure(1, weight=1)
left_side.columnconfigure(0, weight=1)
left_side.configure(fg_color ="white")

right_side = ctk.CTkFrame(main, corner_radius=8)
right_side.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")
right_side.rowconfigure(1, weight=1)
right_side.columnconfigure(0, weight=1)
right_side.configure(fg_color ="white")

lbl_left_title = ctk.CTkLabel(left_side, text="Board", font=("Arial", 14, "bold"))
lbl_left_title.grid(row=0, column=0, pady=(0,6), sticky="e")

lbl_right_title = ctk.CTkLabel(right_side, text="Goal Board", font=("Arial", 14, "bold"))
lbl_right_title.grid(row=0, column=0, pady=(0,6))

# ================== Cấu hình bảng (dùng tk.Canvas để giữ nguyên API canvas) ==================
CELL_SIZE = 80    # Kích thước mỗi ô (trước có thể là 60)
N = 8             # Số ô theo chiều ngang/dọc
BOARD = CELL_SIZE * N

# Giữ layout ổn định, không co giãn khi resize
left_side.grid_columnconfigure(0, weight=1)
left_side.grid_columnconfigure(1, weight=1)
left_side.grid_propagate(False)
right_side.grid_columnconfigure(0, weight=1)
right_side.grid_propagate(False)

# Tạo canvas cho BoardA (chiếm cả 2 cột để căn giữa)
boardA = tk.Canvas(left_side, width=BOARD, height=BOARD, bg="white", highlightthickness=0)
boardA.grid(row=1, column=0, columnspan=2, sticky="n")

boardB = tk.Canvas(right_side, width=BOARD, height=BOARD, bg="white", highlightthickness=0)
boardB.grid(row=1, column=0, sticky="n")

# ================== Data structures cho canvas ids ==================
rect_id_lf = [[None] * N for _ in range(N)]
chess_id_lf = [[None] * N for _ in range(N)]
rect_id_right = [[None] * N for _ in range(N)]
chess_id_right = [[None] * N for _ in range(N)]
car_id_lef = [[None] * N for _ in range(N)]
last_run = None

# ================== Vẽ lưới 8x8 cho 2 bảng ==================
for r in range(N):
    for c in range(N):
        x1, y1 = c * CELL_SIZE, r * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"

        # Vẽ trên board A
        rid = boardA.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        rect_id_lf[r][c] = rid
        boardA.addtag_withtag(f"l_{r}_{c}", rid)

        # Vẽ trên board B
        rid2 = boardB.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        rect_id_right[r][c] = rid2
        boardB.addtag_withtag(f"l_{r}_{c}", rid2)


# ================== Control panel (không dùng padx/pady trong constructor) ==================
ctrl = ctk.CTkFrame(main, corner_radius=8)
ctrl.grid(row=1, column=0, columnspan=2, sticky="ew", padx=6, pady=6)
for i in range(4):
    ctrl.columnconfigure(i, weight=1)

# Labels cost/time chia 2 cột dưới
lblCost = ctk.CTkLabel(left_side, text="Cost: 0", font=("Arial", 14, "bold"), width=120, anchor="w")
lblCost.grid(row=9, column=0, padx=6, pady=6, sticky="ew")

lblTime = ctk.CTkLabel(left_side, text="Time: 0.0", font=("Arial", 14, "bold"), width=120, anchor="e")
lblTime.grid(row=9, column=1, padx=6, pady=6, sticky="ew")


# ================== Utility functions (unchanged logic) ==================
def update_Time(val):
    lblTime.configure(text=f"Time: {val:.1f}")
    root.update_idletasks()

def update_Cost(val):
    lblCost.configure(text=f"Cost: {val}")
    root.update_idletasks()

def clear_boards():
    for r in range(N):
        for c in range(N):
            if car_id_lef[r][c] is not None:
                boardA.delete(car_id_lef[r][c])
                car_id_lef[r][c] = None
    update_Time(0)
    update_Cost(0)


    # Reset lại combobox
    UninformedSearch.set(default_texts["uninformed"])
    InformedSearch.set(default_texts["informed"])
    LocalSearch.set(default_texts["local"])
    CSPSearch.set(default_texts["csp"])
    CESearch.set(default_texts["complex enviroment"])

    combo1.configure(state="readonly")
    combo2.configure(state="readonly")
    combo3.configure(state="readonly")
    combo4.configure(state="readonly")
    combo5.configure(state="readonly")




# ================== Vẽ kết quả (giữ nguyên API, đổi TILE -> CELL_SIZE) ==================
def draw_cars_inBoardA(sol):
    # Xóa quân cũ
    for r in range(N):
        for c in range(N):
            if car_id_lef[r][c] is not None:
                boardA.delete(car_id_lef[r][c])
                car_id_lef[r][c] = None

    # Vẽ solution mới
    for r, c in enumerate(sol):
        if c >= 0:
            cx, cy = c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2
            car_id_lef[r][c] = boardA.create_text(
                cx, cy,
                text="♖",
                font=("Arial", int(CELL_SIZE * 0.8))
            )

def draw_chess_inBoardB(sol):
    # Xóa quân cũ
    for r in range(N):
        for c in range(N):
            if chess_id_right[r][c] is not None:
                boardB.delete(chess_id_right[r][c])
                chess_id_right[r][c] = None

    # Vẽ solution mới
    for r, c in enumerate(sol):
        if c >= 0:
            cx, cy = c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2
            chess_id_right[r][c] = boardB.create_text(
                cx, cy,
                text="♖",
                font=("Arial", int(CELL_SIZE * 0.8))
            )


# ================== Goal / helpers ==================
def Goal_Board():
    cols = list(range(N))
    random.shuffle(cols)
    return cols

def is_goal_State(solution, Goal_Board):
    return solution == Goal_Board

def Anounce(solutions, Goal_Board):
    found = False
    for sol in solutions:
        if is_goal_State(sol, Goal_Board):
            found = True
            break
    if found:
        messagebox.showinfo("Thông báo", "Tìm thấy 1 lời giải")
    else:
        messagebox.showinfo("Thông báo", "Không tìm thấy lời giải")

def is_safe(state, row, col):
    for _, c in enumerate(state):
        if c == col:
            return False
    return True

def is_goal(state):
    return len(state) == N

def get_state(state):
    row = len(state)
    cols = list(range(N))
    random.shuffle(cols)
    return [state + [col] for col in cols if is_safe(state, row, col)]

# ================== Init goal và vẽ ==================
goal = Goal_Board()
draw_chess_inBoardB(goal)

# BFS
def BFS_8Cars():
    start = time.time()
    solution= None
    queue = deque([[]])
    while queue:
        state = queue.popleft()
        if is_goal(state):
            solution = state
            break
        for child in get_state(state):
            queue.append(child)
    if solution:
        for i in range(1, len(solution) + 1):
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution
    end = time.time()
    update_Time(end - start)
    return None

# DFS
def DFS_8Cars():
    start = time.time()
    solution= None
    stack = [[]]
    while stack:
        state = stack.pop()
        if is_goal(state):
            solution = state
            break
        for child in reversed(get_state(state)):
            stack.append(child)

    if solution:
        for i in range(1, len(solution) + 1):
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution
    end = time.time()
    update_Time(end - start)
    return None

# UCS
def cost_UCS(state, row, col):
    m = len(set(state + [col]))
    i = row + 1
    return m + i

def UCS_8Cars():
    start = time.time()
    solution = None
    pq = [(0, [])]
    visited = set()
    while pq:
        total_cost, state = heappop(pq)
        key = tuple(state)
        if key in visited:
            continue
        visited.add(key)
        if is_goal(state):
            solution = state
            break
        row = len(state)
        for child in get_state(state):
            col = child[-1]
            step_cost = cost_UCS(state, row, col)
            heappush(pq, (total_cost + step_cost, child))
    if solution:
        total_cost = 0
        for i in range(1, len(solution) + 1):
            row = i - 1
            col = solution[row]
            step_cost = cost_UCS(solution[:row], row, col)
            total_cost += step_cost
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(total_cost)
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution

    end = time.time()
    update_Time(end - start)
    update_Cost(0)
    return None

# DLS
def DLS_8Cars_limit(limit):
    start = time.time()
    update_Cost(0)
    solution = None
    def dls(state, depth):
        nonlocal solution
        if depth > limit:
            return False
        if is_goal(state):
            solution =  state[:]
            return True
        if depth == limit:
            return False
        for child in get_state(state):
            if dls(child, depth + 1):
                return True
        return False

    dls([], 0)
    if solution is not None:
        for i in range(1, len(solution) + 1):
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        return None

def IDS_8Cars():
    start = time.time()
    state=[]
    solution = None
    def ids(state, depth, limit):
        nonlocal solution
        if is_goal(state):
            solution = state[:]
            return True
        if depth == limit:
            return False
        for child in get_state(state):
            if ids(child,depth + 1, limit):
                return True
        return False

    for limit in range(0, N+1):
            if ids(state, 0, limit):
                break
    if solution is not None:
        for i in range(1, len(solution) + 1):
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        return None

def count_conflicts(state):
    seen = set()
    conflicts = 0
    for col in state:
        if col in seen:
            conflicts += 1
        else:
            seen.add(col)
    return conflicts


def heuristic(state,Goal_Board):
    row = len(state)
    missing = N - row
    conflict = count_conflicts(state)
    penalty = 0
    for i in range(0,row):
        if state[i] != Goal_Board[i]:
            penalty += 1
    return missing + conflict + penalty

def GreedySearch():
    start = time.time()
    solution = None
    pq= []
    heappush(pq,(heuristic([],goal),[]))
    vs= set()

    while pq:
        (h_val, state) = heappop(pq)
        key = tuple(state)
        if key in vs:
            continue
        vs.add(key)

        if is_goal(state):
            solution = state
            break
        row = len(state)

        for child in get_state(state):
            if tuple(child) not in vs:
                h_child = heuristic(child,goal)
                heappush(pq, (h_child,child))


    if solution is not None:
        for i in range(1, len(solution) + 1):
            partial = solution[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return solution
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        return None

def ASSearch_8Cars():
    start_time = time.time()

    start = []
    start_key = tuple(start)

    pq = []
    g_scores = {start_key: 0}
    f_start = g_scores[start_key] + heuristic(start,goal)
    heappush(pq, (f_start, 0, start))

    came_from = {}
    closed = set()
    solution = None

    while pq:
        f_curr, g_curr, state = heappop(pq)
        key = tuple(state)

        if key in closed:
            continue

        # goal test
        if is_goal(state):
            solution = state
            break

        closed.add(key)
        row = len(state)


        for child in get_state(state):
            child_key = tuple(child)
            step_cost = cost_UCS(state, row, child[-1])
            g_child = g_curr + step_cost


            if child_key in g_scores and g_child >= g_scores[child_key]:
                continue


            g_scores[child_key] = g_child
            came_from[child_key] = key
            f_child = g_child + heuristic(child,goal)
            heappush(pq, (f_child, g_child, child))

    # nếu tìm được solution, reconstruct path và animate
    if solution is not None:
        path_keys = []
        k = tuple(solution)
        while True:
            path_keys.append(k)
            if k == start_key:
                break
            k = came_from.get(k)
            if k is None:   # phòng trường hợp mất came_from
                break
        path_keys.reverse()

        for k in path_keys[1:]:   # (bỏ start nếu muốn)
            s = list(k)
            draw_cars_inBoardA(s)
            update_Cost(g_scores.get(k, 0))
            root.update()
            root.after(300)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start_time)
        return solution
    end = time.time()
    update_Time(end - start_time)
    update_Cost(0)
    return None

def HCSearch():
    start= time.time()
    state= random.choice(get_state([]))
    solution= [state]
    while True:
        neighbors = get_state(state)
        if not neighbors:
            break
        next = min(neighbors, key= lambda s:heuristic(s,goal))
        if heuristic(next,goal) >= heuristic(state,goal):
            break
        state = next
        solution.append(state)
    if solution:
        for sol in solution:
                draw_cars_inBoardA(sol)
                update_Cost(heuristic(sol,goal))  # mỗi path sẽ hiển thị cost khác nhau
                root.update()
                root.after(500)
        Anounce(solution, goal)
        end = time.time()
        update_Time(end - start)
        return solution

def BeamSearch():
    start_time = time.time()
    solution = []
    start= []
    beam = [start]
    global k
    k = max(1, N // 2)
    while beam:
        for state in beam:
            if is_goal(state):
                solution.append(state)

        if solution:
            for sol in solution:
                total_cost = 0
                for i in range(1, len(sol) + 1):
                    partial = sol[:i]
                    # tính step_cost tại đây (nếu cần)
                    row = i - 1
                    col = sol[row]
                    step_cost = cost_UCS(sol[:row], row, col)
                    total_cost += step_cost

                    draw_cars_inBoardA(partial)
                    update_Cost(total_cost)  # mỗi path sẽ hiển thị cost khác nhau
                    root.update()
                    root.after(500)
            Anounce(solution, goal)
            end = time.time()
            update_Time(end - start_time)
            return solution

        successors = []
        for state in beam:
            for child in get_state(state):
                h= heuristic(child,goal)
                successors.append((h, child))

        if not successors:
            return None

        successors.sort(key=lambda x: x[0])
        beam = [child for (_, child) in successors[:k]]
    return None

def SA():
    start = time.time()
    state = random.choice(get_state([]))
    best_state = state[:]
    solution = []
    T = 100
    alpha= 0.95
    max_iter = 1000
    for _ in range(max_iter):
        neighbors = get_state(state)
        if not neighbors:
            break
        next = random.choice(neighbors)
        deltaE = heuristic(next, goal) - heuristic(state, goal)
        if deltaE < 0 or random.random() < math.exp(-deltaE / T):
            state = next
            solution.append(state)
            if heuristic(next, goal) < heuristic(state, goal):
                best_state = state[:]
        T *= alpha
        if state == goal:
            break

    if solution:
        for sol in solution:
            draw_cars_inBoardA(sol)
            update_Cost(heuristic(sol, goal))  # mỗi path sẽ hiển thị cost khác nhau
            root.update()
            root.after(500)
        Anounce([solution], goal)
        end = time.time()
        update_Time(end - start)
        return best_state
    end = time.time()
    update_Time(end - start)

def conflicts(ind):
    # Đếm số cột bị trùng nhau
    return len(ind) - len(set(ind))

def fitness(ind,goal):
    return sum(1 for i in range(N) if ind[i] == goal[i])


#Sinh quần thể bna đầu
def init_population(size):
    population= []
    for _ in range(size):
        ind  = [random.randint(0,N-1) for _ in range(N)]
        population.append(ind)
    return population

#Đếm số quân hợp lệ

#Tính fitness
def evaluate_pop(population):
    return [fitness(ind) for ind in population]


#Chọn ngẫu nhiên k cá thể tốt nhất
def tour_select(pop, fit, k= 3):
    idxs = random.sample(range(len(pop)), k)
    best_idx = max(idxs, key= lambda i: fit[i])
    return pop[best_idx][:]

#Sinh con hợp l từ cha mẹ
def order_crossover(p1, p2):
    n = len(p1)
    cut = random.randint(1,N-1)
    return p1[:cut] + p2[cut:]

#Làm đột biến
def swap_mutation(ind, mutation_rate=0.2):
    ind = ind[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    return ind

def GA_8Cars():
    start = time.time()
    pop_size = 100
    max_gens = 1000
    mutation_rate = 0.2
    crossover_rate = 0.9
    elitism = 1

    pop = init_population(pop_size)
    max_fitness = N
    best_ind = None
    best_fit = -1

    for gen in range(max_gens):
        fitnesses = [fitness(ind, goal) for ind in pop]
        gen_best_fit = max(fitnesses)
        gen_best = pop[fitnesses.index(gen_best_fit)]

        if gen_best_fit > best_fit:
            best_fit = gen_best_fit
            best_ind = gen_best[:]



        # animate every 100 generations (optional)
        if gen % 50 == 0:
            draw_cars_inBoardA(best_ind)
            update_Cost(conflicts(best_ind))
            root.update()
            root.after(200)


        if best_fit == max_fitness:
            break

        if best_ind == goal:
            break
        # elitism
        sorted_pop = [ind for _, ind in sorted(zip(fitnesses, pop), key=lambda x: -x[0])]
        new_pop = [sorted_pop[i] for i in range(elitism)]

        while len(new_pop) < pop_size:
            p1 = tour_select(pop, fitnesses)
            p2 = tour_select(pop, fitnesses)
            if random.random() < crossover_rate:
                child = order_crossover(p1, p2)
            else:
                child = p1
            child = swap_mutation(child, mutation_rate)
            new_pop.append(child)

        pop = new_pop

    # final draw
    if best_ind is not None:
        draw_cars_inBoardA(best_ind)
        update_Cost(conflicts(best_ind))
        root.update()
        root.after(500)
        messagebox.showinfo("GA", f"Tìm ra solution với độ tương thích {best_fit:.1f}/{max_fitness}")
        end = time.time()
        update_Time(end - start)
        return best_ind
    else:
        messagebox.showinfo("GA", "Không tìm thấy solution")
        end = time.time()
        update_Time(end - start)
        return None

def get_outcomes(state):
    row = len(state)
    cols = list(range(N))
    outcomes=[]
    random.shuffle(cols)
    for c in cols:
        if is_safe(state,row, c):
            outcomes.append(state)

    return outcomes

def AndOrSearch():
    start_time = time.time()
    start = []
    path = set()
    plan = OrSearch(start, path, goal)  # tìm plan từ start đến goal
    if not plan:
        messagebox.showinfo("And-Or Search", "Không tìm thấy solution")
        return None

    # Animate solution
    total_cost = 0
    for i, state in enumerate(plan):
        draw_cars_inBoardA(state)
        total_cost += 1
        update_Cost(total_cost)
        root.update()
        root.after(500)
        end = time.time()
        update_Time(end - start_time)
    messagebox.showinfo("And-Or Search", "Đã tìm thấy solution")
    return plan



def OrSearch(state,path,goal):
    key = tuple(state)

    if key in path:
        return False
    if state == goal:
        return [state]


    path.add(key)


    for child in get_state(state):
        outcomes = get_outcomes(child)
        #Lưu ý: Vì sử dụng haàm get_outcomes để sinh ra có trạng thái sau mỗi lần chọn dc Or node nên khi đưa qua sử lý AND có thể gây ra tình trạng không tìm được solution
        #Vì thế nếu muốn tìm được thì bỏ outcome = get_outcomes(child), thay plan dưới bằng plan = AndSearch([child],path, goal) --> tìm thấy solution goal_state nhưng mất đi bản chất của AND-Node --> AND-OR Search thành DFS/Greedy
        plan = AndSearch(outcomes,path, goal)
        if plan:
            path.remove(key)
            return [state] + plan

    path.remove(key)
    return False


def AndSearch(states, path, goal):
    plans=[]
    for s in states:
        res = OrSearch(s,path, goal)
        if not res:
            return False
        plans.extend(res)
    return plans


def BacktrackingSearch():
    start = time.time()
    def backtrack(state, row):
        if row == N:
            return state[:]

        for col in range(N):
            if is_safe(state, row, col):
                state.append(col)
                res = backtrack(state, row + 1)
                if res is not None:
                    return res
                state.pop()
        return None
    sol = backtrack([], 0)
    if sol:
        for i in range(1,len(sol) + 1):
            partial = sol[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(500)
            end = time.time()
            update_Time(end - start)
        return sol
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        messagebox.showinfo("Backtracking Search", "Không tìm thấy solution")
        return None

def forward_check(domains, row, col):
        checked_domains = {r: list(cols) for r, cols in domains.items()}
        checked_domains[row] = [col]
        for r in range(row + 1, N):
            if col in checked_domains[r]:
                checked_domains[r].remove(col)

            if not checked_domains[r]:
                return None
        return checked_domains

def FCSearch():
    start = time.time()
    def backtrack(state, row, domains):
        if row == N:
            return state[:]

        for col in list(domains[row]):
            new_domains = forward_check(domains, row, col)
            if new_domains is not None:
                state.append(col)
                res = backtrack(state, row +1, new_domains)
                if res is not None:
                    return res
                state.pop()
        return None

    domains = {r: list(range(N)) for r in range(N)}
    sol= backtrack([],0,domains)
    if sol:
        for i in range(1,len(sol) + 1):
            partial = sol[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(500)
            end = time.time()
            update_Time(end - start)
        return sol
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        messagebox.showinfo("Backtracking Search", "Không tìm thấy solution")
        return None


def is_consistent(i, x ,j,y):
    return x!=j

def Look_AheadSearch():
    start = time.time()
    domains = {r: list(range(N)) for r in range(N)}  # mỗi hàng có N cột khả dĩ
    const= [(i, j) for i in range(N) for j in range(N) if i != j]
    def backtrack(state, row, domains):
        if row == N:
            return state[:]
        for col in list(domains[row]):
            new_domains = forward_check(domains, row, col)
            if new_domains is not None:
                state.append(col)
                if AC3(new_domains, const):
                    res = backtrack(state, row + 1, new_domains)
                    if res is not None:
                        return res
                state.pop()
        return None
    sol = backtrack([], 0, domains)
    if sol is not None:
        for i in range(1, len(sol) + 1):
            partial = sol[:i]
            draw_cars_inBoardA(partial)
            update_Cost(len(partial))
            root.update()
            root.after(500)
            end = time.time()
            update_Time(end - start)

        messagebox.showinfo("Look-ahead (MAC)", "Tìm thấy solution")
        return sol
    else:
        end = time.time()
        update_Time(end - start)
        update_Cost(0)
        messagebox.showinfo("Look-ahead (MAC)", "Không tìm thấy solution")
        return None

def AC3(domains, const):
    def revise(domains, i, j):
        revised = False
        for x in domains[i][:]:
            # nếu không tồn tại y trong domain[Xj] mà (x,y) thỏa constraint
            if not any(is_consistent(i,x,j,y) for y in domains[j]):
                domains[i].remove(x)
                revised = True
        return revised

    queue= deque((i, j) for (i, j) in const)
    while queue:
        i, j = queue.popleft()
        if revise(domains, i, j):
            if not domains[i]:
                return False
            for k in range(N):
                if k != i and k != j:
                    queue.append((k,i))
    return True

def belief_successors(belief):
    """Sinh các belief kế tiếp (mỗi belief chứa 1 tập trạng thái con hợp lệ)."""
    successors = []

    # Với mỗi state trong belief hiện tại
    for state in belief:
        child_states = get_state(list(state))
        # Mỗi child state tạo thành 1 belief riêng (để mở rộng độc lập)
        for child in child_states:
            successors.append(set([tuple(child)]))

    return successors


def belief_Search():
    start_time = time.time()
    start = tuple([])          # trạng thái khởi đầu
    belief = set([start])      # belief ban đầu: chỉ có 1 state rỗng

    frontier = deque([belief]) # hàng đợi các belief cần mở rộng
    visited = set()            # đánh dấu belief đã thăm
    parent = {}
    solution = None

    while frontier:
        curr_b = frontier.popleft()

        if frozenset(curr_b) in visited:
            continue
        visited.add(frozenset(curr_b))

        # Kiểm tra nếu belief hiện tại chứa goal
        for state in curr_b:
            if is_goal(list(state)):
                solution = curr_b
                break
        if solution:
            break

        # Sinh các belief kế tiếp
        for succ_b in belief_successors(curr_b):
            if frozenset(succ_b) not in visited:
                frontier.append(succ_b)
                parent[frozenset(succ_b)] = frozenset(curr_b)

    # Nếu có solution
    if solution:
        goal_state = None
        for st in solution:
            if is_goal(list(st)):
                goal_state = list(st)
                break

        if goal_state:
            for i in range(1, len(goal_state) + 1):
                partial = goal_state[:i]
                draw_cars_inBoardA(partial)
                update_Cost(len(partial))
                root.update()
                root.after(300)
            Anounce([goal_state], goal)
            end = time.time()
            update_Time(end - start_time)
            return goal_state

    # Không tìm thấy solution
    end = time.time()
    update_Time(end - start_time)
    update_Cost(0)
    messagebox.showinfo("Belief State Search", "Không tìm thấy solution")
    return None




def ConformantSearch():
        start_time = time.time()

        # --- Build a sampled initial belief (set of full board states) ---
        # We sample a modest number of random full assignments to keep search feasible.
        sample_size = 40  # thay đổi nếu muốn (giảm để nhanh hơn, tăng để "độ phủ" belief cao hơn)

        def random_full_state():
            # state representation: tuple length N, state[r] = column for row r
            return tuple(random.randint(0, N - 1) for _ in range(N))

        initial_belief = set()
        while len(initial_belief) < sample_size:
            initial_belief.add(random_full_state())

        # --- Actions: set each row r to the goal column goal[r] (overwrite) ---
        # goal (list) đã được tạo ở phần trên của file: goal = Goal_Board()
        actions = [('set_row', r, goal[r]) for r in range(N)]

        start_belief = frozenset(initial_belief)
        frontier = deque([(start_belief, [])])
        visited = {start_belief}

        found_plan = None
        final_belief = None

        while frontier:
            b_frozen, plan = frontier.popleft()
            belief = set(b_frozen)

            # goal test for belief: Mọi state trong belief đã đạt goal chưa ?
            if all(tuple(s) == tuple(goal) for s in belief):
                found_plan = plan
                final_belief = belief
                break

            # Mở rộng với mỗi action
            for a in actions:
                r, c = a[1], a[2]
                new_belief = set()
                for s in belief:
                    lst = list(s)
                    lst[r] = c
                    new_belief.add(tuple(lst))

                newb_key = frozenset(new_belief)
                if newb_key not in visited:
                    visited.add(newb_key)
                    frontier.append((newb_key, plan + [a]))

        if found_plan is not None:
            # Nếu trạng thái ban đầu đã là trạng thái đích.
            if len(found_plan) == 0:
                draw_cars_inBoardA(goal)
                update_Cost(0)
                root.update()
                root.after(300)
                Anounce([goal], goal)
                end = time.time()
                update_Time(end - start_time)
                return goal
            #animate từng bước khi agent áp dụng action lên belief → thể hiện “quá trình giải quyết”
            partial = [-1] * N
            for step, act in enumerate(found_plan, start=1):
                r, c = act[1], act[2]
                partial[r] = c
                draw_cars_inBoardA(partial)
                update_Cost(step)
                root.update()
                root.after(300)

            # final announce: vẽ lại goal board hoàn chỉnh để chắc chắn màn hình hiển thị đúng trạng thái cuối.
            draw_cars_inBoardA(goal)
            update_Cost(len(found_plan))
            root.update()
            root.after(300)
            Anounce([goal], goal)
            end = time.time()
            update_Time(end - start_time)
            return list(goal)

        # no conformant plan found
        end = time.time()
        update_Time(end - start_time)
        messagebox.showinfo("Conformant Search", "Không tìm thấy solution (với initial belief đã sample)")
        return None


# ================== nút Run ==================
algorithms = {
    # Uninformed
    "BFS": BFS_8Cars,
    "DFS": DFS_8Cars,
    "DLS": lambda: DLS_8Cars_limit(8),
    "IDS": IDS_8Cars,
    # Informed
    "UCS": UCS_8Cars,
    "Greedy": GreedySearch,
    "A*": ASSearch_8Cars,
    #Local
    "Hill Climbing": HCSearch,
    "Simulated Annealing": SA,
    "Beam Search": BeamSearch,
    "Genetic": GA_8Cars,

    #Complex Enviroment
    "And-OR Search": AndOrSearch,
    "Belief state search": belief_Search,
    "Conformant Search": ConformantSearch,

    # CSP
    "Backtracking": BacktrackingSearch,
    "Forward-Checking": FCSearch,
    "Look-Ahead": Look_AheadSearch
}
UninformedSearch = ctk.StringVar(value="Chọn Uninformed Search")
InformedSearch = ctk.StringVar(value="Chọn Informed Search")
LocalSearch = ctk.StringVar(value ="Chọn Local Search")
CSPSearch = ctk.StringVar(value="Chọn CSP Search")
CESearch = ctk.StringVar(value="Chọn Complex Enviroment Search")
default_texts = {
    "uninformed": "Chọn Uninformed Search",
    "informed": "Chọn Informed Search",
    "local": "Chọn Local Search",
    "csp": "Chọn CSP Search",
    "complex enviroment": "Chọn Complex Enviroment Search"
}
def on_select_uninformed(choice):
    if choice != default_texts["uninformed"]:
        InformedSearch.set(default_texts["informed"])
        LocalSearch.set(default_texts["local"])
        CSPSearch.set(default_texts["csp"])
        CESearch.set(default_texts["complex enviroment"])
        combo2.configure(state="disabled")
        combo3.configure(state="disabled")
        combo4.configure(state="disabled")
        combo5.configure(state="disabled")

def on_select_informed(choice):
    if choice != default_texts["informed"]:
        UninformedSearch.set(default_texts["uninformed"])
        LocalSearch.set(default_texts["local"])
        CSPSearch.set(default_texts["csp"])
        CESearch.set(default_texts["complex enviroment"])
        combo1.configure(state="disabled")
        combo3.configure(state="disabled")
        combo4.configure(state="disabled")
        combo5.configure(state="disabled")

def on_select_local(choice):
    if choice != default_texts["local"]:
        UninformedSearch.set(default_texts["uninformed"])
        InformedSearch.set(default_texts["informed"])
        CSPSearch.set(default_texts["csp"])
        CESearch.set(default_texts["complex enviroment"])
        combo1.configure(state="disabled")
        combo2.configure(state="disabled")
        combo4.configure(state="disabled")
        combo5.configure(state="disabled")

def on_select_csp(choice):
    if choice != default_texts["csp"]:
        UninformedSearch.set(default_texts["uninformed"])
        InformedSearch.set(default_texts["informed"])
        LocalSearch.set(default_texts["local"])
        CESearch.set(default_texts["complex enviroment"])
        combo1.configure(state="disabled")
        combo2.configure(state="disabled")
        combo3.configure(state="disabled")
        combo5.configure(state="disabled")

def on_select_ce(choice):
    if choice != default_texts["complex enviroment"]:
        UninformedSearch.set(default_texts["uninformed"])
        InformedSearch.set(default_texts["informed"])
        LocalSearch.set(default_texts["local"])
        CSPSearch.set(default_texts["csp"])
        combo1.configure(state="disabled")
        combo2.configure(state="disabled")
        combo3.configure(state="disabled")
        combo4.configure(state="disabled")


combo1 = ctk.CTkComboBox(ctrl, values=["BFS", "DFS", "DLS", "IDS"],
                         variable=UninformedSearch, state="readonly",
                         command=on_select_uninformed)

combo2 = ctk.CTkComboBox(ctrl, values=["UCS", "Greedy", "A*"],
                         variable=InformedSearch, state="readonly",
                         command=on_select_informed)

combo3 = ctk.CTkComboBox(ctrl, values=["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic", ],
                         variable=LocalSearch, state="readonly",
                         command=on_select_local)

combo4 = ctk.CTkComboBox(ctrl, values=["Backtracking", "Forward-Checking", "Look-Ahead"],
                         variable=CSPSearch, state="readonly",
                         command=on_select_csp)
combo5 = ctk.CTkComboBox(ctrl, values=["And-OR Search", "Belief state search", "Conformant Search"], #Conformant Search - Tìm kiếm trong môi trường nhìn thấy 1 phần
                         variable=CESearch, state="readonly",
                         command=on_select_ce)


combo1.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
combo2.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
combo3.grid(row=0, column=2, padx=6, pady=6, sticky="ew")
combo4.grid(row=0, column=3, padx=6, pady=6, sticky="ew")
combo5.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

def run_algorithm():
    selected = None
    # Ưu tiên lấy giá trị nào khác mặc định
    if UninformedSearch.get() != "Chọn Uninformed Search":
        selected = UninformedSearch.get()
    elif InformedSearch.get() != "Chọn Informed Search":
        selected = InformedSearch.get()
    elif LocalSearch.get() != "Chọn Local Search":
        selected = LocalSearch.get()
    elif CSPSearch.get() != "Chọn CSP Search":
        selected = CSPSearch.get()
    elif CESearch.get() != "Chọn Complex Envirment Search":
        selected = CESearch.get()

    #Nếu không chọn hoặc chưa chọn
    if not selected:
        messagebox.showwarning("Warning", "Chưa chọn thuật toán")
        return
    clear_boards()
    algorithms[selected]()  # gọi hàm đúng

btnClear = ctk.CTkButton(ctrl, text = "Clear board", command= clear_boards)
btnClear.grid(row = 3, column= 2, padx = 6, pady = 6, sticky ="ew")

btnRun = ctk.CTkButton(ctrl, text = "Run", command= run_algorithm)
btnRun.grid(row = 3, column= 3, padx = 6, pady = 6, sticky ="ew")


# ================== Start mainloop ==================
root.mainloop()
