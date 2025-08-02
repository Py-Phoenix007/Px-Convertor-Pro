from PyQt6.QtCore import QThread, pyqtSignal
from file_converter import FileConverter
import os

class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str, int) # Message and timeout
    finished = pyqtSignal()

    def __init__(self, files_to_convert, output_directory):
        super().__init__()
        self.files_to_convert = files_to_convert
        self.output_directory = output_directory
        self.converter = FileConverter()
        self.is_running = True

    def run(self):
        print(f"ConversionWorker started with {len(self.files_to_convert)} files.")
        total_files = len(self.files_to_convert)
        if total_files == 0:
            print("No files to convert in worker.")
            self.finished.emit()
            return
        for i, (input_path, output_format) in enumerate(self.files_to_convert):
            if not self.is_running:
                print("Worker stopped early.")
                break
            base_name = os.path.basename(input_path)
            output_filename = f"{os.path.splitext(base_name)[0]}{output_format}"
            output_path = os.path.join(self.output_directory, output_filename)
            self.status.emit(f"({i+1}/{total_files}) Converting {base_name}...", 0)
            print(f"Converting {input_path} to {output_path}")
            try:
                self.converter.convert(input_path, output_path)
                print(f"Saved: {output_path}")
            except Exception as e:
                print(f"Error converting {base_name}: {e}")
                self.status.emit(f"Error converting {base_name}: {e}", 8000)
            progress_percentage = int(((i + 1) / total_files) * 100)
            self.progress.emit(progress_percentage)
        print("ConversionWorker finished.")
        self.status.emit("Conversion process finished.", 5000)
        self.finished.emit()

    def stop(self):
        self.is_running = False
