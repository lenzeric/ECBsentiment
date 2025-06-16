# Good version with TF-IDF ngram lists.
# Import block
import pandas as pd
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.util import ngrams
import matplotlib.pyplot as plt

import seaborn as sns # pip install seaborn
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Global constants
#stop_words = set(stopwords.words('english'))
stop_words = list(stopwords.words("english"))
        
# Functions block
def clean_text(text):
    # Step 1: Sentence tokenize
    sent = sent_tokenize(text)
    
    # Step 2: Word tokenize each sentence
    words_1 = [word_tokenize(t) for t in sent]
    
    # Step 3: Flatten nested list
    list_words = sum(words_1, [])
    
    # Step 4: Remove single-character words except 'a' and 'i'
    token_words = [word for word in list_words if not (len(word) == 1 and word.lower() not in {"a", "i"})]
    
    # Step 5: Remove "gibberish" (i.e., words without vowels)
    token_words = [word for word in token_words if re.search(r'[aeiou]', word, re.I)]
    
    # Step 6: Lowercase all
    low_words = [w.lower() for w in token_words]
    
    # Step 7: Remove stopwords
    remove_words = [w for w in low_words if w not in stop_words]
    
    # Step 8: Remove punctuation (keep only alphanumeric)
    punc_words = [w for w in remove_words if w.isalnum()]
    
    # Step 9: Rejoin to single cleaned string
    unique_string = " ".join(punc_words)
    
    return unique_string

def load_lm_master_dictionary(filepath):
    # Read CSV file (skip header if necessary)
    df = pd.read_csv(filepath)
    df['Word'] = df['Word'].astype('string').fillna('')
    
     # Convert to dictionary for quick lookups
    lm_lexicon = defaultdict(lambda: {"Negative": 0, "Positive": 0})
    
    for _, row in df.iterrows():
        word = row["Word"].lower()  # Convert to lowercase for matching
        lm_lexicon[word]["Negative"] = int(row["Negative"])
        lm_lexicon[word]["Positive"] = int(row["Positive"])
        
    return lm_lexicon

# Define function find_ngram_sentiments_master to associate words and sentiments from lm_lexicon to user-defined text (cleaned text from Fed documents organized by date). ngrams_with_n will be a list of tuples. The matched ngrams with positive sentiment receive a score of 1 and negative sentiment a score of -1. Context words also receive sentiment scores and sum up to adjusted_sentiment which is associated with an ngram and date. The function returns data frame full_df. 
def find_ngram_sentiments_master_from_df(df, ngrams_with_n, lm_lexicon):
    all_sentiment_data = []
    total_words_per_date = {}

    # Convert the DataFrame to a dictionary: {date: cleaned_text}
    #text_data_by_date = dict(zip(df["date"], df["cleaned_text"]))

    # Convert the DataFrame to a dictionary: {date: clean_text}
    text_data_by_date = dict(zip(df["date"], df["clean_text"]))
    
    # Extract n-grams and n-values
    ngram_list, n_values = zip(*ngrams_with_n)
    #ngram_set = set(ngram_list)
    ngram_set = set(tuple(ngram.split()) for ngram in ngram_list)
    
    for date, text in text_data_by_date.items():
        words = word_tokenize(text.lower())
        total_words_per_date[date] = len(words)

        text_ngrams_dict = {n: list(ngrams(words, n)) for n in set(n_values)}

        sentiment_data = []

        for n_value in text_ngrams_dict:
            text_ngrams = text_ngrams_dict[n_value]
            for i, ngram in enumerate(text_ngrams):
                if ngram in ngram_set:
                    start = max(i - 10, 0)
                    end = min(i + n_value + 10, len(words))
                    context_words = words[start:end]
                    context_text = " ".join(context_words)

                    sentiment_score = (
                        1 if lm_lexicon[" ".join(ngram)]["Positive"] > 0 else
                        -1 if lm_lexicon[" ".join(ngram)]["Negative"] > 0 else
                        0
                    )

                    before_sentiment = sum(
                        1 if lm_lexicon[word]["Positive"] > 0 else -1 if lm_lexicon[word]["Negative"] > 0 else 0
                        for word in words[start:i]
                    )

                    after_sentiment = sum(
                        1 if lm_lexicon[word]["Positive"] > 0 else -1 if lm_lexicon[word]["Negative"] > 0 else 0
                        for word in words[i + n_value:end]
                    )

                    adjusted_sentiment = sentiment_score + before_sentiment + after_sentiment

                    sentiment_data.append({
                        "date": date,
                        "ngram": " ".join(ngram),
                        "context": context_text,
                        "base_sentiment": sentiment_score,
                        "before_sentiment": before_sentiment,
                        "after_sentiment": after_sentiment,
                        "adjusted_sentiment": adjusted_sentiment,
                        "n": n_value
                    })

        all_sentiment_data.extend(sentiment_data)

    full_df = pd.DataFrame(all_sentiment_data)
    full_df["total_words"] = full_df["date"].map(total_words_per_date)
    full_df["total_sentiment"] = full_df["adjusted_sentiment"].fillna(0)

    return full_df

