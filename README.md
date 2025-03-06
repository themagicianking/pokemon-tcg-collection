# Pokemon TCG Collection Builder

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

This is an app built to fulfil python-centric knowledge checks for Techtonica.

## Installation

1. Clone the repo to your local machine.
2. Navigate into the project directory and run ``source .venv/bin/activate`` to activate your virtual environment.
3. Use ``pip install -r requirements.txt`` to install all the necessary libraries.
4. Run ``python app.py`` to activate the server and navigate to the local port the app is running on (this will ensure database creation on startup).

## Usage

Use the search fields to find a card whose description matches a certain word and whose name matches a certain word. The chart at the bottom of the page displays the type breakdown of the cards in your search results.

## Testing

This app currently does not have any associated testing.

## To Do

To do list items will go here. As of right now my priority is to complete the current knowledge check, then work backwards through previous ones.

Current requirement:

- [x] Develop a minimum of two complex search queries using full-text search libraries
- [x] Ensure your README includes set up instructions, description, and a visual of your application in action including your database
- Complete 1 of the 2 tasks below:
  - [x] Display a simple data visualization
  - [ ] Add support for bulk data operations (import/export)
        Consolidate your work from KC1 - KC6 into a single application

## Reference

This application will utilize [The Pokemon TCG API](https://pokemontcg.io/).
