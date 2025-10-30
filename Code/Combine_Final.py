import os
import sys
import PIL
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# --Debugging--
# Silence macOS Tk warnings
os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Clear terminal function
def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')
    # Otherwise, assume it's a Unix-like system (Linux, macOS)
    else:
        _ = os.system('clear')

clear_terminal()

# Confirm PIL
print(PIL.__version__)

# --Application--
class ImageCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Combiner (macOS + Windows Compatible)")
        self.root.geometry("1000x700")

        # Store images + state
        self.folder1_images = []
        self.folder2_images = []
        self.current_top = 0
        self.current_bottom = 0
        self.current_combined = None
        self.display_mode = "single"  # single/grid

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Top frame for controls
        control_frame = Frame(self.root)
        control_frame.pack(side=TOP, fill=X, pady=5)

        Button(control_frame, text="Select Top Line Stimuli", command=self.load_folder1).pack(side=LEFT, padx=5)
        Button(control_frame, text="Select Bottom Line Stimuli", command=self.load_folder2).pack(side=LEFT, padx=5)
        Button(control_frame, text="Toggle View", command=self.toggle_view).pack(side=LEFT, padx=5)
        Button(control_frame, text="Save Combined", command=self.save_combined).pack(side=LEFT, padx=5)

        # Info label
        self.info_label = Label(self.root, text="", font=("Arial", 12), anchor="w", justify=LEFT)
        self.info_label.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        # Canvas for images
        self.canvas = Canvas(self.root, bg="#222")
        self.canvas.pack(fill=BOTH, expand=True)

        # Keyboard shortcuts
        self.root.bind("<Left>", lambda e: self.prev_top())
        self.root.bind("<Right>", lambda e: self.next_top())
        self.root.bind("<Up>", lambda e: self.prev_bottom())
        self.root.bind("<Down>", lambda e: self.next_bottom())
        self.root.bind("<Tab>", lambda e: self.toggle_view())
        self.root.bind("<Return>", lambda e: self.save_combined())

    # Folder + Image Loading
    def load_folder1(self):
        folder = filedialog.askdirectory(title="Select Folder 1")
        if folder:
            self.folder1_images = self.load_images_from_folder(folder)
            self.current_top = 0
            self.update_display()

    def load_folder2(self):
        folder = filedialog.askdirectory(title="Select Folder 2")
        if folder:
            self.folder2_images = self.load_images_from_folder(folder)
            self.current_bottom = 0
            self.update_display()

    def load_images_from_folder(self, folder):
        valid_exts = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid_exts)]
        files.sort()
        return files

    # Image Combination + Display
    def combine_images(self, img1_path, img2_path):
        try:
            img1 = Image.open(img1_path).convert("RGBA")
            img2 = Image.open(img2_path).convert("RGBA")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {e}")
            return None

        # Resize to same width
        width = min(img1.width, img2.width)
        img1 = img1.resize((width, int(img1.height * width / img1.width)))
        img2 = img2.resize((width, int(img2.height * width / img2.width)))

        combined_height = img1.height + img2.height
        combined = Image.new("RGBA", (width, combined_height))
        combined.paste(img1, (0, 0))
        combined.paste(img2, (0, img1.height))

        return combined.convert("RGB")

    def update_display(self):
        self.canvas.delete("all")

        if not self.folder1_images or not self.folder2_images:
            self.info_label.config(text="Please select both folders.")
            return

        if self.display_mode == "single":
            combined = self.combine_images(
                self.folder1_images[self.current_top],
                self.folder2_images[self.current_bottom],
            )
            if combined:
                self.show_image(combined)
                self.current_combined = combined
                self.info_label.config(
                    text=f"Single View — Top: {os.path.basename(self.folder1_images[self.current_top])} | "
                         f"Bottom: {os.path.basename(self.folder2_images[self.current_bottom])}"
                )
        else: self.show_grid()


    def show_image(self, image):
        # Scale image to fit canvas
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w < 10 or canvas_h < 10:
            self.root.after(200, lambda: self.show_image(image))
            return

        img_ratio = image.width / image.height
        canvas_ratio = canvas_w / canvas_h

        if img_ratio > canvas_ratio:
            new_w = canvas_w
            new_h = int(new_w / img_ratio)
        else:
            new_h = canvas_h
            new_w = int(new_h * img_ratio)

        resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)  # Keep reference
        self.canvas.create_image(canvas_w // 2, canvas_h // 2, image=self.tk_img, anchor="center")

    def show_grid(self):
        self.canvas.delete("all")
        cols = min(3, len(self.folder1_images))
        rows = min(3, len(self.folder2_images))
        cell_w = self.canvas.winfo_width() // cols
        cell_h = self.canvas.winfo_height() // rows

        if cell_w < 10 or cell_h < 10:
            self.root.after(200, self.show_grid)
            return

        for r in range(rows):
            for c in range(cols):
                top_idx = (self.current_top + c) % len(self.folder1_images)
                bottom_idx = (self.current_bottom + r) % len(self.folder2_images)
                combined = self.combine_images(
                    self.folder1_images[top_idx],
                    self.folder2_images[bottom_idx],
                )
                if combined:
                    thumb = combined.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(thumb)
                    self.canvas.create_image(c * cell_w, r * cell_h, image=img_tk, anchor="nw")
                    # Keep references to prevent GC
                    if not hasattr(self, "thumbs"):
                        self.thumbs = []
                    self.thumbs.append(img_tk)

        self.info_label.config(text=f"Grid View — Top Index {self.current_top}, Bottom Index {self.current_bottom}")

    # Navigation + Save
    def next_top(self):
        if self.folder1_images:
            self.current_top = (self.current_top + 1) % len(self.folder1_images)
            self.update_display()

    def prev_top(self):
        if self.folder1_images:
            self.current_top = (self.current_top - 1) % len(self.folder1_images)
            self.update_display()

    def next_bottom(self):
        if self.folder2_images:
            self.current_bottom = (self.current_bottom + 1) % len(self.folder2_images)
            self.update_display()

    def prev_bottom(self):
        if self.folder2_images:
            self.current_bottom = (self.current_bottom - 1) % len(self.folder2_images)
            self.update_display()

    def toggle_view(self):
        self.display_mode = "grid" if self.display_mode == "single" else "single"
        self.update_display()

    def save_combined(self):
        if self.current_combined:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if file_path:
                self.current_combined.save(file_path)
                messagebox.showinfo("Saved", f"Saved combined image to:\n{file_path}")


if __name__ == "__main__":
    root = Tk()
    app = ImageCombinerApp(root)
    root.mainloop()
