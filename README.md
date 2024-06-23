# My Planner

Welcome to **My Planner**, your go-to solution for effective task management, focused work sessions, and weekly planning. This dynamic web application is the result of the final project for the CS50 course, bringing together practical programming concepts for a seamless user experience.

#### Video Demo:  <https://youtu.be/nI29XWN2TaI>

## Features

- **Task Management:** Easily add, delete, and mark tasks as done or not done.
- **Weekly Planner:** View and organize your tasks on a weekly basis.
- **Countdown Timer:** Set a custom countdown timer to stay focused and productive.

# Project File Structure

## Files:

- **README.md:**
  - Project documentation providing an overview, usage instructions, and other relevant details.

- **app.py:**
  - Main Flask application file containing the server-side logic, route definitions, and database interactions.

- **helpers.py:**
  - Python module containing helper functions used in the main application (`app.py`).

## Static:

- **style_daily.css:**
  - CSS file specifically for styling the Add Tasks page.

- **weekly.css:**
  - CSS file specifically for styling Weekly Planner page.

- **countdown.css:**
  - CSS file specifically for styling the countdown timer page.
  - Adds styles to enhance the visual appeal of the countdown page.

## Templates:

- **layout.html:**
  - Base HTML template providing the overall structure for other templates.
  - Includes the Bootstrap framework, favicon, navigation bar, and a container for the main content.

- **index.html:**
  - Home page template (`/` route).
  - Displays a list of tasks.

- **add.html:**
  - Template for the "Add Task" page (`/add` route).
  - Allows users to add new tasks for a specific date.

- **countdown.html:**
  - Template for the countdown timer page (`/countdown` route).
  - Allows users to set a custom countdown timer.

- **login.html:**
  - Template for the login page (`/login` route).
  - Provides a form for users to enter their login credentials.

- **register.html:**
  - Template for the registration page (`/register` route).
  - Includes a form for users to register with a new username and password.

- **weekly.html:**
  - Template for the weekly planner page (`/weekly` route).
  - Displays a list of tasks organized by day of the week.

- **tasks.js:**
  - JavaScript file for managing tasks.
  - Handles user input for tasks and updates the day name.

- **countdown.js:**
  - JavaScript file for the countdown timer.
  - Implements the countdown timer functionality and updates the visual representation.

## Other:

- **LICENSE:**
  - License file specifying the terms under which the project is distributed.

- **requirements.txt:**
  - File listing the dependencies required to run the application.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [CS50 Library](https://cs50.readthedocs.io/library/python/)
- [SQLite](https://www.sqlite.org/)

### Run the website
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nourshoaib/planner.git

2. **Navigate to the project directory:**
   ```bash
   cd planner

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Run the Flask application:**
   ```bash
   flask run

## Usage

1. **Register or log in to access your personalized home page.**

   Upon visiting the application, users will have the option to register for a new account or log in if they already have one. This step is crucial for accessing a personalized home page where tasks and planning details are stored securely.

2. **Navigate to the Add Task page:**

   Once logged in, users can click on the "Add Task" option to access a dedicated page for adding tasks. This feature allows users to input task details for a specific date, ensuring a well-organized and time-sensitive approach to task management.

3. **Explore the Weekly Planner:**

   Users can easily view and organize their tasks on a weekly basis. The Weekly Planner provides an overview of tasks scheduled for each day, facilitating efficient planning and allocation of time.

4. **Countdown Timer:**

   The Countdown Timer feature allows users to set a custom countdown for focused and productive work sessions. By specifying the desired duration, users can stay on track and accomplish tasks within a defined timeframe.

## Contributing

1. **Fork the repository.**

3. **Create a new branch:**
   ```bash
   git checkout -b feature-name
4. **Make your changes and commit them:**
   ```bash
   git commit -m 'Add new feature'

5. **Push to the branch:**
   ```bash
   git push origin feature-name

6. **Submit a pull request:**
   >After pushing your changes to your forked repository, navigate to the original repository on GitHub. You should see a prompt to create a pull request. Follow the instructions to submit your changes for review.

### Acknowledgments
- [CS50](https://cs50.harvard.edu/): Introduction to Computer Science course at Harvard University.

### License
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
