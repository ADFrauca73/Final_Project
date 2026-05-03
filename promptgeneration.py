import pandas as pd
import os
from time import time

import transformers
import torch
from huggingface_hub import login

secret_key = os.getenv("HUGGINGFACE_KEY")
print(f"Hugging Face Key: {secret_key}")

# Log in to Hugging Face
if secret_key:
    login(secret_key)
else:
    print("HUGGINGFACE_KEY environment variable not set.")
    exit()

prompts_path = "review_prompts.csv"

def generate_review(system_prompt, user_prompt, pipeline):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )
    return(outputs[0]["generated_text"][-1])

def check_if_already_generated(trip_id):
    if os.path.exists("generated_reviews.csv"):
        existing_df = pd.read_csv("generated_reviews.csv")
        return trip_id in existing_df["Trip_ID"].values
    return False
def append_review_to_csv(trip_id, review_score, review):
    new_entry = pd.DataFrame([{
        "Trip_ID": trip_id,
        "Review_score": review_score,
        "Review": review
    }])
    if os.path.exists("generated_reviews.csv"):
        new_entry.to_csv("generated_reviews.csv", mode='a', header=False, index=False)
    else:
        new_entry.to_csv("generated_reviews.csv", index=False)

if __name__ == "__main__":
    df = pd.read_csv(prompts_path)
    # iterate through rows and generate reviews
    manually_validate = False
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    pipeline = transformers.pipeline(
        
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )
    for index, row in df.iterrows():
        Trip_ID,System_prompt,User_prompt,Review_score = row["Trip_ID"], row["System_prompt"], row["User_prompt"], row["Review_score"]
        print(f"Trip_ID: {Trip_ID}, Review_score: {Review_score}")
        if check_if_already_generated(Trip_ID):
            print(f"Review for Trip_ID {Trip_ID} already generated. Skipping.")
            continue
        start_time = time()
        review = generate_review(System_prompt,User_prompt,pipeline)
        end_time = time()
        print(f"Generated Review: {review}\n")
        print(f"Generation Time: {end_time - start_time:.2f} seconds")
        if manually_validate:
            decision = input("y: continue, n: stop, c: continue without manual validation: \n")
            if decision.lower() == "n":
                break
            elif decision.lower() == "c":
                manually_validate = False
        append_review_to_csv(Trip_ID, Review_score, review)

    print("Review generation process completed.")



