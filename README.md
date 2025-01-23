# FinanceBros Project

This repository is for the FinanceBros project. The project is designed to empower users to make strategic financial decisions by providing insights derived from top traders, political influencers, and comprehensive market analyses. It also includes an AI-powered chatbot that provides personalized financial advice catered to the users financial expertise.

[Project video (YouTube)](https://www.youtube.com/watch?v=h0k6nTx9WQ8)

[Project video (Drive)](https://drive.google.com/file/d/1xEvD-DX-1S-J9cZIN2m7kjXQMQX093R-/view)

Note: The videos have mislabeled names. The one labeled "Justin Iverson" is actually Bryan Guen, and the one labeled "Bryan Guen" is actually Justin Iverson.

## Description

The FinanceBros project is a social media platform for finance enthusiasts that aims to help users make informed financial decisions. By offering detailed performance metrics and strategies from leading financial figures, the platform provides a unique perspective on investment opportunities. Users can stay informed with real-time data and trends, receive personalized recommendations, and follow the activities of influential traders. This platform is designed to guide both novice and experienced investors through the complexities of the financial market. Additionally, a financial consultant chatbot feature is available and is customized to each users needs.

## Getting Started

### Dependencies

* Python 3.8 or higher
* Flask 2.0.1
* mySQL Ver 14.14
* OpenAI API Key
* Streamlit 1.0.0
* Windows 10 or macOS 10.15 Catalina
* Docker and Docker Compose
* Datagrip

### Installing

* Clone the repository from GitHub
* Set up a virtual environment and activate it
* Install the required dependencies:
  `pip install -r requirements.txt`
* Set up the mySQL database and run the provided SQL script
* Copy and rename `.env.template` to `.env` and create a password
* Add your OpenAI API key to the Streamlit secrets:
  `echo "[openai]\\nopenai_api_key=your_api_key_here" > .streamlit/secrets.toml`
  ###### Note: The chatbot feature will not work without a valid openAI API key

### Docker and MYSQL

* Setup connection in MySQL
  `port = your_port`
  `user = root`
  `password = your_password`
* Run Docker containers
  In the virutal environment terminal `docker compose up -d`
  
### Executing program

* Start the Flask development server:
  `flask run`
* Start the Streamlit application
* Access the application by navigating to `http://127.0.0.1:8501/` in your web browser.

## Help

For common issues:
* Ensure that MySQL is correctly installed and the database is running.
* If you encounter issues with the OpenAI API, ensure that your API key is correctly set in the Streamlit secrets file. This secrets.toml file should be next to the config.toml file.
* Check the Flask and Streamlit documentation for more details on error messages.

`flask --help`
`streamlit --help`

* Rerun docker container when encountering docker issues.

In terminal run `docker compose down` and `docker compose up -d`

## Authors

* Bryan Guen
* Ethan Xin  
* Eitan Berenfeld  
* Justin Iverson  
* Jared Mar  
* Daniel Klevak  

## Version History

* 0.3
    * Added AI-powered financial consultation chatbot feature
* 0.2
    * Various bug fixes and optimizations
* 0.1
    * Initial Release

## Acknowledgments

* [Mark Fontenot Project Template](https://github.com/NEU-CS3200/24su-3200-project-template)
* [OpenAI API + Streamlit Template](https://github.com/streamlit/llm-examples)

###### In the future, we are planning on building a stock prediction model based on the given data.

<sub> Disclaimer #1: The data being used for the project as of now is mock data. In the future, we are planning on making the transition away from mock data and instead using real publicly available financial data.</sub>

<sub> Disclaimer #2: The information provided on this platform is for informational purposes only and should not be construed as financial advice. We are not licensed financial advisors. Any investment decisions or financial strategies discussed here should be considered with caution and consulted with a qualified financial advisor. Your financial situation is unique, and it is important to seek personalized advice before making any financial decisions.</sub>
