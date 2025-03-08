import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
from PIL import Image

def count_png_files(input_dir):
    try:
        return sum(1 for filename in os.listdir(input_dir) if filename.endswith('.png'))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to count PNG files: {e}")
        return 0

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
    return image.crop(bbox) if bbox else image

def save_frames(cropped_frames, save_location, filename):
    file_folder = sanitize_filename(os.path.splitext(filename)[0])
    file_save_location = os.path.join(save_location, file_folder)
    os.makedirs(file_save_location, exist_ok=True)

    for i, frame in enumerate(cropped_frames):
        frame_filename = f'frame_{i}.png'
        try:
            frame.save(os.path.join(file_save_location, frame_filename))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save frame {frame_filename}: {e}")

def split_icons(input_dir, save_location, selected_frames, progress_var, root):
    if not selected_frames:
        messagebox.showwarning("Warning", "No frames selected for extraction.")
        return

    total_files = count_png_files(input_dir)
    if total_files == 0:
        messagebox.showwarning("Warning", "No PNG files found in the selected directory.")
        return

    progress_var.set(0)
    progress_bar["maximum"] = total_files

    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            full_path = os.path.join(input_dir, filename)
            try:
                spritesheet = Image.open(full_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image {filename}: {e}")
                continue

            width, height = spritesheet.size
            frames = [spritesheet.crop((i * 150, j * 150, (i + 1) * 150, (j + 1) * 150))
                      for i in range(width // 150) for j in range(height // 150)]

            try:
                cropped_frames = [crop_transparency(frames[i]) for i in selected_frames]
            except IndexError as e:
                messagebox.showerror("Error", f"Frame index out of range: {e}")
                continue

            save_frames(cropped_frames, save_location, filename)

            progress_var.set(progress_var.get() + 100 / total_files)
            root.update_idletasks()

    messagebox.showinfo("Information", "Finished processing all files.")

def get_selected_frames():
    input_frames = simpledialog.askstring("Input", "Enter the frame numbers to extract (comma-separated):")
    if input_frames:
        try:
            return [int(x.strip()) - 1 for x in input_frames.split(',') if x.strip().isdigit()]
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid frame numbers.")
    return []

root = tk.Tk()
root.title("FNF Icon Splitter PLUS")
root.geometry("700x500")
root.configure(bg="#1E1E1E")

title_label = tk.Label(root, text="FNF Icon Splitter PLUS", font=("Helvetica", 24, "bold"), bg="#1E1E1E", fg="#FFDD57")
title_label.pack(pady=20)

input_frame = tk.Frame(root, bg="#1E1E1E")
input_frame.pack(pady=10)

input_dir = tk.StringVar()
input_dir_label = tk.Label(input_frame, text="No input directory selected", bg="#1E1E1E", fg="white")
input_dir_label.pack(side='left', padx=5)

input_button = tk.Button(input_frame, text="Select Icons Directory", command=lambda: select_directory(input_dir, input_dir_label), bg="#4CAF50", fg="white", font=("Helvetica", 12))
input_button.pack(side='left', padx=5)

output_frame = tk.Frame(root, bg="#1E1E1E")
output_frame.pack(pady=10)

output_dir = tk.StringVar()
output_dir_label = tk.Label(output_frame, text="No output directory selected", bg="#1E1E1E", fg="white")
output_dir_label.pack(side='left', padx=5)

output_button = tk.Button(output_frame, text="Select Save Directory", command=lambda: select_directory(output_dir, output_dir_label), bg="#4CAF50", fg="white", font=("Helvetica", 12))
output_button.pack(side='left', padx=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=500, variable=progress_var)
progress_bar.pack(pady=20)

process_button = tk.Button(root, text="Start Processing", command=lambda: split_icons(input_dir.get(), output_dir.get(), get_selected_frames(), progress_var, root), bg="#FF5722", fg="white", font=("Helvetica", 14))
process_button.pack(pady=20)

author_label = tk.Label(root, text="Tool improved by sirthegamercoder\nTool written by AutisticLulu", bg="#1E1E1E", fg="white")
author_label.pack(side='bottom', pady=10)

root.mainloop()
