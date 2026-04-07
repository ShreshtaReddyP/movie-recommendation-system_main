import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load your movie data
movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies = movies.head(2000)

print("Columns in data:", movies.columns)

# Improve tags (IMPORTANT)
if 'tags' in movies.columns:
    movies['tags'] = movies['title'] + " " + movies['tags']
else:
    movies['tags'] = movies['title']

#  ADD THIS LINE HERE
movies['tags'] = movies['tags'].apply(lambda x: x.lower())

data = movies['tags']

# Convert text → vectors
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(data.astype(str)).toarray()
vectors = vectors.astype('float32')

similarity = cosine_similarity(vectors)

# Save similarity file
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))

print("✅ similarity.pkl created successfully!")