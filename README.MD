# HH Bot

## Introduction
This is a bot to automatically raise your resumes on https://hh.ru/ **absolutely free** of charge.  

This project consists of a Python application designed to interact with web pages using the Selenium WebDriver. The application is containerized using Docker and orchestrated with Docker Compose.

## Components

### Main Application

#### Python Files

- `main.py`: The main executable file that initializes the logger and starts the application.
- `worker.py`: Contains classes and functions to interact with web pages using Selenium.
- `config.py`, `strings.py`: Configuration and resource files.

#### Environment Variables

The `.env` file contains the following environment variables that need to be configured:  
You can add any number of `RESUME_LINKS`, just like `RESUME_FIRST`.  
- `HH_LOGIN`: Your login information.
- `HH_PASSWORD`: Your password.
- `RESUME_FIRST`: URL of the first resume (e.g., `https://hh.ru/resume/1234c2fdff0bf808dd0039ed1f656276343065`).
- `TZ`: Timezone setting (e.g., `'Europe/Moscow'`).
- `USER_AGENT`: User-agent string for the web requests (can check yours here: https://my-user-agent.com/).

### Docker Configuration

#### Dockerfile

Defines the Docker image with Python 3.11 and includes the Chromium browser and ChromeDriver for Selenium.

#### Docker Compose

- `docker-compose.yml`: Orchestrates the main application service and an Ofelia scheduling service.
- The main service (`hh_upper`) builds from the Dockerfile and uses the `.env` file for environment variables.
- Ofelia is used to schedule the running of the application every 4 hours and 10 minutes.



## Usage
### Docker compose 

1. Clone the repository.
2. Configure the `.env` file with the appropriate values.
3. Start the services using `docker compose up`.

### Direct Execution

The application can be executed by running the main Python script:

```bash
python main.py
```

## Logging

Logging is configured in `main.py` and outputs to both the console and a file named `selenium_actions.log`.  
When running with docker compose, the logs of the first run will be in the code container, and all subsequent scheduled tasks will be in the ofelia container.
## Dependencies

- Selenium WebDriver: For browser automation.
- Tenacity: For retry logic.
- python-dotenv: For managing environment variables.

## Conclusion

This README provides an overview of the project's structure and functionality, including details on environment variables and Docker Compose orchestration. For specific details, please refer to the code and comments within the source files.
