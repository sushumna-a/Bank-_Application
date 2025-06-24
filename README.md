# Banking Application using Docker
# Bank App

A simple web-based banking application built with Flask and SQLite, containerized using Docker.

---

## Objective

The objective of this project is to provide a lightweight, easy-to-use web application for basic banking operations, including account management, balance inquiry, deposits, withdrawals, and viewing transaction statements. The application demonstrates how to build and containerize a Python Flask app with persistent data storage using SQLite.

---

## Tech Stacks

- **Backend Framework:** Flask (Python)
- **Database:** SQLite (local file-based)
- **Containerization:** Docker
- **Dependency Management:** requirements.txt (pip)
- **Python Version:** 3.10 (Docker base image)

---

## Steps Included

1. **Project Structure**
   - `app.py`: Main Flask application with all banking routes and database logic.
   - `requirements.txt`: Lists Python dependencies (Flask).
   - `Dockerfile`: Instructions to build and run the application inside a Docker container.

2. **Database Initialization**
   - On first run, the app initializes an SQLite database (`bank.db`) with tables for accounts and transactions.

3. **Core Features**
   - **Create Account:** Add a new bank account.
   - **Check Balance:** View the balance for a given account.
   - **Deposit:** Add funds to an account.
   - **Withdraw:** Remove funds from an account, with insufficient balance check.
   - **View Statement:** Display all transactions for an account.

4. **Dockerization**
   - The application is containerized using a Dockerfile:
     - Uses the official Python 3.10 image.
     - Sets `/app` as the working directory.
     - Installs dependencies from `requirements.txt`.
     - Runs the Flask app using `python app.py`.

5. **How to Run**
   - **Build the Docker image:**
     ```
     docker build -t flask-bank-app .
     ```
   - **Run the Docker container:**
     ```
     docker run -p 5000:5000 flask-bank-app
     ```
   - Access the app at `http://localhost:5000` in your browser.

---

## Key Insights

- **Simplicity:** The project demonstrates how to build a minimal yet functional web app with Flask and SQLite.
- **Containerization:** Docker ensures consistent deployment across environments.
- **Extensibility:** The codebase can be extended to support user authentication, more complex transaction types, or integration with external databases.
- **Educational Value:** Serves as a practical example for beginners learning about REST APIs, web development, and Docker.

---

## Additional Notes

- **Persistence:** The SQLite database is stored inside the container; to persist data across container restarts, consider mounting a Docker volume.
- **Security:** This is a demo app and does not implement authentication or input validation for production use.
- **Customization:** You can add more dependencies to `requirements.txt` and modify `app.py` for additional features.
- **Port Configuration:** The app runs on port 5000 by default; you can map it to any local port using Docker's `-p` option.

---

## Getting Started

1. Clone the repository:
 git clone <repository_url>
 cd <repository_folder>
