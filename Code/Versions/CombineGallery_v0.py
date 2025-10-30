import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Combiner")
        self.root.geometry("1000x750")
        self.root.configure(bg="#222")

        # --- Data ---
        self.folder1 = []
        self.folder2 = []
        self.index1 = 0
        self.index2 = 0
        self.combined_images = []
        self.current_combined = None

        # --- UI Frames ---
        self.display_frame = Frame(root, bg="#222")
        self.display_frame.pack(expand=True, fill=BOTH)

        self.controls_frame = Frame(root, bg="#333")
        self.controls_frame.pack(fill=X)

        # --- Control Buttons ---
        Button(self.controls_frame, text="Load Top Folder", command=self.load_folder1).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Load Bottom Folder", command=self.load_folder2).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Combine", command=self.combine_current).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Save", command=self.save_all_combined).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Grid View", command=self.show_grid_view).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Single View", command=self.show_single_view).pack(side=LEFT, padx=5, pady=5)
        Button(self.controls_frame, text="Quit", command=root.quit).pack(side=RIGHT, padx=5, pady=5)

        # --- Info Label ---
        self.info_label = Label(root, text="No images loaded", fg="white", bg="#222", font=("Arial", 10))
        self.info_label.pack(pady=3)

        # --- Display Label ---
        self.image_label = Label(self.display_frame, bg="#222")
        self.image_label.pack(expand=True)

        self.stored_canvas = None
        self.scroll_y = None

        self.bind_keys()

    # ---------- Folder Loading ----------
    def load_folder1(self):
        folder = filedialog.askdirectory(title="Select Top Folder")
        if folder:
            self.folder1 = [os.path.join(folder, f) for f in os.listdir(folder)
                            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.index1 = 0

    def load_folder2(self):
        folder = filedialog.askdirectory(title="Select Bottom Folder")
        if folder:
            self.folder2 = [os.path.join(folder, f) for f in os.listdir(folder)
                            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.index2 = 0

    # ---------- Combine and Display ----------
    def combine_current(self):
        if not self.folder1 or not self.folder2:
            return

        img1 = Image.open(self.folder1[self.index1]).convert("RGBA")
        img2 = Image.open(self.folder2[self.index2]).convert("RGBA")

        # Resize to same width
        w = min(img1.width, img2.width)
        img1 = img1.resize((w, int(img1.height * w / img1.width)))
        img2 = img2.resize((w, int(img2.height * w / img2.width)))

        # Combine vertically
        combined = Image.new("RGBA", (w, img1.height + img2.height))
        combined.paste(img1, (0, 0))
        combined.paste(img2, (0, img1.height))

        self.current_combined = combined
        self.combined_images.append(combined)

        self.display_image(combined)
        self.update_info_label()

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img.resize((800, int(img.height * 800 / img.width))))
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    # ---------- Info Label ----------
    def update_info_label(self):
        if not self.folder1 or not self.folder2:
            self.info_label.config(text="No images loaded")
            return
        top_name = os.path.basename(self.folder1[self.index1])
        bottom_name = os.path.basename(self.folder2[self.index2])
        self.info_label.config(
            text=f"Top: ({self.index1+1}/{len(self.folder1)}) {top_name} | "
                 f"Bottom: ({self.index2+1}/{len(self.folder2)}) {bottom_name}"
        )

    # ---------- Save Current ----------
    def save_all_combined(self):
        if not self.current_combined:
            self.info_label.config(text="⚠️ No combined image to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Current Combined Image"
        )
        if save_path:
            self.current_combined.save(save_path)
            self.info_label.config(text=f"✅ Saved current combined image to: {save_path}")

    # ---------- Grid View ----------
    def show_grid_view(self):
        if not self.combined_images:
            return

        # Hide single image display
        self.image_label.pack_forget()

        # Create grid canvas if it doesn't exist
        if self.stored_canvas is None:
            self.stored_canvas = Canvas(self.display_frame, bg="#222")
            self.scroll_y = Scrollbar(self.display_frame, orient="vertical", command=self.stored_canvas.yview)
            self.stored_canvas.configure(yscrollcommand=self.scroll_y.set)
            self.stored_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            self.scroll_y.pack(side=RIGHT, fill=Y)

        # Clear previous content
        self.stored_canvas.delete("all")
        grid_frame = Frame(self.stored_canvas, bg="#222")
        self.stored_canvas.create_window((0, 0), window=grid_frame, anchor="nw")

        thumb_size = 200
        cols = 4
        for i, img in enumerate(self.combined_images):
            thumb = img.resize((thumb_size, int(img.height * thumb_size / img.width)))
            tk_thumb = ImageTk.PhotoImage(thumb)
            lbl = Label(grid_frame, image=tk_thumb, bg="#222")
            lbl.image = tk_thumb
            lbl.grid(row=i // cols, column=i % cols, padx=10, pady=10)

        grid_frame.update_idletasks()
        self.stored_canvas.config(scrollregion=self.stored_canvas.bbox("all"))

    def show_single_view(self):
        if self.stored_canvas:
            self.stored_canvas.destroy()
        self.scroll_y = None
        self.image_label.pack(expand=True)
        self.update_info_label()

    # ---------- Navigation ----------
    def next_both(self, event=None):
        if self.folder1:
            self.index1 = (self.index1 + 1) % len(self.folder1)
        if self.folder2:
            self.index2 = (self.index2 + 1) % len(self.folder2)
        self.combine_current()

    def prev_both(self, event=None):
        if self.folder1:
            self.index1 = (self.index1 - 1) % len(self.folder1)
        if self.folder2:
            self.index2 = (self.index2 - 1) % len(self.folder2)
        self.combine_current()

    def next_top(self, event=None):
        if self.folder1:
            self.index1 = (self.index1 + 1) % len(self.folder1)
        self.combine_current()

    def prev_top(self, event=None):
        if self.folder1:
            self.index1 = (self.index1 - 1) % len(self.folder1)
        self.combine_current()

    def next_bottom(self, event=None):
        if self.folder2:
            self.index2 = (self.index2 + 1) % len(self.folder2)
        self.combine_current()

    def prev_bottom(self, event=None):
        if self.folder2:
            self.index2 = (self.index2 - 1) % len(self.folder2)
        self.combine_current()

    def bind_keys(self):
        self.root.bind("<Right>", self.next_both)
        self.root.bind("<Left>", self.prev_both)
        self.root.bind("a", self.prev_top)
        self.root.bind("d", self.next_top)
        self.root.bind("w", self.prev_bottom)
        self.root.bind("s", self.next_bottom)
        self.root.bind("g", lambda e: self.show_grid_view())
        self.root.bind("v", lambda e: self.show_single_view())
        self.root.bind("q", lambda e: self.root.quit())
        self.root.bind("<Return>", lambda e: self.save_all_combined  ())

# ---------- Run App ----------
if __name__ == "__main__":
    root = Tk()
    app = ImageCombinerApp(root)
    root.mainloop()
