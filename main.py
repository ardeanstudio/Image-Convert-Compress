import os
import threading
from tkinter import Tk, Label, Button, filedialog, Scale, messagebox, StringVar, Radiobutton, HORIZONTAL
from PIL import Image
import imageio
# import pyheif --- Untuk Support Konversi dari Heic/Heif ke format yang tersedia, harus menggunakan Library ini. Disini saya belum support dikarenakan kendala pada sistem saya.

# Membuat Class
class PythonImageTools:
    def __init__(self, master):
        self.master = master
        master.title("Python Image Tools")

        self.label = Label(master, text="Selamat datang di Image Compressor!")
        self.label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        self.select_button = Button(master, text="Pilih Gambar", command=self.select_images)
        self.select_button.grid(row=1, column=0, columnspan=3, pady=(5, 10))

        self.quality_label = Label(master, text="Kualitas Kompresi:")
        self.quality_label.grid(row=2, column=0, pady=5, sticky='e')

        self.quality_scale = Scale(master, from_=0, to=100, orient=HORIZONTAL, length=150)
        self.quality_scale.set(50)  # Ukuran Bawaan
        self.quality_scale.grid(row=2, column=1, pady=5, sticky='w')

        self.preserve_quality_checkbox = Button(master, text="Jaga Kualitas", command=self.toggle_quality_preservation)
        self.preserve_quality = False
        self.preserve_quality_checkbox.grid(row=2, column=2, pady=5, padx=(0, 5))

        self.format_label = Label(master, text="Format Kompresi:")
        self.format_label.grid(row=3, column=0, pady=5, sticky='e')

        self.selected_format = StringVar(master)
        self.selected_format.set("JPEG")  # Format Bawaan
        self.format_options = ["WebP", "PNG", "JPEG", "HEIC", "HEIF"]  # Changed order for compactness
        self.format_radio_buttons = []
        for idx, format_option in enumerate(self.format_options):
            button = Radiobutton(master, text=format_option, variable=self.selected_format, value=format_option)
            self.format_radio_buttons.append(button)
            button.grid(row=3, column=idx + 1, pady=5, padx=(0, 5), sticky='w')

        self.convert_button = Button(master, text="Konversi Format", command=self.convert_images)
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=(10, 5))

        self.compress_button = Button(master, text="Kompres Gambar", command=self.compress_images)
        self.compress_button.grid(row=5, column=0, columnspan=3, pady=(5, 10))

        self.status_label = Label(master, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10)

        self.image_paths = []

# Membuka Prompt Explorer untuk memilih gambar dengan format yang tersedia
    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.heic;*.heif")])

    def toggle_quality_preservation(self):
        self.preserve_quality = not self.preserve_quality

    def compress_images(self):
        if self.image_paths:
            output_directory = filedialog.askdirectory(title="Pilih Direktori untuk Menyimpan Gambar Terkompresi")

            if output_directory:
                quality = self.quality_scale.get()
                selected_format = self.selected_format.get()

                # Menggunakan threading untuk mengompres gambar secara paralel
                thread = threading.Thread(target=self.compress_images_in_directory, args=(self.image_paths, output_directory, quality, self.preserve_quality, selected_format))
                thread.start()
            else:
                self.label.config(text="Pilih direktori untuk menyimpan gambar terkompresi.")
        else:
            self.label.config(text="Pilih gambar terlebih dahulu.")

    def convert_images(self):
        if self.image_paths:
            output_directory = filedialog.askdirectory(title="Pilih Direktori untuk Menyimpan Gambar Terkompresi")

            if output_directory:
                selected_format = self.selected_format.get()

                # Menggunakan threading untuk mengonversi format gambar secara paralel
                thread = threading.Thread(target=self.convert_images_in_directory, args=(self.image_paths, output_directory, selected_format))
                thread.start()
            else:
                self.label.config(text="Pilih direktori untuk menyimpan gambar terkompresi.")
        else:
            self.label.config(text="Pilih gambar terlebih dahulu.")

    def compress_images_in_directory(self, input_paths, output_directory, quality=85, preserve_quality=False, selected_format="JPEG"):
        try:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            total_images = len(input_paths)
            for idx, input_path in enumerate(input_paths):
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_directory, f"{name}.{selected_format.lower()}")  # Perbaikan nama file output
                self.compress_and_save(input_path, output_path, quality, preserve_quality, selected_format)

                # Update status label secara real-time
                progress_text = f"Proses {idx + 1}/{total_images} sedang berlangsung..."
                self.status_label.config(text=progress_text)
                self.master.update_idletasks()

            # Menampilkan jendela pesan setelah proses kompresi selesai
            messagebox.showinfo("Proses Selesai", "Proses kompresi berhasil selesai!")

            # Reset status label setelah selesai
            self.status_label.config(text="")

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def convert_images_in_directory(self, input_paths, output_directory, selected_format="JPEG"):
        try:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            total_images = len(input_paths)
            for idx, input_path in enumerate(input_paths):
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_directory, f"{name}.{selected_format.lower()}")  # Perbaikan nama file output
                self.convert_and_save(input_path, output_path, selected_format)

                # Update status label secara real-time
                progress_text = f"Proses {idx + 1}/{total_images} sedang berlangsung..."
                self.status_label.config(text=progress_text)
                self.master.update_idletasks()

            # Menampilkan jendela pesan setelah proses konversi selesai
            messagebox.showinfo("Proses Selesai", "Proses konversi format berhasil selesai!")

            # Reset status label setelah selesai
            self.status_label.config(text="")

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def compress_and_save(self, input_path, output_path, quality=85, preserve_quality=False, selected_format="JPEG"):
        try:
            image = Image.open(input_path)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            if preserve_quality:
                image.save(output_path, format=selected_format.upper(), quality=95)  # Adjust the quality as needed
            else:
                image.save(output_path, format=selected_format.upper(), quality=quality)

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def convert_and_save(self, input_path, output_path, selected_format="JPEG"):
        try:
            if selected_format.upper() in ["HEIC", "HEIF"]:
                self.convert_heic_heif(input_path, output_path, selected_format)
            else:
                image = Image.open(input_path)

                if image.mode != 'RGB':
                    image = image.convert('RGB')

                image.save(output_path, format=selected_format.upper())  # Save in the selected format

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def convert_heic_heif(self, input_path, output_path, selected_format="JPEG"):
        try:
            heif_image = imageio.imread(input_path)
            image = Image.fromarray(heif_image)

            # Save in the selected format
            image.save(output_path, format=selected_format.upper())

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = Tk()
    app = PythonImageTools(root)
    root.mainloop()
