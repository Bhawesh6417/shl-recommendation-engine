from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import preprocess_catalog

catalog_csv_path = "backend/shl_product_catalog.csv"

X, assessments, candidate_ids, vectorizer = preprocess_catalog(catalog_csv_path)

def search(query):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, X).flatten()
    top_indices = similarity.argsort()[-5:][::-1]  # top 5 matches

    results = []
    for idx in top_indices:
        results.append({
            "CandidateID": candidate_ids[idx],
            "Recommended_Assessment": assessments[idx],
            "Similarity": float(similarity[idx])
        })
    return results
