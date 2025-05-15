# audio_compressor.py

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QSlider, QHBoxLayout
)
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
import tempfile

class AudioCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro Audio Compressor")
        self.setAcceptDrops(True)
        self.setMinimumSize(500, 300)
        self.setStyleSheet("background-color: #1e1e2f; color: white; font-family: 'Segoe UI';")

        self.audio = None
        self.file_path = None

        # Layout
        layout = QVBoxLayout()

        self.title_label = QLabel("🎧 Pro Audio Compressor")
        self.title_label.setFont(QFont("Segoe UI", 18))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.info_label = QLabel("Drag and drop your audio file here")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        # Compression sliders
        slider_layout = QHBoxLayout()
        self.ratio_slider = self._create_slider("Ratio", 1, 10)
        self.threshold_slider = self._create_slider("Threshold (dB)", -60, 0)

        slider_layout.addLayout(self.ratio_slider['layout'])
        slider_layout.addLayout(self.threshold_slider['layout'])
        layout.addLayout(slider_layout)

        # Buttons
        self.compress_button = QPushButton("Compress & Export")
        self.compress_button.clicked.connect(self.compress_audio)
        layout.addWidget(self.compress_button)

        self.setLayout(layout)

    def _create_slider(self, name, min_val, max_val):
        container = QVBoxLayout()
        label = QLabel(f"{name}:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue((min_val + max_val) // 2)
        slider.setStyleSheet("QSlider { margin: 10px; }")
        container.addWidget(label)
        container.addWidget(slider)
        return {'layout': container, 'slider': slider}

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith((".mp3", ".wav", ".flac", ".ogg")):
                self.file_path = path
                self.audio = AudioSegment.from_file(path)
                self.info_label.setText(f"Loaded: {os.path.basename(path)}")
                return
        self.info_label.setText("Unsupported file format!")

    def compress_audio(self):
        if not self.audio:
            self.info_label.setText("No audio loaded!")
            return

        ratio = self.ratio_slider['slider'].value()
        threshold = self.threshold_slider['slider'].value()

        compressed = compress_dynamic_range(
            self.audio,
            threshold=threshold,
            ratio=ratio,
            attack=5.0,
            release=50.0
        )

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Compressed Audio", "compressed.wav", "WAV files (*.wav)"
        )
        if save_path:
            compressed.export(save_path, format="wav")
            self.info_label.setText(f"Audio compressed and saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioCompressor()
    window.show()
    sys.exit(app.exec())
