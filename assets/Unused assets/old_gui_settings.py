menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: black;
                color: white;
                border-bottom: 3px solid #8B0000;  /* Blood red border at the bottom */
            }
            QMenuBar::item {
                background-color: black;
                color: white;
                padding: 5px 15px;  /* Adjust padding for better spacing */
                margin-right: 0px;  /* Remove margins to ensure full stretch */
                border: none;  /* Remove default border */
            }
            QMenuBar::item:selected {
                background-color: black;  /* Keep the background black on hover */
                border-bottom: 3px solid #8B0000;  /* Blood red bar under selected item */
                padding-bottom: 3px;  /* Ensure the bar sticks to the bottom */
            }
            QMenuBar::item:pressed {
                background-color: black;  /* Keep the background black on press */
                border-bottom: 3px solid #8B0000;  /* Blood red bar under pressed item */
            }
            QMenu {
                background-color: black;
                color: white;
            }
            QMenu::item:selected {
                background-color: #8B0000;
            }
        """)