import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AdditionalPackages(QWidget):
    def __init__(self):
        super().__init__()
        # --- Prices (can be dynamic or from a data source) ---
        self.flight_price_val = 259.50
        self.karaoke_price_val = 20.00
        self.pizza_price_val = 35.00
        # Adding two baggage options as per previous discussions
        self.baggage_25kg_price_val = 45.00  # Example price
        self.baggage_8kg_price_val = 15.00  # Example price

        self.selected_packages_price = 0.00
        self.discount_val = 0.00  # Placeholder for discount logic

        self.init_ui()
        self.update_total()  # Initial calculation and display

    def init_ui(self):
        self.setWindowTitle("Additional Packages - user1")
        self.setGeometry(200, 100, 850, 600)  # Adjusted size
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D; /* Main very dark background */
                color: #E0E0E0; /* Default light text color */
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #E0E0E0;
            }
            QCheckBox {
                color: #E0E0E0;
                spacing: 7px; /* Space between checkbox and text */
                font-size: 11pt;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #777777;
                border-radius: 4px; /* Slightly rounded */
                background-color: #404040;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #999999;
            }
            QCheckBox::indicator:checked {
                background-color: #5A8B4C; /* Green for check */
                border: 1px solid #5A8B4C;
                /* Add check mark image if desired, or use unicode check */
            }
            QPushButton {
                background-color: #4CAF50; /* Green for buttons */
                color: white;
                border: none;
                padding: 8px 12px;
                text-align: center;
                font-size: 10pt;
                font-weight: bold;
                border-radius: 5px;
                min-height: 28px; /* Consistent button height */
            }
            QPushButton:hover {
                background-color: #5A8B4C; /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #40913C;
            }
            QLineEdit {
                background-color: #4A4A4A; /* Lighter gray for input */
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
                padding: 7px;
                font-size: 10pt;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        # --- Flight Info Header ---
        flight_info_text = ("<span style='font-size:11pt;'>"
                            "<b>Flight: Ryanair</b> | Brussels to Paris | "
                            "2025-05-01 09:30:00 - 2025-05-01 11:45:00 | "
                            f"<b>Price: {self.flight_price_val:.2f} €</b></span>")
        self.flight_info_label = QLabel(flight_info_text)
        self.flight_info_label.setAlignment(Qt.AlignCenter)
        self.flight_info_label.setStyleSheet("background-color: #383838; padding: 12px; border-radius: 6px;")
        main_layout.addWidget(self.flight_info_label)

        # --- "Ticket reserved!" Text ---
        reserved_label = QLabel("Ticket reserved! Now choose your additional packages.")
        reserved_label.setAlignment(Qt.AlignCenter)
        reserved_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(reserved_label)

        # --- Main Content Area (Packages Left, Summary Right) ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        # --- Left Panel (Packages, Discount, Buy Button) ---
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setSpacing(20)  # Spacing within the left panel

        # Packages Frame
        packages_frame = QFrame()
        packages_frame.setObjectName("PackagesFrame")
        packages_frame.setStyleSheet("""
            QFrame#PackagesFrame {
                background-color: #3A3A3A; /* Slightly lighter dark gray */
                border-radius: 8px;
                padding: 20px; /* More padding */
            }
        """)
        packages_inner_layout = QVBoxLayout(packages_frame)
        packages_inner_layout.setContentsMargins(0, 0, 0, 0)  # Reset inner margins
        packages_inner_layout.setSpacing(15)  # Spacing between package items

        # Helper to create package item
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

        packages_inner_layout.addStretch(1)  # Push packages to the top
        left_panel_layout.addWidget(packages_frame)

        # Discount Code Section (within left panel)
        discount_section_layout = QHBoxLayout()
        discount_section_layout.setContentsMargins(0, 0, 0, 0)  # No extra margins here, use parent's

        discount_label = QLabel("Discount Code:")
        discount_label.setFont(QFont("Arial", 10))
        discount_section_layout.addWidget(discount_label)

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("")  # Image shows no placeholder
        self.discount_input.setFixedWidth(180)
        discount_section_layout.addWidget(self.discount_input)
        discount_section_layout.addSpacing(10)

        self.discount_btn = QPushButton("Apply Discount")
        self.discount_btn.setFixedWidth(130)
        # self.discount_btn.clicked.connect(self.apply_discount_code)
        discount_section_layout.addWidget(self.discount_btn)
        discount_section_layout.addStretch(1)  # Push elements to the left
        left_panel_layout.addLayout(discount_section_layout)

        # Buy Button (within left panel, aligned)
        buy_button_container = QHBoxLayout()  # To control buy button's position
        buy_button_container.addStretch(1)  # Pushes to center/right
        self.buy_btn = QPushButton("Buy")
        self.buy_btn.setMinimumSize(160, 40)
        self.buy_btn.setFont(QFont("Arial", 12, QFont.Bold))
        # self.buy_btn.clicked.connect(self.process_buy)
        buy_button_container.addWidget(self.buy_btn)
        buy_button_container.addStretch(1)  # Pushes to center/left
        left_panel_layout.addLayout(buy_button_container)

        left_panel_layout.addStretch(1)  # Push content in left panel up
        content_layout.addLayout(left_panel_layout, 2)  # Left panel takes 2/3rds width ratio

        # --- Right Panel (Summary Box) ---
        summary_frame = QFrame()
        summary_frame.setObjectName("SummaryFrame")
        summary_frame.setFixedWidth(280)  # Adjusted width
        summary_frame.setStyleSheet("""
            QFrame#SummaryFrame {
                background-color: #3A3A3A; /* Same as packages */
                border: 1px solid #484848; /* Slightly visible border */
                border-radius: 8px;
                padding: 15px; /* More padding */
            }
            QFrame#SummaryFrame QLabel {
                font-size: 10pt; /* Base font for summary items */
                color: #D0D0D0; /* Slightly softer white */
            }
        """)
        summary_layout = QGridLayout(summary_frame)
        summary_layout.setVerticalSpacing(10)
        summary_layout.setHorizontalSpacing(10)
        summary_layout.setContentsMargins(15, 15, 15, 15)

        # Summary Labels and Values
        self.summary_flight_label = QLabel("Flight:")
        self.summary_flight_value = QLabel(f"{self.flight_price_val:.2f} €")
        self.summary_flight_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.summary_packages_label = QLabel("Selected packages:")
        self.summary_packages_value = QLabel(f"{self.selected_packages_price:.2f} €")
        self.summary_packages_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.summary_discount_label = QLabel("Discount:")
        self.summary_discount_value = QLabel(f"{self.discount_val:.2f} €")
        self.summary_discount_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: none; border-top: 1px solid #505050; margin-top: 5px; margin-bottom: 5px;")

        self.summary_total_label = QLabel("Total:")
        self.summary_total_value = QLabel(
            f"{(self.flight_price_val + self.selected_packages_price - self.discount_val):.2f} €")
        self.summary_total_label.setFont(QFont("Arial", 11, QFont.Bold))  # Bolder total
        self.summary_total_value.setFont(QFont("Arial", 11, QFont.Bold))  # Bolder total
        self.summary_total_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.summary_total_value.setStyleSheet("color: #FFFFFF;")  # Brighter white for total
        self.summary_total_label.setStyleSheet("color: #FFFFFF;")

        summary_layout.addWidget(self.summary_flight_label, 0, 0)
        summary_layout.addWidget(self.summary_flight_value, 0, 1)
        summary_layout.addWidget(self.summary_packages_label, 1, 0)
        summary_layout.addWidget(self.summary_packages_value, 1, 1)
        summary_layout.addWidget(self.summary_discount_label, 2, 0)
        summary_layout.addWidget(self.summary_discount_value, 2, 1)
        summary_layout.addWidget(line, 3, 0, 1, 2)  # Span 2 columns
        summary_layout.addWidget(self.summary_total_label, 4, 0)
        summary_layout.addWidget(self.summary_total_value, 4, 1)
        summary_layout.setRowStretch(5, 1)  # Push summary items to top

        content_layout.addWidget(summary_frame, 1)  # Right panel takes 1/3rd width ratio

        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)  # Push content area upwards if window is taller

    def update_total(self):
        self.selected_packages_price = 0.00
        if self.karaoke_cb.isChecked():
            self.selected_packages_price += self.karaoke_price_val
        if self.pizza_cb.isChecked():
            self.selected_packages_price += self.pizza_price_val
        if self.baggage_25kg_cb.isChecked():
            self.selected_packages_price += self.baggage_25kg_price_val
        if self.baggage_8kg_cb.isChecked():
            self.selected_packages_price += self.baggage_8kg_price_val

        self.summary_packages_value.setText(f"{self.selected_packages_price:.2f} €")
        # Apply discount logic if implemented
        # For now, discount_val is always 0.00
        self.summary_discount_value.setText(f"{self.discount_val:.2f} €")

        current_total = self.flight_price_val + self.selected_packages_price - self.discount_val
        self.summary_total_value.setText(f"{current_total:.2f} €")  # Update rich text total
        # Make total bold (already set font in init_ui, text update is enough)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdditionalPackages()
    window.show()
    sys.exit(app.exec_())