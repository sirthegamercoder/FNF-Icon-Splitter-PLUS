import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
from PIL import Image

def count_png_files(input_dir):
    return sum(1 for filename in os.listdir(input_dir) if filename.endswith('.png'))

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def select_directory(variable, label):
    directory = filedialog.askdirectory()
    if directory:
        variable.set(directory)
        label.config(text=directory)

def crop_transparency(image):
    image_alpha = image.convert("RGBA").split()[-1]
    bbox = image_alpha.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

def split_icons(input_dir, save_location, selected_frames, progress_var, root):
    progress_var.set(0)
    total_files = count_png_files(input_dir)
    progress_bar["maximum"] = total_files

    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            full_path = os.path.join(input_dir, filename)
            spritesheet = Image.open(full_path)

            width, height = spritesheet.size
            frames = []
            for i in range(width // 150):
                for j in range(height // 150):
                    left = i * 150
                    upper = j * 150
                    right = left + 150
                    lower = upper + 150
                    frame = spritesheet.crop((left, upper, right, lower))
                    frames.append(frame)

            cropped_frames = [crop_transparency(frames[i]) for i in selected_frames]

            file_folder = sanitize_filename(os.path.splitext(filename)[0])
            file_save_location = os.path.join(save_location, file_folder)
            os.makedirs(file_save_location, exist_ok=True)
            for i, frame in enumerate(cropped_frames):
                frame_filename = f'frame_{i}.png'
                frame.save(os.path.join(file_save_location, frame_filename))
                progress_var.set((i + 1) / len(cropped_frames) * 100)
                root.update_idletasks()

    messagebox.showinfo("Information", "Finished processing all files.")

def get_selected_frames():
    input_frames = simpledialog.askstring("Input", "Enter the frame numbers to extract (comma-separated):")
    if input_frames:
        return [int(x.strip()) for x in input_frames.split(',') if x.strip().isdigit()]
    return []

root = tk.Tk()
root.title("FNF Icon Splitter PLUS")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="FNF Icon Splitter PLUS", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

input_dir = tk.StringVar()
input_dir_label = tk.Label(input_frame, text="No input directory selected", bg="#f0f0f0")
input_dir_label.pack(side='left', padx=5)

input_button = tk.Button(input_frame, text="Select Icons Directory", command=lambda: select_directory(input_dir, input_dir_label))
input_button.pack(side='left', padx=5)

output_frame = tk.Frame(root, bg="#f0f0f0")
output_frame.pack(pady=10)

output_dir = tk.StringVar()
output_dir_label = tk.Label(output_frame, text="No output directory selected", bg="#f0f0f0")
output_dir_label.pack(side='left', padx=5)

output_button = tk.Button(output_frame, text="Select Save Directory", command=lambda: select_directory(output_dir, output_dir_label))
output_button.pack(side='left', padx=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=300, variable=progress_var)
progress_bar.pack(pady=20)

process_button = tk.Button(root, text="Start Processing", command=lambda: split_icons(input_dir.get(), output_dir.get(), get_selected_frames(), progress_var, root), bg="#4CAF50", fg="white")
process_button.pack(pady=10)

author_label = tk.Label(root, text="Tool improved by MTGC aka MTGM\nTool written by AutisticLulu", bg="#f0f0f0")
author_label.pack(side='bottom', pady=5)

root.mainloop()
