from flask import Flask, request

import google.generativeai as genai  # Import Google Gemini API

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Google AI Studio API Client
GOOGLE_API_KEY = "AIzaSyA5nMC2wlHX9rvtFIhwpdxu5HWXmMHLsbI"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to label output
def output_label(n):
    return "Not Fake News" if n == 1 else "Fake News"

# Function to check news validity using Google Gemini AI
def check_fact(news_statement):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-002")  # Use latest Gemini AI model
        response = model.generate_content(f"Fact-check this statement: '{news_statement}'. Is it true or false?")

        # Check if response is valid
        if response and hasattr(response, "text"):
            result = response.text.strip().lower()

            # Check if AI indicates the news is true or false
            if "true" in result:
                return 1  # Not Fake News
            elif "false" in result:
                return 0  # Fake News
            else:
                return "Uncertain (AI couldn't determine)"
        
        return "Error (Invalid API Response)"

    except Exception as e:
        print(f"API Error: {e}")
        return "Error (API Failure)"

# HTML content as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Fact Checker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 300px;
            padding: 10px;
            margin-right: 10px;
        }
        input[type="submit"] {
            padding: 10px 15px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        h2 {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>News Fact Checker</h1>
    <form method="POST">
        <label for="news_statement">Enter a news statement:</label><br>
        <input type="text" id="news_statement" name="news_statement" required><br><br>
        <input type="submit" value="Check Fact">
    </form>
    <h2>Result:</h2>
    <p>{{ result }}</p>
</body>
</html>
"""

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    from flask import render_template_string

    result = ""
    if request.method == 'POST':
        news_statement = request.form['news_statement']
        if news_statement:
            fact_check_result = check_fact(news_statement)
            if "Error" in str(fact_check_result):
                result = fact_check_result
            else:
                result = (f"Prediction: {output_label(fact_check_result)}")

    return render_template_string(HTML_TEMPLATE, result=result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
