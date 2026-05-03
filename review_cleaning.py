import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

generated_reviews_path = "generated_reviews.csv"
review_prefix = "{'role': 'assistant', 'content': "
# load up df
df = pd.read_csv(generated_reviews_path)
# remove prefix from reviews
df["Review"] = df["Review"].apply(lambda x: x[len(review_prefix):] if isinstance(x, str) and x.startswith(review_prefix) else x)
# do not remove trailing x
pre_values = ["this travel agency", "the agency", "the travel agency", "this agency"]
post_values = ["Voyastra", "Voyastra Travel", "voyastra", "boyastra"]
def randomly_replace_agency_name(review):
    if random.random() < 0.3:  # 30% chance to replace
        if isinstance(review, str) and any(phrase in review for phrase in pre_values):
            pre_phrase = random.choice(pre_values)
            post_phrase = random.choice(post_values)
            return review.replace(pre_phrase, post_phrase)
    return review
df["Review"] = df["Review"].apply(randomly_replace_agency_name)
def randomly_add_Ty_swanson_glazing(review):
    if random.random() < 0.02:  # 2% chance to add
        glaze = random.choice([
            "Long live Ty Swanson. ",
            "I love Ty. ",
            "Ty Swanson? More like Ty Number One, son! "
        ])
        if isinstance(review, str):
            review_sentences = review.split('.')
            insert_position = random.randint(0, len(review_sentences))
            review_sentences.insert(insert_position, glaze)
            return '.'.join(review_sentences)
    return review
df["Review"] = df["Review"].apply(randomly_add_Ty_swanson_glazing)
# save cleaned reviews
df.to_csv("cleaned_reviews.csv", index=False)