# Discgolf Tournament Checker

## Overview

This project scrapes disc golf tournament data from [DiscgolfMetrix](https://discgolfmetrix.com), caches the results in a local SQLite database, and presents the information via a Telegram bot interface. A future user interface (UI) is planned.

## Features

- Scrapes tournament and event data from DiscgolfMetrix
- Stores/caches data in a local SQLite database
- Logging of scraping activity to `application.log`
- Telegram bot for querying and managing tournament data
- Modular code for future UI integration

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/discgolfscraper.git
   cd discgolfscraper
   ```

2. **Install dependencies:**
   ```
   pip install requests beautifulsoup4 python-telegram-bot python-dotenv
   ```

3. **Configure environment variables:**
   - Create a `.env.local` file in the project root.
   - Add your Telegram bot token:
     ```
     TGBOT_KEY=your-telegram-bot-token
     ```

4. **Run the application:**
   ```
   python main.py
   ```

## Usage

- The script will fetch event data for specified courses and log details to `application.log`.
- Use the Telegram bot to interact with the database:
  - `/start` — Start the bot
  - `/new_course` — Add a new course
  - `/course <name>` — Get details for a specific course
  - `/list_courses` — List all cached courses

## Roadmap

- Add a user interface for browsing cached tournament data
- Support for multiple courses and advanced filtering
- Notification features for upcoming events
- Improved error handling and reporting

## Contributing

Pull requests and suggestions are welcome!

## License

MIT License
