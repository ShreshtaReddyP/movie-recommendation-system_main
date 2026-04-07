import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load your movie data
movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

print("Columns in data:", movies.columns)

# Try to create tags (important step)
if 'tags' in movies.columns:
    data = movies['tags']
else:
    # fallback: use titles
    data = movies['title']

# Convert text → vectors
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(data.astype(str)).toarray()
vectors = vectors.astype('float32')

similarity = cosine_similarity(vectors)

# Save similarity file
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))

print("✅ similarity.pkl created successfully!")