# IntelliShop

IntelliShop is a modern web application that provides an intuitive e-commerce platform. Built with Django and MongoDB, it offers the foundation for online shopping experiences.

## Quick Start Guide

### Setting Up Environment Variables

Before running the application, you need to set up your environment variables:

1. Create a `.env` file in the project root directory with the following template:
   ```
   # MongoDB Configuration
   MONGODB_URI=mongodb+srv://username:password@yourcluster.mongodb.net/?retryWrites=true&w=majority
   MONGODB_NAME=YourDatabaseName

   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

2. Replace the placeholder values with your actual MongoDB credentials and desired settings.

### Running the Application

The application includes a build script that handles setup and execution:

./build.sh

Access the application at http://localhost:8000

## Features

- Product catalog with categories
- MongoDB integration for scalable data storage
- Responsive design for desktop and mobile devices
- User authentication and account management

## Technologies Used

- **Backend**: Django, Python 3
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: WSL (Windows Subsystem for Linux)

## Prerequisites

- Python 3.8 or higher
- Access to a MongoDB database (Atlas URI)
- Git

## Detailed Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/intellishop.git
cd intellishop
```

### 2. Environment Setup

Follow the "Setting Up Environment Variables" section above to create your `.env` file.

### 3. Run the Build Script

Follow the "Running the Application" section above to execute the build script.

## Project Structure

```
intellishop/
├── mysite/                  # Django project directory
│   ├── intellishop/         # Main application
│   │   ├── models/          # MongoDB models
│   │   ├── utils/           # Utility functions
│   │   ├── management/      # Custom management commands
│   │   ├── views.py         # View controllers
│   │   └── ...
│   ├── manage.py            # Django management script
│   └── ...
├── build.sh                 # Setup and run script
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (create this)
```
