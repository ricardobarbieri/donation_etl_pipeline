# Donation ETL Pipeline - GoFundMe Simulation (Version 1.0 - Testing Phase)

Welcome to the **Donation ETL Pipeline**, a project in its **testing phase** (version 1.0) that simulates an ETL (Extract, Transform, Load) data pipeline inspired by GoFundMe's data centralization process. This pipeline collects, processes, and analyzes donation data, providing an interactive graphical user interface (GUI) to run the pipeline, visualize results, and export data. Our goal is to create a robust, accessible, and user-friendly tool, particularly for those new to data engineering, with features like interactive charts and accessibility support for visually impaired users.

> **Note**: This project is in the testing phase (version 1.0). We are actively working on adding more features, integrating real APIs, and improving scalability. Your contributions and feedback are greatly appreciated!

## 📋 About the Project

The **Donation ETL Pipeline** is a Python application that mimics the data flow of a crowdfunding platform like GoFundMe. It extracts donation data (from a local JSON file or, in future updates, public APIs), transforms it (cleaning and aggregating metrics), and loads it into a database (SQLite by default, with optional PostgreSQL support). The GUI, built with **Streamlit**, allows users to execute the pipeline, view tables and interactive charts, and export results, making it an excellent tool for learning and experimenting with data pipelines.

### Key Features
- **Complete ETL Pipeline**:
  - **Extract**: Retrieves donation data from a local JSON file or (in development) public APIs.
  - **Transform**: Cleans data, removes duplicates, and computes metrics like total donations per campaign.
  - **Load**: Stores data in SQLite (default) or PostgreSQL (optional).
- **Interactive GUI**:
  - Built with Streamlit, featuring dynamic tables, Plotly charts, and buttons to run the pipeline and export data.
  - Audible feedback via `pyttsx3` for accessibility to visually impaired users.
- **Visualizations**: Interactive bar charts displaying total donations by campaign.
- **Data Export**: Supports exporting processed data as CSV or JSON files.
- **Logging**: Detailed logs of all pipeline steps saved to `pipeline.log`.
- **Automation**: Pipeline scheduling with the `schedule` library (GUI integration in progress).
- **Accessibility**: Designed for compatibility with screen readers (e.g., NVDA, VoiceOver) with high-contrast text and clear labels.

### Technologies Used
- **Python 3.x**: Core programming language.
- **Streamlit**: Interactive web-based GUI.
- **Pandas**: Data manipulation and transformation.
- **SQLite** and **PostgreSQL**: Databases for data storage.
- **Plotly**: Interactive visualizations.
- **pyttsx3**: Audible feedback for accessibility.
- **schedule**: Task scheduling.
- **logging**: Activity logging.

## 🎯 Project Goals

Inspired by GoFundMe's data pipeline for centralizing and analyzing donation data, this project serves as a practical learning tool for:
- Understanding ETL pipelines and data engineering concepts.
- Exploring modern Python libraries like Streamlit, Pandas, and Plotly.
- Building accessible applications with screen reader support and audible feedback.
- Experimenting with local and cloud-ready databases (SQLite, PostgreSQL).

As version 1.0 in the testing phase, it provides a solid foundation for further development, such as real API integrations and cloud-based storage.
