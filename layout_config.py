from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QTextEdit,
    QTableWidget, QDateEdit, QSpinBox, QComboBox, QLabel,
    QGroupBox, QFormLayout, QSizePolicy, QFrame, QAbstractItemView
)
from PySide6.QtCore import QDate, Qt
from utils.constants import DISPLAY_DATE_FORMAT, DATE_INPUT_WIDTH

DEFAULT_LAYOUT_SPACING = 10
DEFAULT_LAYOUT_MARGINS = (12, 12, 12, 12)


def create_page_layout(spacing: int = DEFAULT_LAYOUT_SPACING, margins=DEFAULT_LAYOUT_MARGINS):
    layout = QVBoxLayout()
    layout.setSpacing(spacing)
    layout.setContentsMargins(*margins)
    return layout


def create_row_layout(spacing: int = 6):
    layout = QHBoxLayout()
    layout.setSpacing(spacing)
    return layout


def create_page_title(text: str) -> QLabel:
    title = QLabel(text)
    font = title.font()
    font.setPointSize(12)
    font.setBold(True)
    title.setFont(font)
    title.setContentsMargins(0, 0, 0, 12)
    return title


def create_form_group(text: str):
    group = QGroupBox(text)
    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    form_layout.setHorizontalSpacing(14)
    form_layout.setVerticalSpacing(10)
    group.setLayout(form_layout)
    group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return group, form_layout


def create_action_row(*widgets) -> QHBoxLayout:
    row = QHBoxLayout()
    row.addStretch()
    for widget in widgets:
        row.addWidget(widget)
    return row


def create_readonly_label(text: str = '') -> QLabel:
    label = QLabel(text)
    label.setFrameShape(QFrame.NoFrame)
    label.setLineWidth(0)
    label.setContentsMargins(0, 0, 0, 0)
    label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    label.setStyleSheet("background: transparent; color: #222222;")
    return label


def create_date_edit(min_date: QDate | None = None, max_date: QDate | None = None, calendar_popup: bool = True, display_format: str = DISPLAY_DATE_FORMAT, width: int = DATE_INPUT_WIDTH) -> QDateEdit:
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(calendar_popup)
    date_edit.setDisplayFormat(display_format)
    date_edit.setFixedWidth(width)
    if min_date is not None:
        date_edit.setMinimumDate(min_date)
    if max_date is not None:
        date_edit.setMaximumDate(max_date)
    return date_edit


def create_button(text: str, default: bool = False, auto_default: bool = True) -> QPushButton:
    button = QPushButton(text)
    button.setDefault(default)
    button.setAutoDefault(auto_default)
    return button


def create_text_input(placeholder: str = '', max_length: int | None = None, validator=None) -> QLineEdit:
    text_input = QLineEdit()
    if max_length is not None:
        text_input.setMaxLength(max_length)
    if placeholder:
        text_input.setPlaceholderText(placeholder)
    if validator is not None:
        text_input.setValidator(validator)
    return text_input


def create_multiline_text_edit(placeholder: str = '') -> QTextEdit:
    text_edit = QTextEdit()
    if placeholder:
        text_edit.setPlaceholderText(placeholder)
    return text_edit


def create_table_widget(rows: int = 0, columns: int = 0, headers: list[str] | None = None, editable: bool = False) -> QTableWidget:
    table = QTableWidget()
    table.setRowCount(rows)
    table.setColumnCount(columns)
    if headers:
        table.setHorizontalHeaderLabels(headers)
    if not editable:
        table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setStretchLastSection(True)
    return table


def create_spin_box(min_value: int = 0, max_value: int = 100, step: int = 1) -> QSpinBox:
    spin_box = QSpinBox()
    spin_box.setRange(min_value, max_value)
    spin_box.setSingleStep(step)
    return spin_box


def create_combo_box(items: list[str] | None = None) -> QComboBox:
    combo_box = QComboBox()
    if items:
        combo_box.addItems(items)
    return combo_box


def create_label(text: str = '') -> QLabel:
    label = QLabel(text)
    return label
