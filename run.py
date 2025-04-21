from app import create_app
from app.utils.scheduler import Scheduler
from datetime import datetime
import os

app = create_app()

# Configure the scheduler
app.config['SCRAPING_INTERVAL_MINUTES'] = int(os.getenv('SCRAPING_INTERVAL_MINUTES', 60))

# Initialize the scheduler
scheduler = Scheduler(app)

# Add context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    # Run the application
    port = int(os.getenv('PORT', 12000))
    app.run(host='0.0.0.0', port=port, debug=True)