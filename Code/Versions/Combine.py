import os
from tkinter import Tk, Button, filedialog, Canvas, Frame, Label
from PIL import Image, ImageTk

class VerticalImageCombiner:
    def __init__(self, root):
        self.root = root
        self.root.title("Vertical Image Combiner")

        # --- State ---
        self.folder1 = None
        self.folder2 = None
        self.images1 = []
        self.images2 = []
        self.idx1 = 0
        self.idx2 = 0
        self.current_combined = None

        # --- UI Layout ---
        top_frame = Frame(root)
        top_frame.pack(pady=5)

        Button(top_frame, text="Select Top Folder", command=self.load_folder1).pack(side="left", padx=5)
        Button(top_frame, text="Select Bottom Folder", command=self.load_folder2).pack(side="left", padx=5)
        Button(top_frame, text="Save (S)", command=self.save_combined).pack(side="left", padx=5)

        self.label_info = Label(root, text="No images loaded", font=("Arial", 10))
        self.label_info.pack(pady=3)

        self.canvas = Canvas(root, bg="#222")
        self.canvas.pack(padx=10, pady=10, expand=True, fill="both")

        # --- Keyboard bindings ---
        self.root.bind("<Left>", lambda e: self.change_image(-1, "A"))
        self.root.bind("<Right>", lambda e: self.change_image(1, "A"))
        self.root.bind("<Up>", lambda e: self.change_image(-1, "B"))
        self.root.bind("<Down>", lambda e: self.change_image(1, "B"))
        self.root.bind("<s>", lambda e: self.save_combined())

    # --- Folder Loaders ---
    def load_folder1(self):
        self.folder1 = filedialog.askdirectory(title="Select Top Folder")
        if self.folder1:
            self.images1 = self._get_images_from_folder(self.folder1)
            self.idx1 = 0
            self.display_combined()

    def load_folder2(self):
        self.folder2 = filedialog.askdirectory(title="Select Bottom Folder")
        if self.folder2:
            self.images2 = self._get_images_from_folder(self.folder2)
            self.idx2 = 0
            self.display_combined()

    def _get_images_from_folder(self, folder):
        return sorted([
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(("png", "jpg", "jpeg"))
        ])

    # --- Image Navigation ---
    def change_image(self, direction, folder):
        if folder == "A" and self.images1:
            self.idx1 = (self.idx1 + direction) % len(self.images1)
        elif folder == "B" and self.images2:
            self.idx2 = (self.idx2 + direction) % len(self.images2)
        self.display_combined()

    # --- Image Display ---
    def display_combined(self):
        if not self.images1 or not self.images2:
            self.label_info.config(text="Load both folders to view combined image.")
            return

        img_top = Image.open(self.images1[self.idx1]).convert("RGBA")
        img_bottom = Image.open(self.images2[self.idx2]).convert("RGBA")

        # Resize both to same width
        target_width = 600
        img_top = img_top.resize((target_width, int(img_top.height * target_width / img_top.width)))
        img_bottom = img_bottom.resize((target_width, int(img_bottom.height * target_width / img_bottom.width)))

        total_height = img_top.height + img_bottom.height
        combined = Image.new("RGBA", (target_width, total_height))
        combined.paste(img_top, (0, 0))
        combined.paste(img_bottom, (0, img_top.height))

        # Update UI
        self.tk_img = ImageTk.PhotoImage(combined)
        self.canvas.delete("all")
        self.canvas.config(width=target_width, height=total_height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Info label
        top_name = os.path.basename(self.images1[self.idx1])
        bottom_name = os.path.basename(self.images2[self.idx2])
        self.label_info.config(
            text=f"Top: ({self.idx1+1}/{len(self.images1)}) {top_name} | "
                 f"Bottom: ({self.idx2+1}/{len(self.images2)}) {bottom_name}"
        )

        self.current_combined = combined

    # --- Save Combined Image ---
    def save_combined(self):
        if not self.current_combined:
            self.label_info.config(text="⚠️ No combined image to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Combined Image"
        )
        if save_path:
            self.current_combined.save(save_path)
            self.label_info.config(text=f"✅ Saved combined image to: {save_path}")

# --- Run App ---
if __name__ == "__main__":
    root = Tk()
    root.geometry("650x800")
    app = VerticalImageCombiner(root)
    root.mainloop()
