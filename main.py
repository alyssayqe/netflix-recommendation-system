import pandas as pd

# Load the Netflix dataset
df = pd.read_csv('netflix_titles.csv')

# Function to split values in each column of the dataset and output unique values
def split_and_output_unique_values(df):
    unique_genres = set()
    unique_cast = set()
    unique_types = set()

    for row in df.itertuples(index=False):
        genres = str(row.listed_in).split(',') if pd.notnull(row.listed_in) else []
        cast = str(row.cast).split(',') if pd.notnull(row.cast) else []

        unique_genres.update(genres)
        unique_cast.update(cast)
        unique_types.add(row.type)
      
    unique_genres = sorted(unique_genres) # Sort unique genres into alphabetical order
    
    return unique_genres, unique_cast, unique_types


# Function to get recommendations based on user input
def get_recommendations(user_input, unique_genres, unique_cast, unique_types):
    recommendations = []
    
    for row in df.itertuples(index=False):
        matches = []
        
        if not user_input['type'] or user_input['type'] == row.type:
            matches.append(True)
        
        if not user_input['cast'] or (row.cast and any(cast_member in str(row.cast).split(", ") for cast_member in user_input['cast'])):
            matches.append(True)
        
        if not user_input['genre'] or any(genre in str(row.listed_in).split(", ") for genre in user_input['genre']):
            matches.append(True)
        
        if all(matches):
            recommendations.append(row.title)

    return recommendations

# Split values in each column and output unique values
unique_genres, unique_cast, unique_types = split_and_output_unique_values(df)

# Print the list of unique genres
print("List of Genres:")
for genre in unique_genres:
    print(genre)

# Add a blank line for spacing
print()

# Prompt user for input
user_input = {
    'type': input("Enter 'Movie' or 'TV Show' (optional, press Enter to include all): "),
    'cast': input("Enter the cast members (comma-separated, optional, press Enter to include all): "),
    'genre': input("Enter the genres (comma-separated, optional, press Enter to include all): ")
}

# Convert cast and genre inputs to a list if not empty
if user_input['cast']:
    user_input['cast'] = [cast.strip() for cast in user_input['cast'].split(',')]

if user_input['genre']:
    user_input['genre'] = [genre.strip() for genre in user_input['genre'].split(',')]

# Get recommendations based on user input
recommendations = get_recommendations(user_input, unique_genres, unique_cast, unique_types)

# Filter out recommendations based on cast members
if user_input['cast'] and recommendations:
    recommendations = [recommendation for recommendation in recommendations if any(cast_member in str(df.loc[df['title'] == recommendation, 'cast'].values[0]).split(", ") for cast_member in user_input['cast'])]

# Filter out recommendations based on genres
if user_input['genre'] and recommendations:
    recommendations = [recommendation for recommendation in recommendations if any(genre in str(df.loc[df['title'] == recommendation, 'listed_in'].values[0]).split(", ") for genre in user_input['genre'])]

# Add a blank line for spacing
print()

# Print the recommendations
if recommendations:
    print("Recommended Content:")
    for recommendation in recommendations:
        print(recommendation)
else:
    print("No recommendations found.")







