from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class GifGenerator:
    def __init__(self, images, output_file, duration=500):
        """
        Initializes the GifGenerator with images, output file name, and duration between frames.

        :param images: List of paths to image files.
        :param output_file: The name of the output GIF file.
        :param duration: Duration between frames in milliseconds.
        """
        self.images = images
        self.output_file = output_file
        self.duration = duration

    def generate_gif(self):
        """
        Generates a GIF from the images provided.
        """
        if not self.images:
            raise ValueError("The images list is empty.")

        # Open the image files
        frames = [Image.open(image) for image in self.images]

        # Convert to RGB if necessary
        frames = [frame.convert('RGB') if frame.mode != 'RGB' else frame for frame in frames]

        # Save as GIF
        frames[0].save(
            self.output_file,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=self.duration,
            loop=0
        )
        print(f"GIF saved as {self.output_file}")

# GUI to select files and output directory
def open_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    def select_images():
        files = filedialog.askopenfilenames(title="Select Images for GIF", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if files:
            current_files = images_entry.get()
            if current_files:
                updated_files = current_files + ";" + ";".join(files)
            else:
                updated_files = ";".join(files)
            images_entry.delete(0, tk.END)
            images_entry.insert(0, updated_files)

    def select_output_directory():
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            output_dir_entry.delete(0, tk.END)
            output_dir_entry.insert(0, directory)

    def generate_gif():
        images = images_entry.get().split(";")
        output_dir = output_dir_entry.get()
        filename = filename_entry.get()

        if not images or not output_dir or not filename:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        output_file = os.path.join(output_dir, f"{filename}.gif")
        gif_generator = GifGenerator(images, output_file, duration=700)
        try:
            gif_generator.generate_gif()
            messagebox.showinfo("Success", f"GIF saved as {output_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create GUI window
    gui = tk.Tk()
    gui.title("GIF Generator")

    # Images selection
    tk.Label(gui, text="Select Images:").grid(row=0, column=0, padx=10, pady=5)
    images_entry = tk.Entry(gui, width=50)
    images_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(gui, text="Browse", command=select_images).grid(row=0, column=2, padx=10, pady=5)

    # Output directory selection
    tk.Label(gui, text="Select Output Directory:").grid(row=1, column=0, padx=10, pady=5)
    output_dir_entry = tk.Entry(gui, width=50)
    output_dir_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(gui, text="Browse", command=select_output_directory).grid(row=1, column=2, padx=10, pady=5)

    # Filename entry
    tk.Label(gui, text="Enter Output Filename (without extension):").grid(row=2, column=0, padx=10, pady=5)
    filename_entry = tk.Entry(gui, width=50)
    filename_entry.grid(row=2, column=1, padx=10, pady=5)

    # Generate button
    tk.Button(gui, text="Generate GIF", command=generate_gif).grid(row=3, column=1, pady=20)

    gui.mainloop()

# Usage example
if __name__ == "__main__":
    open_gui()