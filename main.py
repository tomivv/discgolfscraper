import datetime
import logging
from bot.main import run_bot
from database import init_database

logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info(f"Started app at {datetime.datetime.now(datetime.timezone.utc)}")
    init_database()
    run_bot()
    
if __name__ == '__main__':
    main()