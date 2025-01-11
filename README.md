# Text-Analysis-Pipeline

A comprehensive pipeline for scraping web articles and performing detailed text analysis, including sentiment analysis, readability metrics, and content complexity measurements.

## Features

- Web scraping of articles using Selenium with Brave Browser
- Text preprocessing and cleaning
- Sentiment analysis using VADER
- Readability metrics calculation (Fog Index)
- Content complexity analysis
- Personal pronouns tracking
- Excel output with multiple metrics

## Requirements

### Python Packages
```bash
pip install -r requirements.txt
```

### External Software
- Brave Browser
- ChromeDriver (matching your Brave browser version)

### NLTK Data
The following NLTK data will be downloaded automatically:
- stopwords
- punkt

## Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/Text-Analysis-Pipeline.git
cd Text-Analysis-Pipeline
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Update paths in both scripts:
- Input Excel file path
- Output folder path
- ChromeDriver path
- Brave Browser path

## Usage

1. Prepare input Excel file with URLs in the format:
   - Column 1: URL_ID
   - Column 2: URL

2. Run the web scraper:
```bash
python scraper.py
```

3. Run the text analyzer:
```bash
python analyzer.py
```

## Output Metrics

The analyzer generates an Excel file with the following metrics:
- Positive/Negative Sentiment Scores
- Polarity Score
- Subjectivity Score
- Average Sentence Length
- Percentage of Complex Words
- Fog Index
- Word Count
- Complex Word Count
- Syllables Per Word
- Personal Pronouns Count
- Average Word Length

## File Structure
```
Text-Analysis-Pipeline/
├── scraper.py         # Web scraping script
├── analyzer.py        # Text analysis script
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
