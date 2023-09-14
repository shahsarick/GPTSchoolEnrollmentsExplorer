# GPTSchoolEnrollmentsExplorer
A project that explores the data for enrollment data in California as well as demographic county data.
Getting Started

1. Clone the repository and navigate into the project directory.
```
git clone <repository_url>
cd <project_directory>
```
2.  Rename the env.example file to .env and replace the placeholder with your OpenAI API key.
3.  Install the required Python packages.
   ```pip install -r requirements.txt```
4. run the ETL script to load data into the SQLite Database for the first time.
   ```python etl.py```
5. Start the Streamlit application.
   ```streamlit run sql_agent_class.py```

The application will open in your default web browser.

Project Contents

The project consists of several Python scripts and a requirements file:

- sql_agent_class.py: This is the main script that defines the SQLAgent class and the Streamlit application. The SQLAgent class uses the OpenAI API to generate SQL queries based on user input. It then creates a dataframe and execute python to generate charts. It is using an agent so queries can be a bit slow.

- etl.py: This script is used to load data into the SQLite database. It reads data from an Excel file and a CSV file, and loads the data into two tables in the database. Use the flags -demographics or -enrollments if you want to load that datafile into the database. Right now it is set to replace in case you get updated data.

- python_utils.py: This script contains utility functions for generating and formatting Python code as well as unzipping.

- prompt.py: This script defines the prompts used by the OpenAI API when the agent is generating SQL Queries.

- requirements.txt: This file lists the Python packages required for the project.

Key Functions

- SQLAgent.generate_query_response(): This method takes a user message as input and uses the OpenAI API to generate a SQL query. The query is then returned as part of the response.

- SQLAgent.extract_sql_code(): This static method extracts SQL code from a text string using regular expressions.

- SQLAgent.generate_dataframe(): This method executes a SQL query against the SQLite database and returns the result as a pandas DataFrame.

- SQLAgent.table_previews(): This method generates previews of the data in the two tables in the SQLite database in the streamlit sidebar.

- SQLAgent.main(): This method runs the main loop of the Streamlit application. It handles user input, calls the other methods to generate SQL queries and data previews, and updates the Streamlit interface.

- generate_code() and format_code() in python_utils.py: These functions are used to generate Python code using the OpenAI API and to format the generated code.

- load_data(), validate_schema(), county_demographics_load(), and enrollments_load() in etl.py: These functions are used to load data into the SQLite database.
