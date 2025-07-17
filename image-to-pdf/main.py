import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from converter import convert_images_to_pdf

class ImageToPDFConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Image to PDF Converter")
        self.geometry("800x600")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.selected_files = []

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Image to PDF Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Instructions
        self.instructions = ctk.CTkLabel(
            self.main_frame,
            text="Select one or multiple images to convert to PDF",
            font=ctk.CTkFont(size=14)
        )
        self.instructions.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Selected files list
        self.files_frame = ctk.CTkFrame(self.main_frame)
        self.files_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.files_textbox = ctk.CTkTextbox(self.files_frame, width=600, height=300)
        self.files_textbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.files_textbox.configure(state="disabled")

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Select files button
        self.select_button = ctk.CTkButton(
            self.button_frame,
            text="Select Images",
            command=self.select_files,
            width=200
        )
        self.select_button.grid(row=0, column=0, padx=10, pady=10)

        # Clear selection button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear Selection",
            command=self.clear_selection,
            width=200,
            fg_color="transparent",
            border_width=2
        )
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Convert button
        self.convert_button = ctk.CTkButton(
            self.main_frame,
            text="Convert to PDF",
            command=self.convert_to_pdf,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.convert_button.grid(row=4, column=0, padx=20, pady=(0, 20))

    def update_files_list(self):
        self.files_textbox.configure(state="normal")
        self.files_textbox.delete("1.0", "end")
        for i, file in enumerate(self.selected_files, 1):
            self.files_textbox.insert("end", f"{i}. {os.path.basename(file)}\n")
        self.files_textbox.configure(state="disabled")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp")
            ]
        )
        if files:
            self.selected_files.extend(files)
            self.update_files_list()

    def clear_selection(self):
        self.selected_files.clear()
        self.update_files_list()

    def convert_to_pdf(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one image first!")
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as"
        )

        if output_file:
            try:
                convert_images_to_pdf(self.selected_files, output_file)
                messagebox.showinfo(
                    "Success",
                    f"PDF has been created successfully!\nSaved as: {output_file}"
                )
                # Clear selection after successful conversion
                self.clear_selection()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = ImageToPDFConverter()
    app.mainloop()
