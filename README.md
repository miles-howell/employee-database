# employee-database

# 🗂️ Employee Directory — Internal Company Tool

This project is a fully functional **employee directory web app** built with Django and designed for internal use by corporate teams. It integrates with legacy Microsoft Access databases and provides a fast, user-friendly UI for exploring employee data by department, hierarchy, and milestones.

---

## 🔒 License

This project is shared for portfolio and demonstration purposes only.

🛑 **Unauthorized commercial use, resale, or redistribution is strictly prohibited.**  
💼 If you're interested in using this project for business, client work, or integration into a product:

📩 **Reach out for a commercial license** at [miles@plannedpixel.com](mailto:miles@plannedpixel.com)

License: [Creative Commons Attribution-NonCommercial 4.0](http://creativecommons.org/licenses/by-nc/4.0/)


## 🔧 Tech Stack

- **Backend:** Python, Django
- **Database:** Microsoft Access (.accdb), SQLite (demo only)
- **Frontend:** HTML, CSS (custom themes), JavaScript
- **Exporting:** CSV generation via Django management command
- **Hosting (live version):** Internal network (not public)

---

## 🧩 Features

- **Department-Based Sorting**  
  Employees are organized by department and sorted visually by **managerial hierarchy**.

- **Manager Highlighting**  
  Department heads and supervisors are visually identified using **card watermarks**.

- **Birthday & Anniversary Highlights**  
  The homepage displays all employees with **milestones this month**, with special emphasis on **today’s birthdays or anniversaries**.

- **Advanced Search Page**  
  Powerful multi-criteria search including department, title, hire date, and supervisor status.

- **CSV Export**  
  Users can export custom search results as a downloadable CSV file.

---

## 🚧 Data Privacy Notice

**⚠️ Warning:** This project was originally built using real employee data.  
To protect privacy, **all sensitive data must be removed** before sharing, cloning, or deploying this project outside the internal network.

Use the following command to safely clear the database:

```bash
python manage.py flush
