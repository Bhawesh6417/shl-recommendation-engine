from flask import Flask, request, jsonify
import pandas as pd
import google.generativeai as genai  # Import the Gemini library

app = Flask(__name__)

# Initialize the Google Gemini client
api_key = 'AIzaSyB8ElKvrPTYaV9kG2q4AsTXYCc6fTIk0Uo'  # Add your Google API key here
genai.configure(api_key=api_key)

# Load candidate data from the CSV
def load_candidates_from_csv(file_path: str):
    # Read the CSV file
    df = pd.read_csv(file_path)
    candidates = df[['CandidateID', 'Skills', 'Industry', 'Recommended_Assessment']].to_dict(orient='records')
    return candidates

# Example path to your CSV file (change this to your actual path)
CANDIDATE_CSV_PATH = 'shl_product_catalog.csv'

@app.route("/recommend", methods=["GET"])
def recommend_assessment():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query parameter provided"}), 400

    # Load the candidates from the CSV file
    candidates = load_candidates_from_csv(CANDIDATE_CSV_PATH)

    # Now, let's prepare the data
    candidate_skills_and_industries = [f"{candidate['Skills']} {candidate['Industry']}" for candidate in candidates]

    # Use Google Gemini to evaluate similarity between the JD and the candidate's skills & industries
    scores = []
    for candidate_profile in candidate_skills_and_industries:
        # Using Google's Gemini model to evaluate the similarity between the job description and candidate profiles
        response = genai.generate_text(
            prompt=f"Given the job description '{query}' and the candidate profile '{candidate_profile}', score the similarity on a scale from 1 to 10.",
            temperature=0.7,
            max_output_tokens=10
        )

        # Extract the score from the Gemini response
        score = float(response['candidates'][0]['text'].strip())  # Assuming the response is in this format
        scores.append(score)

    # Find the candidate with the best score
    best_candidate_index = scores.index(max(scores))
    best_candidate = candidates[best_candidate_index]

    # Return the recommended assessment for that candidate
    return jsonify({
        "recommended_assessment": best_candidate['Recommended_Assessment'],
        "candidate_id": best_candidate['CandidateID']
    })

if __name__ == "__main__":
    app.run(debug=True)