def apply_inclusion_exclusion(row):
    # Retrieve adjusted sentiment & total_words safely
    ngram_info = adjusted_values.get((row["date"], row["ngram"]), {"adjusted_sentiment": 0, "total_words": 1})
    
    base_sentiment = ngram_info["adjusted_sentiment"]
    total_words = ngram_info["total_words"]
    
    # Compute included/excluded sentiment
    included_sentiment = sum(adjusted_values.get((row["date"], inc), {"adjusted_sentiment": 0})["adjusted_sentiment"] 
                             for inc in include_dict.get(row["ngram"], []))
    
    excluded_sentiment = sum(adjusted_values.get((row["date"], exc), {"adjusted_sentiment": 0})["adjusted_sentiment"] 
                             for exc in exclude_dict.get(row["ngram"], []))

    # Compute final adjusted sentiment
    final_sentiment = base_sentiment + included_sentiment - excluded_sentiment

    return pd.Series({"final_adjusted_sentiment": final_sentiment, "total_words": total_words})

# Add a function to tokenize the text for TF-IDF model
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# --- Optional: View top ngrams per document ---
def top_ngrams_for_doc(row_vector, feature_names, top_n=10):
    sorted_indices = np.argsort(row_vector)[::-1][:top_n]
    return [(feature_names[i], row_vector[i]) for i in sorted_indices if row_vector[i] > 0]

# Main execution block
# Load the files
df1 = pd.read_csv("scraped_texts_with_dates.csv")
df2 = pd.read_csv("scraped_texts_with_dates_2.csv")

# Combine both
df = pd.concat([df1, df2], ignore_index=True)

# Group by date and concatenate all texts for the same date. There is no longer a "url" or "index" column because we're grouping by date. We're only planning to use "date" and "text".
df = (
    df.groupby("date", as_index=False)["text"]
    .agg(lambda x: " ".join(x))
)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%y")

# Example: sort by date
df = df.sort_values("date")

# TF-IDF specification of ngrams
# Preprocess the text
df["clean_text"] = df["text"].astype(str).apply(preprocess)

# Define vectorizer for 1-3 grams ---
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    max_df=0.95,
    min_df=2
)

tfidf_matrix = vectorizer.fit_transform(df["clean_text"])
feature_names = vectorizer.get_feature_names_out()

# Compute average TF-IDF score per ngram
avg_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
top_ngrams = pd.DataFrame({
    "ngram": feature_names,
    "avg_tfidf": avg_scores
}).sort_values(by="avg_tfidf", ascending=False)

# View top 20 ngrams
print(top_ngrams.head(20))

tfidf_scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
top_indices = tfidf_scores.argsort()[::-1]  # sort descending

top_ngrams = [(feature_names[i], tfidf_scores[i]) for i in top_indices[:100]]

# Top 100 ngrams from TF-IDF
top_ngrams_only = [ngram for ngram, score in top_ngrams]

# Export top 100 ngrams with scores to CSV
df_top_ngrams = pd.DataFrame(top_ngrams, columns=["ngram", "tfidf_score"])
df_top_ngrams.to_csv("top_ngrams.csv", index=False)

# Optional: Export full ranked list
pd.DataFrame(top_ngrams, columns=["ngram", "tfidf_score"]).to_csv("top_ngrams.csv", index=False)

top_ngrams_lower = [ng.lower() for ng in top_ngrams_only]
ngrams_with_n = [(ngram, len(ngram.split())) for ngram in top_ngrams_lower]

# Load the Master Dictionary from Loughran-McDonald
lm_filepath = "Loughran-McDonald_MasterDictionary_1993-2023.csv"  # Update with actual path
lm_lexicon = load_lm_master_dictionary(lm_filepath)

# Create dataframe of sentiments from the cleaned text (merged_text_by_date), ngram lists (all_ngrams), and Loughran-McDonald dictionary (lm_lexicon).
df_all = find_ngram_sentiments_master_from_df(df, ngrams_with_n, lm_lexicon)

# Aggregate by date and ngram. There may be many instances of the same ngram for each date (and within each document). Therefore, adjusted_sentiment is now the sum of adjusted_sentiment by date and ngram.
df_all = df_all.groupby(["date", "ngram"]).agg(
    adjusted_sentiment=("adjusted_sentiment", "sum"),
    total_words=("total_words", "first"),  # Use "first" since total_words is constant per date
).reset_index()

