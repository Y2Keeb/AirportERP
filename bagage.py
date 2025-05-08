import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QBuffer  # Added QBuffer
from PyQt5.QtGui import QFont, QPixmap, QImage  # Added QPixmap, QImage

# --- QR Code Generation ---
import qrcode
from io import BytesIO  # To handle image data in memory


class AdditionalPackages(QWidget):
    def __init__(self):
        super().__init__()
        # --- Prices (can be dynamic or from a data source) ---
        self.flight_price_val = 259.50
        self.karaoke_price_val = 20.00
        self.pizza_price_val = 35.00
        self.baggage_25kg_price_val = 45.00
        self.baggage_8k##g_price_val = 15.00

        self.selected_packages_price = 0.00
        self.discount_val = 0.00

        # --- Flight Details for QR Code ---
        self.flight_details_for_qr = (
            f"Flight: Ryanair\n"
            f"Route: Brussels to Paris\n"
            f"Date: 2025-05-01\n"
            f"Time: 09:30 - 11:45\n"
            f"Price: {self.flight_price_val:.2f} EUR"
        )

        self.init_ui()
        self.update_total()

    def _generate_qr_code_pixmap(self, data, size=100):
        """Generates a QR code and returns it as a QPixmap."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,  # Adjust for QR code pixel size
                border=2,  # Border around QR code
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Convert PIL image to QPixmap
            buffer = BytesIO()
            img.save(buffer, "PNG")
            buffer.seek(0)
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue(), "PNG")
            pixmap = QPixmap.fromImage(qimage)
            return pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            # Return a placeholder pixmap or None
            placeholder = QPixmap(size, size)
            placeholder.fill(Qt.gray)
            return placeholder

    def init_ui(self):
        self.setWindowTitle("Additional Packages - user1")
        self.setGeometry(200, 100, 850, 650)  # Slightly increased height for QR
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: #E0E0E0;
                font-family: Arial, sans-serif;
            }
            QLabel { color: #E0E0E0; }
            QCheckBox { color: #E0E0E0; spacing: 7px; font-size: 11pt; }
            QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #777777; border-radius: 4px; background-color: #404040; }
            QCheckBox::indicator:hover { border: 1px solid #999999; }
            QCheckBox::indicator:checked { background-color: #5A8B4C; border: 1px solid #5A8B4C; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 12px; text-align: center; font-size: 10pt; font-weight: bold; border-radius: 5px; min-height: 28px; }
            QPushButton:hover { background-color: #5A8B4C; }
            QPushButton:pressed { background-color: #40913C; }
            QLineEdit { background-color: #4A4A4A; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 5px; padding: 7px; font-size: 10pt; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        flight_info_text = ("<span style='font-size:11pt;'>"
                            "<b>Flight: Ryanair</b> | Brussels to Paris | "
                            "2025-05-01 09:30:00 - 2025-05-01 11:45:00 | "
                            f"<b>Price: {self.flight_price_val:.2f} €</b></span>")
        self.flight_info_label = QLabel(flight_info_text)
        self.flight_info_label.setAlignment(Qt.AlignCenter)
        self.flight_info_label.setStyleSheet("background-color: #383838; padding: 12px; border-radius: 6px;")
        main_layout.addWidget(self.flight_info_label)

        reserved_label = QLabel("Ticket reserved! Now choose your additional packages.")
        reserved_label.setAlignment(Qt.AlignCenter)
        reserved_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(reserved_label)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        left_panel_layout = QVBoxLayout()
        left_panel_layout.setSpacing(20)

        packages_frame = QFrame()
        packages_frame.setObjectName("PackagesFrame")
        packages_frame.setStyleSheet("""
            QFrame#PackagesFrame { background-color: #3A3A3A; border-radius: 8px; padding: 20px; }
        """)
        packages_inner_layout = QVBoxLayout(packages_frame)
        packages_inner_layout.setContentsMargins(0, 0, 0, 0)
        packages_inner_layout.setSpacing(15)

        def create_package_item(layout, checkbox_var, text, price, desc_text):
            checkbox_var.setText(f"{text} – {price:.2f} €")
            checkbox_var.stateChanged.connect(self.update_total)
            layout.addWidget(checkbox_var)
            desc_label = QLabel(desc_text)
            desc_label.setFont(QFont("Arial", 9))
            desc_label.setStyleSheet("color: #B0B0B0; padding-left: 28px; margin-top: -5px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        self.karaoke_cb = QCheckBox()
        create_package_item(packages_inner_layout, self.karaoke_cb, "Sky Karaoke Add-On", self.karaoke_price_val,
                            "Sing your heart out at 30,000 feet. Mic provided, pitch not guaranteed.")
        self.pizza_cb = QCheckBox()
        create_package_item(packages_inner_layout, self.pizza_cb, "Emergency Pizza Button", self.pizza_price_val,
                            "Hit the button, receive pizza. Don’t ask where it comes from.")
        self.baggage_25kg_cb = QCheckBox()
        create_package_item(packages_inner_layout, self.baggage_25kg_cb, "Checked Baggage (25kg)",
                            self.baggage_25kg_price_val,
                            "Standard checked baggage allowance (up to 25kg).")
        self.baggage_8kg_cb = QCheckBox()
        create_package_item(packages_inner_layout, self.baggage_8kg_cb, "Cabin Baggage (8kg)",
                            self.baggage_8kg_price_val,
                            "One cabin bag (up to 8kg, size restrictions apply).")
        packages_inner_layout.addStretch(1)
        left_panel_layout.addWidget(packages_frame)

        discount_section_layout = QHBoxLayout()
        discount_section_layout.setContentsMargins(0, 0, 0, 0)
        discount_label = QLabel("Discount Code:")
        discount_label.setFont(QFont("Arial", 10))
        discount_section_layout.addWidget(discount_label)
        self.discount_input = QLineEdit()
        self.discount_input.setFixedWidth(180)
        discount_section_layout.addWidget(self.discount_input)
        discount_section_layout.addSpacing(10)
        self.discount_btn = QPushButton("Apply Discount")
        self.discount_btn.setFixedWidth(130)
        discount_section_layout.addWidget(self.discount_btn)
        discount_section_layout.addStretch(1)
        left_panel_layout.addLayout(discount_section_layout)

        buy_button_container = QHBoxLayout()
        buy_button_container.addStretch(1)
        self.buy_btn = QPushButton("Buy")
        self.buy_btn.setMinimumSize(160, 40)
        self.buy_btn.setFont(QFont("Arial", 12, QFont.Bold))
        buy_button_container.addWidget(self.buy_btn)
        buy_button_container.addStretch(1)
        left_panel_layout.addLayout(buy_button_container)
        left_panel_layout.addStretch(1)
        content_layout.addLayout(left_panel_layout, 2)

        summary_frame = QFrame()
        summary_frame.setObjectName("SummaryFrame")
        summary_frame.setFixedWidth(280)
        summary_frame.setStyleSheet("""
            QFrame#SummaryFrame { background-color: #3A3A3A; border: 1px solid #484848; border-radius: 8px; padding: 15px; }
            QFrame#SummaryFrame QLabel { font-size: 10pt; color: #D0D0D0; }
        """)
        summary_layout = QGridLayout(summary_frame)  # Changed to QGridLayout
        summary_layout.setVerticalSpacing(10)
        summary_layout.setHorizontalSpacing(10)
        summary_layout.setContentsMargins(15, 15, 15, 15)

        self.summary_flight_label = QLabel("Flight:")
        self.summary_flight_value = QLabel(f"{self.flight_price_val:.2f} €")
        self.summary_flight_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        summary_layout.addWidget(self.summary_flight_label, 0, 0)
        summary_layout.addWidget(self.summary_flight_value, 0, 1)

        self.summary_packages_label = QLabel("Selected packages:")
        self.summary_packages_value = QLabel(f"{self.selected_packages_price:.2f} €")
        self.summary_packages_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        summary_layout.addWidget(self.summary_packages_label, 1, 0)
        summary_layout.addWidget(self.summary_packages_value, 1, 1)

        self.summary_discount_label = QLabel("Discount:")
        self.summary_discount_value = QLabel(f"{self.discount_val:.2f} €")
        self.summary_discount_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        summary_layout.addWidget(self.summary_discount_label, 2, 0)
        summary_layout.addWidget(self.summary_discount_value, 2, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: none; border-top: 1px solid #505050; margin-top: 5px; margin-bottom: 5px;")
        summary_layout.addWidget(line, 3, 0, 1, 2)  # Span 2 columns for the line

        self.summary_total_label = QLabel("Total:")
        self.summary_total_value = QLabel(
            f"{(self.flight_price_val + self.selected_packages_price - self.discount_val):.2f} €")
        self.summary_total_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.summary_total_value.setFont(QFont("Arial", 11, QFont.Bold))
        self.summary_total_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.summary_total_value.setStyleSheet("color: #FFFFFF;")
        self.summary_total_label.setStyleSheet("color: #FFFFFF;")
        summary_layout.addWidget(self.summary_total_label, 4, 0)
        summary_layout.addWidget(self.summary_total_value, 4, 1)

        # --- QR Code Section ---
        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(Qt.AlignCenter)
        qr_pixmap = self._generate_qr_code_pixmap(self.flight_details_for_qr, size=110)  # Adjust size as needed
        if qr_pixmap:
            self.qr_code_label.setPixmap(qr_pixmap)
        # Add QR code under the total, spanning both columns and centered
        summary_layout.addWidget(self.qr_code_label, 5, 0, 1, 2, Qt.AlignCenter)  # Row 5, Col 0, RowSpan 1, ColSpan 2

        summary_layout.setRowStretch(6, 1)  # Push content up, ensuring QR code isn't pushed too far down

        content_layout.addWidget(summary_frame, 1)
        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)

    def update_total(self):
        self.selected_packages_price = 0.00
        if self.karaoke_cb.isChecked(): self.selected_packages_price += self.karaoke_price_val
        if self.pizza_cb.isChecked(): self.selected_packages_price += self.pizza_price_val
        if self.baggage_25kg_cb.isChecked(): self.selected_packages_price += self.baggage_25kg_price_val
        if self.baggage_8kg_cb.isChecked(): self.selected_packages_price += self.baggage_8kg_price_val

        self.summary_packages_value.setText(f"{self.selected_packages_price:.2f} €")
        self.summary_discount_value.setText(f"{self.discount_val:.2f} €")
        current_total = self.flight_price_val + self.selected_packages_price - self.discount_val
        self.summary_total_value.setText(f"{current_total:.2f} €")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdditionalPackages()
    window.show()
    sys.exit(app.exec_())
