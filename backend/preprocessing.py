import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_catalog(catalog_csv_path):
    df = pd.read_csv(catalog_csv_path)

    # Combine relevant fields for vectorization
    df["combined"] = df["Education"].astype(str) + " " + \
                     df["ExperienceYears"].astype(str) + " years experience " + \
                     df["Skills"].astype(str) + " " + \
                     df["Industry"].astype(str)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["combined"])

    return (
        X,
        df["Recommended_Assessment"].tolist(),
        df["CandidateID"].tolist(),
        vectorizer
    )
preprocess_catalog("backend/shl_product_catalog.csv")