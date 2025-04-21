# News Agent

A news aggregation website that scrapes, rephrases, translates, and publishes news content in Urdu with SEO optimization. This application automatically collects news from various international and national sources, processes it using NLP techniques, translates it to Urdu, and presents it in a user-friendly bilingual interface.

![News Agent Screenshot](app/static/images/placeholder.jpg)

## Features

- **Automated News Scraping**: Collects news from reputable international and national sources
- **Content Processing**: Rephrases content to avoid plagiarism using NLP techniques
- **Urdu Translation**: Translates all content to Urdu for the local audience
- **SEO Optimization**: Automatically generates meta tags, descriptions, and keywords
- **Bilingual Interface**: Switch between English and Urdu with a single click
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Category-based Navigation**: Browse news by categories (World, Business, Technology, etc.)
- **Search Functionality**: Find news articles by keywords
- **API Access**: RESTful API endpoints for accessing news data programmatically

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **NLP**: NLTK, spaCy for text processing and analysis
- **Translation**: Google Translate API for English to Urdu translation
- **Scheduling**: APScheduler for periodic news scraping
- **Web Scraping**: BeautifulSoup4, Requests, Selenium (for JavaScript-heavy sites)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-agent.git
   cd news-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download NLTK data:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=sqlite:///news_agent.db
   SECRET_KEY=your_secret_key_change_in_production
   SCRAPING_INTERVAL_MINUTES=60
   PORT=12000
   ```

6. Initialize the database with sample data:
   ```bash
   python init_db.py
   ```

## Usage

1. Run the application:
   ```bash
   python run.py
   ```

2. Access the website at `http://localhost:12000`

3. Features you can try:
   - Switch between English and Urdu using the language dropdown
   - Browse news by categories
   - Read full articles
   - Search for specific news
   - View the latest news on the homepage

## Project Structure

```
news-agent/
├── app/                           # Main application package
│   ├── static/                    # Static files
│   │   ├── css/                   # CSS stylesheets
│   │   ├── js/                    # JavaScript files
│   │   └── images/                # Image assets
│   ├── templates/                 # HTML templates
│   │   ├── base.html             # Base template with common elements
│   │   ├── index.html            # Homepage template
│   │   ├── article.html          # Single article template
│   │   ├── category.html         # Category page template
│   │   └── search.html           # Search results template
│   ├── models/                    # Database models
│   │   ├── __init__.py
│   │   └── news.py               # News-related models
│   ├── controllers/               # Route controllers
│   │   ├── __init__.py
│   │   ├── main.py               # Main web routes
│   │   └── api.py                # API endpoints
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   ├── text.py               # Text processing utilities
│   │   └── scheduler.py          # Scheduling utilities
│   ├── scrapers/                  # News scraping modules
│   │   ├── __init__.py
│   │   ├── base.py               # Base scraper class
│   │   ├── bbc.py                # BBC News scraper
│   │   └── dawn.py               # Dawn News scraper
│   ├── nlp/                       # Natural Language Processing
│   │   ├── __init__.py
│   │   └── processor.py          # Text processing and rephrasing
│   ├── translations/              # Translation modules
│   │   ├── __init__.py
│   │   └── translator.py         # English to Urdu translator
│   ├── seo/                       # SEO optimization
│   │   ├── __init__.py
│   │   └── optimizer.py          # SEO metadata generator
│   └── __init__.py                # Application factory
├── migrations/                    # Database migrations
├── .env                           # Environment variables
├── requirements.txt               # Project dependencies
├── init_db.py                     # Database initialization script
├── run.py                         # Application entry point
└── README.md                      # Project documentation
```

## How It Works

1. **News Scraping**: The application periodically scrapes news from configured sources using the scrapers in `app/scrapers/`.
2. **Content Processing**: Raw content is processed using NLP techniques in `app/nlp/processor.py` to rephrase and summarize.
3. **Translation**: The processed content is translated to Urdu using `app/translations/translator.py`.
4. **SEO Optimization**: Metadata is generated for each article using `app/seo/optimizer.py`.
5. **Storage**: All content is stored in the database using SQLAlchemy models.
6. **Presentation**: The web interface displays content in both English and Urdu with language switching capability.

## API Endpoints

The application provides a RESTful API for accessing news data programmatically:

- `GET /api/news` - Get latest news articles
  - Query parameters:
    - `page`: Page number (default: 1)
    - `per_page`: Items per page (default: 10)
    - `category`: Filter by category slug
    - `source`: Filter by source ID
    - `q`: Search query

- `GET /api/news/<slug>` - Get a specific news article by its slug

- `GET /api/categories` - Get all categories
  - Returns a list of all news categories with their IDs and slugs

- `GET /api/sources` - Get all sources
  - Returns a list of all news sources with their IDs and URLs

## Customization

### Adding New News Sources

To add a new news source:

1. Create a new scraper in `app/scrapers/` that inherits from `BaseScraper`
2. Implement the required methods: `fetch_articles()` and `parse_article()`
3. Register the scraper in `app/scrapers/__init__.py`

### Modifying the Frontend

The frontend uses Bootstrap 5 for styling and is fully responsive. To customize:

1. Edit the templates in `app/templates/`
2. Modify the CSS in `app/static/css/style.css`
3. Update JavaScript functionality in `app/static/js/main.js`

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style of the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [NLTK](https://www.nltk.org/) - Natural Language Processing
- [Google Translate API](https://cloud.google.com/translate) - Translation services
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping library