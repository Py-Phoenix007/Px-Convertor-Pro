from PIL import Image
from pydub import AudioSegment
import ffmpeg
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
try:
    from pdf2docx import Converter as PDF2DocxConverter
except ImportError:
    PDF2DocxConverter = None

class FileConverter:
    def convert(self, input_path, output_path):
        _, input_ext = os.path.splitext(input_path)
        _, output_ext = os.path.splitext(output_path)
        input_ext = input_ext.lower()
        output_ext = output_ext.lower()

        try:
            if input_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
                self._convert_image(input_path, output_path)
            elif input_ext in ['.mp3', '.wav', '.ogg', '.flac']:
                self._convert_audio(input_path, output_path)
            elif input_ext in ['.mp4', '.avi', '.mov', '.mkv']:
                self._convert_video(input_path, output_path)
            elif input_ext == '.docx' and output_ext == '.pdf':
                self._convert_docx_to_pdf(input_path, output_path)
            elif input_ext == '.pdf' and output_ext == '.docx':
                self._convert_pdf_to_docx(input_path, output_path)
            elif input_ext in ['.txt', '.py', '.json', '.csv', '.xml', '.html', '.md', '.rtf', '.log', '.ini', '.yaml', '.yml']:
                if output_ext in ['.txt', '.py', '.json', '.csv', '.xml', '.html', '.md', '.rtf', '.log', '.ini', '.yaml', '.yml']:
                    self._copy_text_file(input_path, output_path)
                elif output_ext == '.pdf':
                    self._convert_text_to_pdf(input_path, output_path)
                else:
                    raise ValueError(f"Conversion from {input_ext} to {output_ext} is not supported.")
            else:
                raise ValueError(f"Conversion from {input_ext} to {output_ext} is not supported.")
        except Exception as e:
            raise RuntimeError(f"Failed to convert {os.path.basename(input_path)}: {e}")

    def _convert_pdf_to_docx(self, input_path, output_path):
        if PDF2DocxConverter is None:
            raise RuntimeError("pdf2docx is not installed. Please install it with 'pip install pdf2docx'.")
        converter = PDF2DocxConverter(input_path)
        converter.convert(output_path, start=0, end=None)
        converter.close()

    def _convert_image(self, input_path, output_path):
        with Image.open(input_path) as img:
            # Handle formats like GIF that may have transparency (alpha channel)
            if img.mode == 'RGBA' and output_path.lower().endswith(('.jpg', '.jpeg')):
                img = img.convert('RGB')
            img.save(output_path)

    def _convert_audio(self, input_path, output_path):
        _, output_ext = os.path.splitext(output_path)
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_ext[1:])

    def _convert_video(self, input_path, output_path):
        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, vcodec='copy', acodec='copy')
                .run(overwrite_output=True, quiet=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e}")

    def _convert_docx_to_pdf(self, input_path, output_path):
        # A basic implementation. For complex layouts, a more robust library may be needed.
        doc = Document(input_path)
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        y = height - 72
        for para in doc.paragraphs:
            if y < 72: # Basic page break
                c.showPage()
                y = height - 72
            c.drawString(72, y, para.text)
            y -= 20 # Line spacing
        c.save()

    def _copy_text_file(self, input_path, output_path):
        with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
            fout.write(fin.read())

    def _convert_text_to_pdf(self, input_path, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        y = height - 72
        with open(input_path, 'r', encoding='utf-8') as fin:
            for line in fin:
                if y < 72:
                    c.showPage()
                    y = height - 72
                c.drawString(72, y, line.rstrip())
                y -= 16
        c.save()
