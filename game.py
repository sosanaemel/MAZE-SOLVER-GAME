import tkinter as tk
from tkinter import messagebox
import queue
import random

# إعدادات اللعبة
CELL_SIZE = 35
PADDING = 10
MAZE_WIDTH = 15
MAZE_HEIGHT = 15

class MazeGenerator:
    """مولد متاهات عشوائية مع بداية بها طريقين"""
    
    @staticmethod
    def generate_maze(width, height):
        # إنشاء متاهة مليئة بالجدران
        maze = [["#" for _ in range(width)] for _ in range(height)]
        
        # نقطة البداية
        start_x, start_y = 1, 1
        maze[start_y][start_x] = " "
        
        # Stack للـ DFS
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            
            # الاتجاهات الممكنة
            random.shuffle(directions)
            found = False
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (1 <= nx < width - 1 and 1 <= ny < height - 1 and 
                    (nx, ny) not in visited):
                    # إزالة الجدار بين الخليتين
                    maze[y + dy // 2][x + dx // 2] = " "
                    maze[ny][nx] = " "
                    
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    found = True
                    break
            
            if not found:
                stack.pop()
        
        # وضع نقطة البداية والنهاية
        maze[1][1] = "O"
        
        # إنشاء طريقين من نقطة البداية
        MazeGenerator.create_two_paths_from_start(maze, start_x, start_y)
        
        # البحث عن أبعد نقطة من البداية للنهاية
        end_pos = MazeGenerator.find_farthest_point(maze, (1, 1))
        maze[end_pos[0]][end_pos[1]] = "X"
        
        return maze
    
    @staticmethod
    def create_two_paths_from_start(maze, start_x, start_y):
        """إنشاء طريقين مختلفين من نقطة البداية"""
        # الاتجاهات الممكنة من نقطة البداية
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        # اختيار أول اتجاهين صالحين لإنشاء طريقين
        path_count = 0
        paths_created = []
        
        for dx, dy in directions:
            nx, ny = start_x + dx, start_y + dy
            
            if (1 <= nx < len(maze[0]) - 1 and 1 <= ny < len(maze) - 1 and
                maze[ny][nx] == "#"):
                
                # فحص إذا كان هذا الاتجاه يؤدي إلى طريق حقيقي
                if MazeGenerator.is_valid_path_direction(maze, start_x, start_y, dx, dy):
                    maze[ny][nx] = " "
                    paths_created.append((nx, ny))
                    path_count += 1
                    
                    if path_count >= 2:
                        break
        
        # إذا لم نتمكن من إنشاء طريقين، ننشئ طريقاً إضافياً بالقوة
        if path_count < 2:
            for dx, dy in directions:
                nx, ny = start_x + dx, start_y + dy
                
                if (1 <= nx < len(maze[0]) - 1 and 1 <= ny < len(maze) - 1 and
                    maze[ny][nx] == "#" and (nx, ny) not in paths_created):
                    
                    maze[ny][nx] = " "
                    paths_created.append((nx, ny))
                    path_count += 1
                    
                    if path_count >= 2:
                        break
    
    @staticmethod
    def is_valid_path_direction(maze, x, y, dx, dy):
        """فحص إذا كان الاتجاه يؤدي إلى طريق حقيقي وليس طريق مسدود مباشر"""
        nx, ny = x + dx, y + dy
        
        # فحص الخلايا المجاورة للخلية الجديدة
        neighbor_count = 0
        for ddx, ddy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nnx, nny = nx + ddx, ny + ddy
            
            if (0 <= nnx < len(maze[0]) and 0 <= nny < len(maze) and
                maze[nny][nnx] != "#" and not (nnx == x and nny == y)):
                neighbor_count += 1
        
        # نريد طريقاً له على الأقل جار واحد غير نقطة البداية
        return neighbor_count > 0
    
    @staticmethod
    def find_farthest_point(maze, start):
        """إيجاد أبعد نقطة من البداية باستخدام BFS"""
        q = queue.Queue()
        q.put((start, 0))
        visited = {start}
        farthest = start
        max_dist = 0
        
        while not q.empty():
            (row, col), dist = q.get()
            
            if dist > max_dist:
                max_dist = dist
                farthest = (row, col)
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and
                    (nr, nc) not in visited and maze[nr][nc] != "#"):
                    visited.add((nr, nc))
                    q.put(((nr, nc), dist + 1))
        
        return farthest

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Maze Game - Player vs AI")
        
        # الألوان - ألوان الأزرق
        self.colors = {
            'wall': '#1E3A8A',          # أزرق داكن (لون الجدران)
            'wall_lines': '#FFFFFF',    # خطوط بيضاء على الجدران
            'path': '#E0F2FE',          # أزرق فاتح جداً (للمسارات)
            'start': '#3B82F6',         # أزرق فاتح (نقطة البداية)
            'end': '#FF6B6B',           # أحمر مرجاني (نقطة النهاية - لون مختلف)
            'player': '#2563EB',        # أزرق (اللاعب)
            'ai': '#EF4444',            # أحمر (الذكاء الاصطناعي)
            'player_trail': '#60A5FA',  # أزرق فاتح (مسار اللاعب)
            'ai_trail': '#FCA5A5',      # أحمر فاتح (مسار الذكاء الاصطناعي)
            'start_paths': '#A5D8FF',   # أزرق فاتح للطرق من البداية
            'bg': '#F0F9FF',            # أزرق فاتح جداً (خلفية اللعبة)
            'text': '#1E3A8A',          # أزرق داكن للنصوص
            'button_bg': '#3B82F6',     # أزرق للأزرار
            'button_fg': '#FFFFFF',     # أبيض لنص الأزرار
            'button_end_bg': '#FF6B6B', # أحمر مرجاني لزر End
            'error': '#DC2626',         # أحمر للرسائل الخطأ
            'player_lost': '#94A3B8',   # رمادي للاعب عندما يخسر
            'same_path': '#FBBF24',     # أصفر للخلايا المشتركة
            'same_path_trail': '#F59E0B' # أصفر داكن لمسار الخلايا المشتركة
        }
        
        # متغيرات اللعبة
        self.player_stuck = False  # هل توقف اللاعب؟
        self.player_lost = False   # هل خسر اللاعب؟
        self.ai_auto_moving = False  # هل AI يتحرك تلقائياً؟
        self.start_paths = []      # الطرق المتاحة من نقطة البداية
        self.same_path_cells = set()  # الخلايا التي سلكها اللاعب وAI معاً
        self.previous_player_pos = None  # لتتبع حركة اللاعب
        
        # تغيير خلفية النافذة الرئيسية
        self.root.configure(bg=self.colors['bg'])
        
        # إعداد Canvas
        canvas_width = MAZE_WIDTH * CELL_SIZE + PADDING * 2
        canvas_height = MAZE_HEIGHT * CELL_SIZE + PADDING * 2
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, 
                                bg=self.colors['path'], highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # إعداد معلومات اللعبة
        info_frame = tk.Frame(root, bg=self.colors['bg'])
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.round_label = tk.Label(info_frame, text="Round: 1", font=('Arial', 12, 'bold'), 
                                    fg=self.colors['text'], bg=self.colors['bg'], anchor='w')
        self.round_label.pack(side='left', padx=10)
        
        self.info_label = tk.Label(info_frame, text="", font=('Arial', 12), 
                                   fg=self.colors['text'], bg=self.colors['bg'], anchor='w')
        self.info_label.pack(side='left', padx=10)
        
        self.status_label = tk.Label(info_frame, text="Choose a path from START!", 
                                     font=('Arial', 11), fg=self.colors['text'], bg=self.colors['bg'])
        self.status_label.pack(side='left', padx=20)
        
        # إطار الأزرار
        btn_frame = tk.Frame(root, bg=self.colors['bg'])
        btn_frame.pack(pady=5)
        
        # تصميم الأزرار بألوان الأزرق
        button_style = {
            'font': ('Arial', 11, 'bold'),
            'width': 12,
            'height': 1,
            'bd': 2,
            'relief': 'raised'
        }
        
        self.new_maze_btn = tk.Button(btn_frame, text="New Maze", command=self.generate_new_maze,
                                      bg=self.colors['button_bg'], fg=self.colors['button_fg'], **button_style)
        self.new_maze_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="Reset Round", command=self.reset_game,
                                   bg=self.colors['end'], fg=self.colors['button_fg'], **button_style)
        self.reset_btn.pack(side='left', padx=5)
        
        # تتبع النقاط
        self.player_wins = 0
        self.ai_wins = 0
        self.current_round = 1
        
        self.score_label = tk.Label(root, text="", font=('Arial', 13, 'bold'), 
                                    fg=self.colors['text'], bg=self.colors['bg'])
        self.score_label.pack(pady=5)
        
        # رسالة خطأ
        self.error_label = tk.Label(root, text="", font=('Arial', 10, 'bold'), 
                                   fg=self.colors['error'], bg=self.colors['bg'])
        self.error_label.pack(pady=2)
        
        # مؤشر الخلايا المشتركة
        self.same_path_indicator = tk.Label(root, text="", font=('Arial', 10), 
                                           fg=self.colors['same_path'], bg=self.colors['bg'])
        self.same_path_indicator.pack(pady=2)
        
        # توليد متاهة جديدة
        self.maze = None
        self.generate_new_maze()
        
        # ربط أزرار لوحة المفاتيح
        self.root.bind('<Up>', lambda e: self.move_player(-1, 0))
        self.root.bind('<Down>', lambda e: self.move_player(1, 0))
        self.root.bind('<Left>', lambda e: self.move_player(0, -1))
        self.root.bind('<Right>', lambda e: self.move_player(0, 1))
    
    def generate_new_maze(self):
        """توليد متاهة جديدة"""
        self.maze = MazeGenerator.generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.reset_game()
    
    def reset_game(self):
        """إعادة تشغيل اللعبة بنفس المتاهة"""
        self.start_pos = self.find_start(self.maze, "O")
        self.end_pos = self.find_start(self.maze, "X")
        
        self.player_pos = list(self.start_pos)
        self.ai_pos = list(self.start_pos)
        
        self.player_path = []
        self.ai_path = []
        
        self.player_visited = {tuple(self.start_pos)}
        self.ai_visited = {tuple(self.start_pos)}
        self.same_path_cells = set()
        self.previous_player_pos = None
        
        self.game_over = False
        self.winner = None
        self.player_stuck = False
        self.player_lost = False
        self.ai_auto_moving = False
        
        # العثور على الطرق المتاحة من نقطة البداية
        self.find_start_paths()
        
        # إخفاء رسالة الخطأ
        self.error_label.config(text="")
        self.same_path_indicator.config(text="")
        
        # تحديث حالة اللعبة
        self.status_label.config(text="Choose a path from START!", fg=self.colors['text'])
        
        self.update_info()
        self.update_score()
        self.draw_maze()
    
    def find_start_paths(self):
        """إيجاد الطرق المتاحة من نقطة البداية"""
        self.start_paths = []
        row, col = self.start_pos
        
        # فحص الخلايا المجاورة للبداية
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            
            if (0 <= nr < len(self.maze) and 0 <= nc < len(self.maze[0]) and
                self.maze[nr][nc] == " "):
                self.start_paths.append((nr, nc))
        
        # إذا لم نجد طريقين، ننشئ طريقاً إضافياً
        if len(self.start_paths) < 2:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                
                if (0 <= nr < len(self.maze) and 0 <= nc < len(self.maze[0]) and
                    self.maze[nr][nc] == "#" and (nr, nc) not in self.start_paths):
                    
                    # تحويل الجدار إلى طريق
                    self.maze[nr][nc] = " "
                    self.start_paths.append((nr, nc))
                    
                    if len(self.start_paths) >= 2:
                        break
    
    def find_start(self, maze, start):
        """إيجاد نقطة البداية أو النهاية"""
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                if value == start:
                    return (i, j)
        return None
    
    def find_neighbors(self, row, col):
        """إيجاد الجيران المتاحين"""
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row + 1 < len(self.maze):
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col + 1 < len(self.maze[0]):
            neighbors.append((row, col + 1))
        return neighbors
    
    def is_valid_move(self, pos):
        """التحقق من صحة الحركة"""
        row, col = pos
        if self.maze[row][col] == "#":
            return False
        return True
    
    def find_ai_path_to_end(self):
        """إيجاد المسار الكامل للـ AI حتى النهاية باستخدام BFS"""
        q = queue.Queue()
        q.put((tuple(self.ai_pos), [tuple(self.ai_pos)]))
        visited = {tuple(self.ai_pos)}
        
        while not q.empty():
            current_pos, path = q.get()
            
            if current_pos == self.end_pos:
                return path[1:]  # إرجاع المسار بدون الموضع الحالي
            
            neighbors = self.find_neighbors(current_pos[0], current_pos[1])
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                
                r, c = neighbor
                if self.maze[r][c] == "#":
                    continue
                
                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)
        
        return []  # إذا لم يجد مساراً
    
    def move_player(self, dr, dc):
        """تحريك اللاعب"""
        if self.game_over or self.player_lost:
            return
        
        new_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
        
        if self.is_valid_move(new_pos):
            # حفظ الموضع السابق
            self.previous_player_pos = tuple(self.player_pos)
            
            # حركة صحيحة
            self.player_path.append(tuple(self.player_pos))
            self.player_pos = list(new_pos)
            self.player_visited.add(tuple(new_pos))
            self.player_stuck = False
            
            # التحقق من الخلايا المشتركة مع AI
            self.check_shared_cells()
            
            # إخفاء رسالة الخطأ
            self.error_label.config(text="")
            
            # تحديث حالة اللعبة
            if tuple(self.player_pos) != self.start_pos:
                self.status_label.config(text="Navigating the maze...", fg=self.colors['text'])
            
            # التحقق من فوز اللاعب
            if tuple(self.player_pos) == self.end_pos:
                self.game_over = True
                self.winner = "player"
                self.player_wins += 1
                self.show_winner()
            else:
                # تحريك AI خطوة واحدة فقط
                self.move_ai_one_step()
            
            self.update_info()
            self.draw_maze()
        else:
            # حركة غير صحيحة (اصطدام بجدار) - اللاعب يخسر مباشرة
            self.player_lost = True
            self.show_wall_hit_message()
            
            # AI يكمل طريقه حتى النهاية
            self.start_ai_to_end()
    
    def check_shared_cells(self):
        """التحقق من الخلايا المشتركة بين اللاعب وAI"""
        # تحقق من كل خلية في مسار اللاعب (بما في ذلك الموقع الحالي)
        for player_cell in self.player_path + [tuple(self.player_pos)]:
            # إذا كانت هذه الخلية في مسار AI (بما في ذلك موقعه الحالي)
            if player_cell in self.ai_path or player_cell == tuple(self.ai_pos):
                self.same_path_cells.add(player_cell)
        
        # تحديث مؤشر الخلايا المشتركة
        if len(self.same_path_cells) > 0:
            self.same_path_indicator.config(
                text=f"⚠️ You're on AI's path! ({len(self.same_path_cells)} cells shared)",
                fg=self.colors['same_path']
            )
        else:
            self.same_path_indicator.config(text="")
    
    def show_wall_hit_message(self):
        """عرض رسالة عند الاصطدام بجدار"""
        message = "❌ You hit a wall! You lost! AI continues to the end..."
        self.error_label.config(text=message)
        self.same_path_indicator.config(text="")  # إخفاء مؤشر الخلايا المشتركة
        
        # جعل النافذة تهتز قليلاً للإشارة للخطأ
        self.root.after(100, lambda: self.shake_window())
        
        # تحديث الشاشة
        self.root.update()
    
    def shake_window(self):
        """جعل النافذة تهتز عند الخطأ"""
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        
        for i in range(0, 3):
            if i % 2 == 0:
                self.root.geometry(f"+{x+5}+{y}")
            else:
                self.root.geometry(f"+{x-5}+{y}")
            self.root.update()
            self.root.after(50)
        
        self.root.geometry(f"+{x}+{y}")
    
    def start_ai_to_end(self):
        """بدء حركة AI التلقائية حتى النهاية"""
        if self.game_over or self.ai_auto_moving:
            return
        
        self.ai_auto_moving = True
        self.ai_full_path = self.find_ai_path_to_end()
        
        if not self.ai_full_path:
            # إذا لم يجد AI مساراً، نهاية الجولة
            self.game_over = True
            self.winner = "player"  # اللاعب يفوز لأن AI عالق
            self.player_wins += 1
            self.show_winner()
            return
        
        # بدء الحركة التلقائية
        self.move_ai_along_path()
    
    def move_ai_along_path(self):
        """تحريك AI على طول المسار المحدد"""
        if self.game_over or not self.ai_auto_moving or not self.ai_full_path:
            return
        
        # أخذ الخطوة التالية من المسار
        next_pos = self.ai_full_path.pop(0)
        
        # تحريك AI للخطوة التالية
        self.ai_path.append(tuple(self.ai_pos))
        self.ai_pos = list(next_pos)
        self.ai_visited.add(next_pos)
        
        # التحقق من الخلايا المشتركة
        self.check_shared_cells()
        
        # تحديث الشاشة
        self.update_info()
        self.draw_maze()
        
        # التحقق إذا وصل AI للنهاية
        if tuple(self.ai_pos) == self.end_pos:
            self.game_over = True
            self.winner = "ai"
            self.ai_wins += 1
            self.show_winner()
            return
        
        # الاستمرار في الحركة بعد تأخير
        if self.ai_full_path:  # إذا كان لا يزال هناك مسار
            self.root.after(300, self.move_ai_along_path)  # 300 مللي ثانية بين الخطوات
        else:
            # إذا انتهى المسار ولم يصل للنهاية (يجب ألا يحدث هذا)
            self.ai_auto_moving = False
    
    def move_ai_one_step(self):
        """تحريك الذكاء الاصطناعي خطوة واحدة (عندما يتحرك اللاعب)"""
        if self.game_over or self.ai_auto_moving or self.player_lost:
            return
        
        # إيجاد الخطوة التالية للـ AI
        ai_path = self.find_ai_path_to_end()
        if ai_path:
            next_pos = ai_path[0]  # الخطوة الأولى في المسار
            self.ai_path.append(tuple(self.ai_pos))
            self.ai_pos = list(next_pos)
            self.ai_visited.add(next_pos)
            
            # التحقق من الخلايا المشتركة
            self.check_shared_cells()
            
            # التحقق من فوز AI
            if tuple(self.ai_pos) == self.end_pos:
                self.game_over = True
                self.winner = "ai"
                self.ai_wins += 1
                self.show_winner()
    
    def show_winner(self):
        """عرض الفائز"""
        # إيقاف أي حركة مستمرة لـ AI
        self.game_over = True
        self.ai_auto_moving = False
        
        # تحديث مؤشر الخلايا المشتركة
        if self.winner == "player":
            if len(self.same_path_cells) > 0:
                self.same_path_indicator.config(
                    text=f"🎉 You won! Shared {len(self.same_path_cells)} cells with AI",
                    fg=self.colors['same_path']
                )
            else:
                self.same_path_indicator.config(text="")
            
            title = "Congratulations! 🎉"
            message = f"YOU WON Round {self.current_round}!\n\nYou: {len(self.player_path)} steps\nAI: {len(self.ai_path)} steps"
            if len(self.same_path_cells) > 0:
                message += f"\nShared path cells: {len(self.same_path_cells)}"
            message += "\n\nPlay next round?"
            self.status_label.config(text="YOU WON!", fg='#059669')
            # إيقاف أي رسائل خطأ
            self.error_label.config(text="")
        else:
            if self.player_lost:
                title = "Round Over - You Hit a Wall!"
                message = f"You lost by hitting a wall!\nAI won Round {self.current_round}!\n\nYou: {len(self.player_path)} steps\nAI: {len(self.ai_path)} steps"
                if len(self.same_path_cells) > 0:
                    message += f"\nShared path cells: {len(self.same_path_cells)}"
                message += "\n\nTry next round?"
                self.status_label.config(text="You Lost - Hit Wall!", fg='#DC2626')
            else:
                title = "Round Over"
                message = f"AI Won Round {self.current_round}!\n\nYou: {len(self.player_path)} steps\nAI: {len(self.ai_path)} steps"
                if len(self.same_path_cells) > 0:
                    message += f"\nShared path cells: {len(self.same_path_cells)}"
                message += "\n\nTry next round?"
                self.status_label.config(text="AI Won", fg='#DC2626')
            
            # إيقاف أي رسائل خطأ
            self.error_label.config(text="AI reached the end!")
        
        self.current_round += 1
        self.update_score()
        
        self.root.after(1000, lambda: self.ask_next_round(title, message))
    
    def ask_next_round(self, title, message):
        """سؤال اللاعب إذا أراد دور جديد"""
        result = messagebox.askyesno(title, message)
        if result:
            self.generate_new_maze()
        else:
            self.show_final_score()
    
    def show_final_score(self):
        """عرض النتيجة النهائية"""
        if self.player_wins > self.ai_wins:
            msg = f"🏆 YOU ARE THE CHAMPION! 🏆\n\nFinal Score:\nYou: {self.player_wins}\nAI: {self.ai_wins}"
        elif self.ai_wins > self.player_wins:
            msg = f"AI Wins the Game!\n\nFinal Score:\nYou: {self.player_wins}\nAI: {self.ai_wins}"
        else:
            msg = f"It's a TIE!\n\nFinal Score:\nYou: {self.player_wins}\nAI: {self.ai_wins}"
        
        messagebox.showinfo("Game Over", msg)
    
    def update_info(self):
        """تحديث معلومات اللعبة"""
        info_text = f"Steps: You {len(self.player_path)} | AI {len(self.ai_path)}"
        
        # إضافة معلومات عن الخلايا المشتركة
        if len(self.same_path_cells) > 0:
            info_text += f" | Shared: {len(self.same_path_cells)}"
        
        if self.player_lost:
            info_text += " | YOU LOST - AI finishing..."
        elif self.ai_auto_moving:
            info_text += " | AI finishing..."
        
        # إضافة معلومات عن الطرق المتاحة
        if len(self.player_path) == 0 and not self.game_over:
            info_text += f" | Choose from {len(self.start_paths)} paths"
        
        self.info_label.config(text=info_text)
        self.round_label.config(text=f"Round: {self.current_round}")
    
    def update_score(self):
        """تحديث النتيجة الإجمالية"""
        score_text = f"Score - You: {self.player_wins}  |  AI: {self.ai_wins}"
        self.score_label.config(text=score_text)
    
    def draw_maze(self):
        """رسم المتاهة"""
        self.canvas.delete('all')
        
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                x = j * CELL_SIZE + PADDING
                y = i * CELL_SIZE + PADDING
                
                # رسم الخلية
                if value == "#":
                    # جدران زرقاء داكنة مع خطوط بيضاء واضحة
                    self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                                fill=self.colors['wall'], outline='#1E3A8A', width=2)
                    
                    # إضافة خطوط بيضاء واضحة على الجدران (نمط شبكي)
                    # خطوط أفقية
                    self.canvas.create_line(x+5, y+CELL_SIZE//3, x+CELL_SIZE-5, y+CELL_SIZE//3,
                                          fill=self.colors['wall_lines'], width=2)
                    self.canvas.create_line(x+5, y+2*CELL_SIZE//3, x+CELL_SIZE-5, y+2*CELL_SIZE//3,
                                          fill=self.colors['wall_lines'], width=2)
                    
                    # خطوط عمودية
                    self.canvas.create_line(x+CELL_SIZE//3, y+5, x+CELL_SIZE//3, y+CELL_SIZE-5,
                                          fill=self.colors['wall_lines'], width=2)
                    self.canvas.create_line(x+2*CELL_SIZE//3, y+5, x+2*CELL_SIZE//3, y+CELL_SIZE-5,
                                          fill=self.colors['wall_lines'], width=2)
                    
                    # نقاط في الزوايا
                    self.canvas.create_oval(x+3, y+3, x+8, y+8, fill=self.colors['wall_lines'], outline='')
                    self.canvas.create_oval(x+CELL_SIZE-8, y+3, x+CELL_SIZE-3, y+8, fill=self.colors['wall_lines'], outline='')
                    self.canvas.create_oval(x+3, y+CELL_SIZE-8, x+8, y+CELL_SIZE-3, fill=self.colors['wall_lines'], outline='')
                    self.canvas.create_oval(x+CELL_SIZE-8, y+CELL_SIZE-8, x+CELL_SIZE-3, y+CELL_SIZE-3, fill=self.colors['wall_lines'], outline='')
                    
                elif value == "X":
                    # نقطة النهاية بلون أحمر مرجاني (لون مختلف)
                    self.canvas.create_rectangle(x + 3, y + 3, 
                                                x + CELL_SIZE - 3, y + CELL_SIZE - 3,
                                                fill=self.colors['end'], outline='#B91C1C', width=3)
                    # إضافة تأثير ثلاثي الأبعاد
                    self.canvas.create_rectangle(x + 1, y + 1, 
                                                x + CELL_SIZE - 1, y + CELL_SIZE - 1,
                                                outline='#FF8A8A', width=1)
                    self.canvas.create_text(x + CELL_SIZE//2, y + CELL_SIZE//2,
                                           text="END", font=('Arial', 9, 'bold'), fill='white')
                    
                elif value == "O":
                    # نقطة البداية بلون أزرق فاتح
                    self.canvas.create_oval(x + 5, y + 5,
                                           x + CELL_SIZE - 5, y + CELL_SIZE - 5,
                                           fill=self.colors['start'], outline='#1E3A8A', width=3)
                    self.canvas.create_text(x + CELL_SIZE//2, y + CELL_SIZE//2,
                                           text="START", font=('Arial', 8, 'bold'), fill='white')
                
                # تلوين الطرق من نقطة البداية بشكل مميز
                if (i, j) in self.start_paths and (i, j) != tuple(self.player_pos):
                    self.canvas.create_rectangle(x + 2, y + 2, 
                                                x + CELL_SIZE - 2, y + CELL_SIZE - 2,
                                                fill=self.colors['start_paths'], outline='#3B82F6', width=1)
                    self.canvas.create_text(x + CELL_SIZE//2, y + CELL_SIZE//2,
                                           text="?", font=('Arial', 10, 'bold'), fill='#1E3A8A')
                
                # رسم المسارات
                if (i, j) in self.player_path:
                    # مسار اللاعب بأزرق فاتح
                    self.canvas.create_oval(x + CELL_SIZE//2 - 5, y + CELL_SIZE//2 - 5,
                                          x + CELL_SIZE//2 + 5, y + CELL_SIZE//2 + 5,
                                          fill=self.colors['player_trail'], outline='#2563EB', width=2)
                
                if (i, j) in self.ai_path:
                    # مسار الذكاء الاصطناعي بلون أحمر فاتح
                    self.canvas.create_oval(x + CELL_SIZE//2 - 5, y + CELL_SIZE//2 - 5,
                                          x + CELL_SIZE//2 + 5, y + CELL_SIZE//2 + 5,
                                          fill=self.colors['ai_trail'], outline='#EF4444', width=2)
                
                # تلوين الخلايا المشتركة بلون أصفر
                if (i, j) in self.same_path_cells:
                    # دائرة صفراء في وسط الخلية المشتركة
                    self.canvas.create_oval(x + CELL_SIZE//2 - 8, y + CELL_SIZE//2 - 8,
                                          x + CELL_SIZE//2 + 8, y + CELL_SIZE//2 + 8,
                                          fill=self.colors['same_path'], outline='#D97706', width=2)
                    # إضافة علامة ✕ داخل الدائرة
                    self.canvas.create_text(x + CELL_SIZE//2, y + CELL_SIZE//2,
                                          text="✕", font=('Arial', 12, 'bold'), fill='#92400E')
        
        # رسم اللاعب
        px = self.player_pos[1] * CELL_SIZE + PADDING + CELL_SIZE // 2
        py = self.player_pos[0] * CELL_SIZE + PADDING + CELL_SIZE // 2
        
        # تغيير لون اللاعب إذا خسر
        if self.player_lost:
            player_color = self.colors['player_lost']  # رمادي
            player_outline = '#64748B'
            player_text = "☠️"
        else:
            player_color = self.colors['player']
            player_outline = '#1E3A8A'
            player_text = "P"
        
        self.canvas.create_oval(px - 12, py - 12, px + 12, py + 12,
                               fill=player_color, outline=player_outline, width=3)
        self.canvas.create_text(px, py, text=player_text, font=('Arial', 12, 'bold'), fill='white')
        
        # رسم الذكاء الاصطناعي
        ax = self.ai_pos[1] * CELL_SIZE + PADDING + CELL_SIZE // 2
        ay = self.ai_pos[0] * CELL_SIZE + PADDING + CELL_SIZE // 2
        ai_color = self.colors['ai']
        if self.ai_auto_moving:
            ai_color = '#10B981'  # أخضر عندما يتحرك تلقائياً
        self.canvas.create_oval(ax - 12, ay - 12, ax + 12, ay + 12,
                               fill=ai_color, outline='#B91C1C', width=3)
        self.canvas.create_text(ax, ay, text="AI", font=('Arial', 10, 'bold'), fill='white')
        
        # إضافة حدود حول المتاهة
        self.canvas.create_rectangle(PADDING, PADDING,
                                    MAZE_WIDTH * CELL_SIZE + PADDING,
                                    MAZE_HEIGHT * CELL_SIZE + PADDING,
                                    outline='#1E3A8A', width=4)
        
        # إضافة مؤشر إذا كان AI يتحرك تلقائياً
        if self.ai_auto_moving:
            if self.player_lost:
                message = "❌ You hit a wall! AI finishing to the end..."
                color = '#DC2626'
            else:
                message = "🚀 AI is moving automatically to the end..."
                color = '#059669'
            
            self.canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2 + PADDING, 
                                   MAZE_HEIGHT * CELL_SIZE + PADDING + 15,
                                   text=message,
                                   font=('Arial', 9, 'bold'), fill=color)
        
        # إضافة مؤشر لطرق البداية إذا كان اللاعب لم يتحرك بعد
        if len(self.player_path) == 0 and not self.game_over:
            self.canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2 + PADDING, 
                                   MAZE_HEIGHT * CELL_SIZE + PADDING + 15,
                                   text=f"🎯 Choose from {len(self.start_paths)} paths from START!",
                                   font=('Arial', 9, 'bold'), fill='#1E3A8A')
        
        # إضافة مؤشر للخلايا المشتركة
        if len(self.same_path_cells) > 0:
            self.canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2 + PADDING, 
                                   MAZE_HEIGHT * CELL_SIZE + PADDING + 30,
                                   text=f"⚠️ Yellow cells: Same path as AI ({len(self.same_path_cells)} cells)",
                                   font=('Arial', 8, 'bold'), fill=self.colors['same_path'])

def main():
    root = tk.Tk()
    root.configure(bg='#F0F9FF')  # خلفية زرقاء فاتحة جداً
    root.resizable(False, False)
    
    # إضافة عنوان جميل
    title_label = tk.Label(root, text="🌀 Dual Path Maze Challenge 🌀", 
                          font=('Arial', 16, 'bold'), 
                          fg='#1E3A8A', bg='#F0F9FF')
    title_label.pack(pady=5)
    
    # إضافة تعليمات
    instructions = tk.Label(root, 
                          font=('Arial', 10), 
                          fg='#1E40AF', bg='#F0F9FF')
    instructions.pack(pady=2)
    
    game = MazeGame(root)
    
    # إضافة تذييل
    footer_label = tk.Label(root, 
                           text="START has 2+ paths → Choose one → Avoid walls → Reach END before AI",
                           font=('Arial', 9), fg='#1E3A8A', bg='#F0F9FF')
    footer_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()