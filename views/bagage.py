from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QGroupBox
)

class AdditionalPackages(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.flight_price = 259.5
        self.karaoke_price = 20
        self.pizza_price = 35
        self.baggage_price = 40  # Example price for baggage

        self.selected_packages = 0

        main_layout = QVBoxLayout()

        # Title
        title = QLabel(
            "Flight: Ryanair | Brussels to Paris | 2025-05-01 09:30:00 - 2025-05-01 11:45:00 | Price: 259.5"
        )
        main_layout.addWidget(title)

        # Packages group
        packages_group = QGroupBox()
        packages_layout = QVBoxLayout()

        self.karaoke_cb = QCheckBox("Sky Karaoke Add-On – 20 €")
        self.karaoke_cb.stateChanged.connect(self.update_total)
        packages_layout.addWidget(self.karaoke_cb)
        packages_layout.addWidget(QLabel("Sing your heart out at 30,000 feet. Mic provided, pitch not guaranteed."))

        self.pizza_cb = QCheckBox("Emergency Pizza Button – 35 €")
        self.pizza_cb.stateChanged.connect(self.update_total)
        packages_layout.addWidget(self.pizza_cb)
        packages_layout.addWidget(QLabel("Hit the button, receive pizza. Don’t ask where it comes from."))

        # BAGGAGE ADD-ON
        self.baggage_cb = QCheckBox("Baggage Add-On – 40 €")
        self.baggage_cb.stateChanged.connect(self.update_total)
        packages_layout.addWidget(self.baggage_cb)
        packages_layout.addWidget(QLabel("Add checked baggage to your flight."))

        packages_group.setLayout(packages_layout)
        main_layout.addWidget(packages_group)

        # Discount code
        discount_layout = QHBoxLayout()
        self.discount_input = QLineEdit()
        discount_layout.addWidget(self.discount_input)
        self.discount_btn = QPushButton("Apply Discount")
        discount_layout.addWidget(self.discount_btn)
        main_layout.addLayout(discount_layout)

        # Price summary
        self.summary_label = QLabel(self.get_summary_text())
        main_layout.addWidget(self.summary_label)

        # Buy button
        self.buy_btn = QPushButton("Buy")
        main_layout.addWidget(self.buy_btn)

        self.setLayout(main_layout)

    def update_total(self):
        self.selected_packages = 0
        if self.karaoke_cb.isChecked():
            self.selected_packages += self.karaoke_price
        if self.pizza_cb.isChecked():
            self.selected_packages += self.pizza_price
        if self.baggage_cb.isChecked():
            self.selected_packages += self.baggage_price
        self.summary_label.setText(self.get_summary_text())

    def get_summary_text(self):
        total = self.flight_price + self.selected_packages
        return (
            f"Flight: {self.flight_price:.2f} €\n"
            f"Selected packages: {self.selected_packages:.2f} €\n"
            f"Discount: 0.00 €\n"
            f"Total: {total:.2f} €"
        )

if __name__ == "__main__":
    app = QApplication([])
    window = AdditionalPackages()
    window.show()
    app.exec_()