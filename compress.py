import os
import sys
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to get the user's Downloads folder
def get_downloads_folder():
    if os.name == 'nt':  # Windows
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # macOS and Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

# Function to get video duration
def get_video_duration(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f'Error occurred while probing video: {e.stderr.decode() if e.stderr else str(e)}', file=sys.stderr)
        return None

# Function to compress the video
def compress_video_to_target_size(input_file, output_file, target_size_mb, audio_bitrate='128k'):
    try:
        duration = get_video_duration(input_file)
        if duration is None:
            log_text.insert(tk.END, "Failed to retrieve video duration.\n")
            return

        target_size_bits = target_size_mb * 8 * 1024 * 1024
        target_bitrate = (target_size_bits - (audio_bitrate_to_bits(audio_bitrate) * duration)) / duration

        min_bitrate = 100000  # Minimum bitrate of 100 kbps
        if target_bitrate < min_bitrate:
            log_text.insert(tk.END, "Target bitrate too low, adjusting to minimum.\n")
            target_bitrate = min_bitrate

        while True:
            log_text.insert(tk.END, f'Trying video bitrate: {target_bitrate:.2f} bits/s\n')
            log_text.update_idletasks()  # Update the GUI

            # Ensure the output file path has a valid filename and extension
            if not output_file.lower().endswith('.mp4'):
                output_file += '.mp4'

            ffmpeg.input(input_file).output(output_file, video_bitrate=target_bitrate, audio_bitrate=audio_bitrate).run(overwrite_output=True)

            output_file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            if output_file_size_mb <= target_size_mb:
                log_text.insert(tk.END, f'Video compressed successfully! Output size: {output_file_size_mb:.2f} MB\n')
                break
            else:
                log_text.insert(tk.END, f'Output size {output_file_size_mb:.2f} MB exceeds target size. Reducing bitrate.\n')
                target_bitrate *= 0.9  # Reduce bitrate by 10% and retry

    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        log_text.insert(tk.END, f'Error during compression: {error_message}\n')

# Function to convert audio bitrate string to bits
def audio_bitrate_to_bits(audio_bitrate):
    if audio_bitrate.endswith('k'):
        return int(audio_bitrate[:-1]) * 1000
    elif audio_bitrate.endswith('M'):
        return int(audio_bitrate[:-1]) * 1000000
    else:
        return int(audio_bitrate)

# Function to open the file dialog and get input file
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if file_path:
        input_file_var.set(file_path)

# Function to save output file
def get_output_file_path(filename):
    # Get the user's Downloads folder
    downloads_folder = get_downloads_folder()
    # Combine the Downloads folder path with the provided filename
    output_file = os.path.join(downloads_folder, filename)
    return output_file

# Function to start the compression
def start_compression():
    input_file = input_file_var.get()
    output_filename = output_filename_var.get()
    target_size_mb = target_size_var.get()

    if not input_file or not output_filename:
        messagebox.showerror("Error", "Please select the input file and provide a valid output filename.")
        return

    if not target_size_mb.isdigit():
        messagebox.showerror("Error", "Please enter a valid target size in MB.")
        return

    # Convert target size to integer
    target_size_mb = int(target_size_mb)

    # Get the full path for the output file
    output_file = get_output_file_path(output_filename)

    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, f"Compressing {input_file} to {target_size_mb} MB...\n")
    log_text.insert(tk.END, f"Saving output to: {output_file}\n")
    compress_video_to_target_size(input_file, output_file, target_size_mb)

# Create the main application window
app = tk.Tk()
app.title("Video Compressor")
app.geometry("600x400")

# Input file selection
input_file_var = tk.StringVar()
output_filename_var = tk.StringVar()
target_size_var = tk.StringVar()

tk.Label(app, text="Input File:").pack(pady=5)
tk.Entry(app, textvariable=input_file_var, width=50).pack(pady=5)
tk.Button(app, text="Browse", command=select_input_file).pack(pady=5)

# Output filename (without path, just filename)
tk.Label(app, text="Output Filename (without path):").pack(pady=5)
tk.Entry(app, textvariable=output_filename_var, width=50).pack(pady=5)

# Target size input
tk.Label(app, text="Target Size (MB) ( Suggested (25):").pack(pady=5)
tk.Entry(app, textvariable=target_size_var, width=10).pack(pady=5)

# Compress button
tk.Button(app, text="Compress", command=start_compression, bg="green", fg="white").pack(pady=10)

# Log output
tk.Label(app, text="Log:").pack(pady=5)
log_text = tk.Text(app, height=10, width=70)
log_text.pack(pady=5)

# Start the Tkinter event loop
app.mainloop()
