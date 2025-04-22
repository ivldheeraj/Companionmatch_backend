# Project Setup and Execution Guide

This document provides step-by-step instructions for setting up and running the application.

## Prerequisites

Before starting, make sure you have:
- Python installed (version specified in requirements.txt)
- Access to your database server (as configured in DB_config)

## Installation

1. Clone this repository to your local machine
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, verify your database configuration in the DB_config file. Ensure that:
- Database connection details are correct
- You have proper permissions to create/modify tables
- The database server is running and accessible

## Seeding the Database

The application requires initial data to be loaded before running. Follow these steps in order:

1. First, run the seed data script:

```bash
python seed_data.py
```

2. Next, run the questionnaire seeding script:

```bash
python seed_questionnaire.py
```

These scripts will populate your database with the necessary initial data required for the application to function properly.

## Running the Application

After completing the above steps, you can start the application by running:

```bash
python main.py
```

## Troubleshooting

If you encounter any issues:
- Verify that all dependencies in requirements.txt are installed
- Check that your database configuration is correct
- Ensure that the seed scripts completed successfully without errors
- Check application logs for specific error messages

## Additional Information

- The seed_data.py script populates the database with essential application data
- The seed_questionnaire.py script loads the questionnaire templates and related content
- Both scripts must be run successfully before starting the main application

## Contact

If you encounter persistent issues, please contact the me.