# Get all unique dates and ngrams
all_dates = df_all["date"].unique()
all_ngrams = df_all["ngram"].unique()

# Create full DataFrame with all (date, ngram) combinations
full_index = pd.MultiIndex.from_product([all_dates, all_ngrams], names=["date", "ngram"])
full_df = pd.DataFrame(index=full_index).reset_index()

# Merge the full grid with ngram_sentiment_df to ensure all pairs exist
df_all = full_df.merge(df_all, on=["date", "ngram"], how="left")

# Create dictionary mapping (date, ngram) → (adjusted_sentiment, total_words)
adjusted_values = df_all.set_index(["date", "ngram"])[["adjusted_sentiment", "total_words"]].to_dict(orient="index")

# Apply the function and update full_df
df_all[["final_adjusted_sentiment", "total_words"]] = df_all.apply(apply_inclusion_exclusion, axis=1)

# Aggregate by date and ngram. There may be many instances of the same ngram for each date (and within each document). Therefore, adjusted_sentiment is now the sum of adjusted_sentiment by date and ngram.
df_by_date = df_all.groupby("date").agg(
    total_sentiment=("final_adjusted_sentiment", "sum"),
    total_words=("total_words", "first")  # or "sum"
).reset_index()

# Fill in missing values so all (date) combinations exist.
# This ensures neutral sentiment for missing phrases and avoids divide-by-zero issues.
df_by_date["total_sentiment"] = df_by_date["total_sentiment"].fillna(0)
df_by_date["total_words"] = df_by_date["total_words"].fillna(1)

# Scale and standardize. Divide final_adjusted_sentiment by total_words and call it scaled_sentiment. Then standardize it.
df_by_date["scaled_sentiment"] = df_by_date["total_sentiment"] / df_by_date["total_words"]

df_by_date["standardized_sentiment"] = (
    df_by_date["scaled_sentiment"] - df_by_date["scaled_sentiment"].mean()
) / df_by_date["scaled_sentiment"].std()

# Add refinancing rate to plot to compare to standardized sentiment
# Load ECB refinancing rate ---
ecb_df = pd.read_csv("refinancingrate.csv", parse_dates=["date"])

# Create a pivoted dataframe and export to Excel in one sheet. I want ngrams as columns, dates as row numbers, and standardized sentiments as values in the center. This matches the format in Drechsel and Aruoba's Excel file in the sheet: Sentiments by meeting.
pivot_df = df_by_date[["date", "standardized_sentiment"]].set_index("date")
pivot_df.rename(columns={"standardized_sentiment": "sentiment_zscore"}, inplace=True)
pivot_df.sort_index(inplace=True)

# Resample to monthly frequency (month-end)
monthly_df = pivot_df.resample("ME").mean()

# Apply 12-month moving average
rolling_df = monthly_df.rolling(window=12, min_periods=1).mean()

# Add 'year_month' for merging
rolling_df["year_month"] = rolling_df.index.to_period("M").astype(str)
ecb_df["year_month"] = ecb_df["date"].dt.to_period("M").astype(str)

# Merge on 'year_month'
merged_df = pd.merge(
    rolling_df.reset_index(),
    ecb_df[["mrr", "year_month"]],
    on="year_month",
    how="left"
)

# Drop any rows with missing data if needed (optional)
merged_df.dropna(subset=["sentiment_zscore", "mrr"], inplace=True)

# Correlation
correlation = merged_df["sentiment_zscore"].corr(merged_df["mrr"])

# Dual-axis plot with custom colors and no grid on second y-axis ---
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot sentiment on primary y-axis (dark blue)
sentiment_color = "#003366"
ax1.set_xlabel("Date")
ax1.set_ylabel("Sentiment (12-mo MA)", color=sentiment_color)
ax1.plot(merged_df["date"], merged_df["sentiment_zscore"], label="Sentiment (12-mo MA)", color=sentiment_color)
ax1.tick_params(axis='y', labelcolor=sentiment_color)
ax1.grid(True)  # Enable grid only for ax1

# Plot ECB rate on secondary y-axis (light blue) without grid
rate_color = "#66b3ff"
ax2 = ax1.twinx()
ax2.set_ylabel("ECB Refinancing Rate (%)", color=rate_color)
ax2.plot(merged_df["date"], merged_df["mrr"], label="Refinancing Rate", color=rate_color)
ax2.tick_params(axis='y', labelcolor=rate_color)
ax2.grid(False)  # Disable grid for ax2

# Title and layout
plt.title(f"ECB Sentiment vs. Refinancing Rate\nCorrelation: {correlation:.2f}")
fig.tight_layout()
plt.show()