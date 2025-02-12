from flask import Flask, request, render_template
import google.generativeai as ai

# Initialize Flask app
app = Flask(__name__)

# Configure the AI model
with open("api key.txt") as f:
    key = f.read().strip()
ai.configure(api_key=key)

@app.route('/', methods=['GET', 'POST'])
def generate_story():
    story = None
    error = None

    if request.method == 'POST':
        # Get the region and language input from the form
        user_region = request.form.get("region")
        user_language = request.form.get("language")

        if not user_region or not user_language:
            error = "Both region and language are required."
        else:
            try:
                # Define the generative model
                model = ai.GenerativeModel(model_name="gemini-1.5-flash")

                # Craft the prompt based on user input
                user_prompt = f"""
                Generate a short folk tale based on the myths and legends of {user_region}.
                The story should:
                1. Reflect the traditions, values, and beliefs of {user_region}'s culture.
                2. Incorporate accurate dialects, tones, and idiomatic expressions typical of the region.
                3. Include a moral lesson that aligns with the cultural and ethical teachings of {user_region}.
                4. Be culturally sensitive, avoiding stereotypes or misrepresentations.
                5. Be in the {user_language} language, suitable for young readers.
                6. Follow local storytelling traditions, including pacing, structure, and key motifs.

                Constraints:
                - The story must be concise (300-500 words).
                - The language must be age-appropriate.
                - Exclude any controversial or inappropriate content.
                """

                # Generate the response
                response = model.generate_content(user_prompt)
                story = response.text

            except Exception as e:
                error = str(e)

    # Render the HTML template with the story and error message
    return render_template('index.html', story=story, error=error)

if __name__ == '__main__':
    app.run(debug=True)
