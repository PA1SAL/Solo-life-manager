import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTextEdit, QMainWindow
from PyQt5.QtGui import QPixmap

# Dictionary of ingredients and corresponding meals
ingredient_to_meal = {
    "chicken": "Chicken Stir Fry",
    "beef": "Beef Tacos",
    "shrimp": "Shrimp Scampi",
    "pasta": "Spaghetti Carbonara",
    "rice": "Vegetable Fried Rice",
    "potato": "Potato Soup",
    "tomato": "Caprese Salad",
    "lettuce": "Chicken Caesar Salad"
}

class RecentSuggestionsWindow(QMainWindow):
    def __init__(self, recent_suggestions):
        super().__init__()
        self.setWindowTitle("Recent Suggestions")
        self.setGeometry(400, 200, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.recent_suggestions_display = QTextEdit()
        self.recent_suggestions_display.setReadOnly(True)
        self.recent_suggestions_display.setText("\n".join(recent_suggestions))

        self.layout.addWidget(self.recent_suggestions_display)

class LikedDishesWindow(QMainWindow):
    def __init__(self, liked_dishes):
        super().__init__()
        self.setWindowTitle("Liked Dishes")
        self.setGeometry(400, 200, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.liked_dishes_display = QTextEdit()
        self.liked_dishes_display.setReadOnly(True)
        self.liked_dishes_display.setText("\n".join(liked_dishes))

        self.layout.addWidget(self.liked_dishes_display)

class MealSuggestionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.recent_suggestions = []
        self.liked_dishes = []
        self.initUI()
        self.create_database()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle("Meal Suggestion App")
        self.setGeometry(100, 100, 1350, 982)

        # Background image
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("bg.jpg"))  # Change "background.jpg" to your image file
        self.background_label.setGeometry(0, 0, 1350, 982)

        # Input field
        self.ingredients_label = QLabel("Enter ingredients separated by comma:", self)
        self.ingredients_label.setStyleSheet("color: black; font-size: 40px")
        self.ingredients_entry = QLineEdit(self)
        self.ingredients_entry.setStyleSheet("color: black; font-size: 16px")
        self.analyze_button = QPushButton("Analyze Ingredients", self)
        self.analyze_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px")
        self.analyze_button.clicked.connect(self.analyzeIngredients)

        # Buttons for recent suggestions and liked dishes
        self.recent_suggestions_button = QPushButton("Recent Suggestions", self)
        self.recent_suggestions_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 16px")
        self.recent_suggestions_button.clicked.connect(self.showRecentSuggestions)
        self.liked_dishes_button = QPushButton("Liked Dishes", self)
        self.liked_dishes_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 16px")
        self.liked_dishes_button.clicked.connect(self.showLikedDishes)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.ingredients_entry)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.recent_suggestions_button)
        layout.addWidget(self.liked_dishes_button)
        self.setLayout(layout)

    def create_database(self):
        try:
            conn = sqlite3.connect("meal_suggestion.db")
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS recent_suggestions (meal TEXT)''')
            c.execute('''CREATE TABLE IF NOT EXISTS liked_dishes (dish TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error creating database:", e)

    def analyzeIngredients(self):
        ingredients = self.ingredients_entry.text().lower().split(",")
        matching_meals = [ingredient_to_meal[ingredient] for ingredient in ingredients if ingredient in ingredient_to_meal]

        if matching_meals:
            self.recent_suggestions = matching_meals + self.recent_suggestions[:2]  # Store up to 3 recent suggestions
            self.save_to_database(matching_meals, "recent_suggestions")
        else:
            QMessageBox.information(self, "Meal Suggestion", "Sorry, no matching meals found.")

    def save_to_database(self, data, table_name):
        try:
            conn = sqlite3.connect("meal_suggestion.db")
            c = conn.cursor()
            for item in data:
                c.execute(f"INSERT INTO {table_name} VALUES (?)", (item,))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error saving to database:", e)

    def load_from_database(self, table_name):
        try:
            conn = sqlite3.connect("meal_suggestion.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table_name}")
            data = c.fetchall()
            conn.close()
            return [row[0] for row in data]
        except Exception as e:
            print("Error loading from database:", e)
            return []

    def showRecentSuggestions(self):
        recent_suggestions = self.load_from_database("recent_suggestions")
        recent_suggestions_window = RecentSuggestionsWindow(recent_suggestions)
        recent_suggestions_window.show()

    def showLikedDishes(self):
        liked_dishes = self.load_from_database("liked_dishes")
        liked_dishes_window = LikedDishesWindow(liked_dishes)
        liked_dishes_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MealSuggestionApp()
    window.show()
    sys.exit(app.exec_())
