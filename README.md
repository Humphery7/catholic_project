# catholic_project


# Saint of the Day Project

## Overview

The **Saint of the Day** project is designed to provide users with information about saints. It utilizes web scraping with Selenium to gather data about saints and updates a PostgreSQL database with the obtained information. The project also features a Flask API deployed on Render, allowing users to access saint data via HTTP requests. Additionally, a public PostgreSQL database on Render is utilized to ensure accessibility from various devices.

## Features

- **Web Scraping:** Utilizes Selenium to scrape data about saints from online sources.
- **Database Update:** Utilizes psycopg2 to update a PostgreSQL database with saint information.
- **Flask API:** Provides a RESTful API with endpoints to fetch saint data.
- **Render Deployment:** The API is deployed on Render for accessibility.
- **MongoDB Database:** Tha database is deployed on MongoDB Atlas

## Getting Started

### Prerequisites

- Python 3.9
- [Selenium](https://selenium-python.readthedocs.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Psycopg2](https://www.psycopg.org/)
- [Render](https://render.com/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/saint-of-the-day.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environmental variables:

   Create a `.env` file and add the following:

   ```env
   DATABASE_URL=your_postgres_database_url
   API_KEY=your_api_key
   ```

### Usage

1. Run the web scraping and database update script:

   ```bash
   python scrape_and_update.py
   ```

2. Start the Flask API:

   ```bash
   python app.py
   ```

   The API will be accessible at `https://flask-api-catholic-project.onrender.com`.

3. Access the API endpoints:

   - `/saints`: Get all saints' records.
   - `/saints/today`: Get the saint of the day.
   - `/saints/date/{date}`: Get the saint for a specific date.

## Deployment

1. Deploy the Flask API on Render.

2. Create MongoDB Database and deploy with MongoDB Atlas.

## Contributing

Contributions are welcome! Please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project has no LICENSE.

## Acknowledgments

- Special thanks to [Render](https://render.com/) for hosting services.

## Contact

For inquiries, please contact [humpheryufuoma@gmail.com]
