import tkinter as tk
from tkinter import ttk
import json
import os
import sys
from datetime import datetime, timedelta
import threading
import time

class Stopwatch:
    def __init__(self, label="Stopwatch", elapsed_time=0, is_running=False):
        self.label = label
        self.elapsed_time = elapsed_time  # in seconds
        self.is_running = is_running
        self.start_time = None
        self.last_update = datetime.now()
        
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now() - timedelta(seconds=self.elapsed_time)
            
    def stop(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time = (datetime.now() - self.start_time).total_seconds()
            
    def get_current_time(self):
        if self.is_running:
            return (datetime.now() - self.start_time).total_seconds()
        return self.elapsed_time
    
    def to_dict(self):
        return {
            'label': str(self.label) if self.label else 'Stopwatch',
            'elapsed_time': self.get_current_time(),
            'is_running': self.is_running
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            label=data.get('label', 'Stopwatch'),
            elapsed_time=data.get('elapsed_time', 0),
            is_running=False  # Always start paused when loaded
        )

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set minimal window style
        self.root.configure(bg='#f0f0f0')
        
        self.stopwatches = []
        self.stopwatch_frames = []
        
        # Storage file - save in appropriate location
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # Check if we're in Program Files (installed version)
            exe_dir = os.path.dirname(sys.executable)
            # Check both Program Files and Program Files (x86)
            program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
            program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
            exe_dir_normalized = os.path.normpath(exe_dir).lower()
            program_files_normalized = os.path.normpath(program_files).lower()
            program_files_x86_normalized = os.path.normpath(program_files_x86).lower()
            
            if (exe_dir_normalized.startswith(program_files_normalized) or 
                exe_dir_normalized.startswith(program_files_x86_normalized)):
                # Installed version - use AppData for user-specific data
                appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
                app_folder = os.path.join(appdata, 'Time Tracker')
                os.makedirs(app_folder, exist_ok=True)
                self.storage_file = os.path.join(app_folder, "stopwatches.json")
            else:
                # Portable version - use same directory as exe
                self.storage_file = os.path.join(exe_dir, "stopwatches.json")
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
            self.storage_file = os.path.join(base_path, "stopwatches.json")
        
        # Load saved stopwatches
        self.load_stopwatches()
        
        # Create UI
        self.create_ui()
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_times, daemon=True)
        self.update_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_ui(self):
        # Header with add button
        header_frame = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        header_frame.pack(fill=tk.X, padx=10)
        
        title_label = tk.Label(header_frame, text="Time Tracker", 
                              font=('Segoe UI', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(side=tk.LEFT)
        
        add_button = tk.Button(header_frame, text="+", font=('Segoe UI', 20, 'bold'),
                              command=self.add_stopwatch, bg='#4CAF50', fg='white',
                              width=3, relief=tk.FLAT, cursor='hand2')
        add_button.pack(side=tk.RIGHT)
        
        # Scrollable frame for stopwatches
        self.canvas = tk.Canvas(self.root, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        def update_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.scrollable_frame.bind("<Configure>", update_scroll_region)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        # Rebuild stopwatch UI
        self.rebuild_ui()
        
    def rebuild_ui(self):
        # Clear existing frames
        for frame in self.stopwatch_frames:
            frame.destroy()
        self.stopwatch_frames.clear()
        
        # Create frames for each stopwatch
        for i, stopwatch in enumerate(self.stopwatches):
            self.create_stopwatch_frame(i, stopwatch)
        
        # Update scroll region after rebuilding
        if hasattr(self, 'canvas'):
            self.root.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            
    def create_stopwatch_frame(self, index, stopwatch):
        frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, 
                        borderwidth=1, pady=5, padx=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        self.stopwatch_frames.append(frame)
        
        # Top row: Label and remove button
        top_frame = tk.Frame(frame, bg='white')
        top_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Editable label - store reference to entry widget on stopwatch
        label_entry = tk.Entry(top_frame, font=('Segoe UI', 11), 
                              bg='white', relief=tk.FLAT, borderwidth=0)
        label_entry.insert(0, stopwatch.label)
        label_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        stopwatch.label_entry = label_entry  # Store reference for saving
        
        def update_label(event=None):
            stopwatch.label = label_entry.get()
            self.save_stopwatches()
        
        label_entry.bind('<FocusOut>', update_label)
        label_entry.bind('<Return>', update_label)
        
        # Remove button (X) - use default parameter to capture index correctly
        remove_btn = tk.Button(top_frame, text="×", font=('Segoe UI', 16, 'bold'),
                              command=lambda idx=index: self.remove_stopwatch(idx),
                              bg='white', fg='#ff4444', relief=tk.FLAT,
                              cursor='hand2', width=2)
        remove_btn.pack(side=tk.RIGHT)
        
        # Time display
        time_label = tk.Label(frame, text="00:00:00", font=('Segoe UI', 24, 'bold'),
                             bg='white', fg='#333')
        time_label.pack(pady=10)
        stopwatch.time_label = time_label
        
        # Buttons frame
        buttons_frame = tk.Frame(frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Start button - use default parameter to capture index correctly
        start_btn = tk.Button(buttons_frame, text="Start", 
                             command=lambda idx=index: self.toggle_start(idx),
                             bg='#4CAF50', fg='white', font=('Segoe UI', 10, 'bold'),
                             relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        start_btn.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        stopwatch.start_btn = start_btn
        
        # Stop button - use default parameter to capture index correctly
        stop_btn = tk.Button(buttons_frame, text="Stop", 
                            command=lambda idx=index: self.stop_stopwatch(idx),
                            bg='#f44336', fg='white', font=('Segoe UI', 10, 'bold'),
                            relief=tk.FLAT, padx=20, pady=5, cursor='hand2')
        stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        stopwatch.stop_btn = stop_btn
        
        # Update button states
        self.update_button_states(index)
        
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def toggle_start(self, index):
        stopwatch = self.stopwatches[index]
        if stopwatch.is_running:
            stopwatch.stop()
        else:
            stopwatch.start()
        self.update_button_states(index)
        self.save_stopwatches()
        
    def stop_stopwatch(self, index):
        stopwatch = self.stopwatches[index]
        stopwatch.stop()
        self.update_button_states(index)
        self.save_stopwatches()
        
    def update_button_states(self, index):
        stopwatch = self.stopwatches[index]
        if stopwatch.is_running:
            stopwatch.start_btn.config(text="Pause", bg='#FF9800')
        else:
            stopwatch.start_btn.config(text="Start", bg='#4CAF50')
            
    def update_times(self):
        while self.running:
            for stopwatch in self.stopwatches:
                if hasattr(stopwatch, 'time_label'):
                    current_time = stopwatch.get_current_time()
                    stopwatch.time_label.config(text=self.format_time(current_time))
            time.sleep(0.1)
            
    def add_stopwatch(self):
        new_stopwatch = Stopwatch(label=f"Stopwatch {len(self.stopwatches) + 1}")
        self.stopwatches.append(new_stopwatch)
        self.rebuild_ui()
        self.save_stopwatches()
        
    def remove_stopwatch(self, index):
        if 0 <= index < len(self.stopwatches):
            # Stop the stopwatch before removing
            self.stopwatches[index].stop()
            self.stopwatches.pop(index)
            self.rebuild_ui()
            self.save_stopwatches()
            
    def save_stopwatches(self):
        try:
            data = {
                'stopwatches': [sw.to_dict() for sw in self.stopwatches],
                'saved_at': datetime.now().isoformat()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving stopwatches: {e}")
            
    def load_stopwatches(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.stopwatches = [
                        Stopwatch.from_dict(sw_data) 
                        for sw_data in data.get('stopwatches', [])
                    ]
        except Exception as e:
            print(f"Error loading stopwatches: {e}")
            self.stopwatches = []
            
    def on_closing(self):
        # Update all labels from Entry widgets before saving
        for stopwatch in self.stopwatches:
            if hasattr(stopwatch, 'label_entry'):
                label_text = stopwatch.label_entry.get().strip()
                stopwatch.label = label_text if label_text else stopwatch.label
            if stopwatch.is_running:
                stopwatch.stop()
        self.save_stopwatches()
        self.running = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

