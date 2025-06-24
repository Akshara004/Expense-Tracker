# 💰 Budget Buddy - Expense Tracker Web App

A clean, full-stack **Expense Tracker** built using Python and Flask that helps users log expenses, visualize spending patterns, and stay on top of their monthly budget goals. Includes secure authentication, dark mode, charts, and a responsive landing page.

---

## 🚀 Features

- ✅ User Registration & Login (Flask-Login, hashed passwords)
- ✅ Add, view, and categorize expenses
- ✅ Category-wise expense summaries (monthly)
- ✅ Interactive Pie Chart using Chart.js
- ✅ Responsive Landing Page with CTA
- ✅ Flash messages and error handling
- ✅ Dark Mode toggle (with localStorage)
- ✅ Mobile-friendly with Bootstrap 5
- ✅ Clean UI with navbar and footer

---

## 🛠 Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2, Chart.js
- **Database**: SQLite (for development)

---

## 🧠 Key Concepts

- **User-Expense Relationship**: One-to-many via SQLAlchemy foreign keys
- **Chart Integration**: Jinja2 passes category totals → JavaScript renders pie chart
- **Dark Mode**: JavaScript + localStorage + CSS toggling
- **Blueprints**: Modular organization of auth, dashboard, and summary views

---


## 📷 Screenshots

### 🏠 Landing Page
![Landing Page](assets/landing.png)

### 💻 Dashboard
![Dashboard](assets/dashboard.png)

### 📊 Summary Charts
![Summary](assets/summary_chart.png)

---


> "Track smarter. Spend wiser. Welcome to Budget Buddy!"
