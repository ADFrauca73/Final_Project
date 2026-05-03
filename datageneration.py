import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# -----------------------------
# GLOBAL PARAMETERS
# -----------------------------
N_TRANSACTIONS = 10000
N_REVIEWS = 500
START_DATE = pd.to_datetime("2021-01-01")
MONTHS = pd.date_range(start=START_DATE, periods=60, freq='MS')

# -----------------------------
# DESTINATIONS
# -----------------------------
destinations = pd.DataFrame({
    "Destination": [
        "Paris, France", "Rome, Italy", "Barcelona, Spain", "Reykjavik, Iceland",
        "Bangkok, Thailand", "Tokyo, Japan", "Bali, Indonesia", "New Delhi, India",
        "Lima, Peru", "Santiago, Chile", "Buenos Aires, Argentina",
        "Cape Town, South Africa", "Marrakech, Morocco", "Johannesburg, South Africa", "Cairo, Egypt"
    ],
    "Region": [
        "Europe","Europe","Europe","Europe",
        "Asia","Asia","Asia","Asia",
        "Americas","Americas","Americas",
        "Africa","Africa","Africa","Africa"
    ],
    "Popularity": [
        0.9,0.85,0.8,0.6,
        0.75,0.7,0.5,0.4,
        0.3,0.28,0.26,
        0.4,0.35,0.32,0.3
    ],
    "is_niche": [False, False, False, True,
        False, False, True, True,
        False, False, True,
        True, True, True, True
    ]

})

def destination_is_niche(dest):
    return destinations.loc[destinations.Destination == dest, "is_niche"].values[0]

peak_months = {
    "Europe": [6,7,8],
    "Asia": [12,1,2],
    "Americas": [12,1,2],
    "Africa": [7,8,9]
}

# -----------------------------
# CLIENT GENERATION
# -----------------------------
N_CLIENTS = 5000
clients = pd.DataFrame({
    "Client_ID": range(1, N_CLIENTS+1)
})

continents = {"North America": 0.25, "Europe": 0.35, "Asia": 0.25, "Africa": 0.05, "South America": 0.1}
continent_to_nationalities = {
    "North America": {"USA": 0.4, "Canada": 0.3, "Mexico": 0.2, "Cuba": 0.05, "Panama": 0.05},
    "Europe": {"UK": 0.2, "Germany": 0.15, "France": 0.15, "Italy": 0.05, "Spain": 0.05, "Iceland": 0.05, "Greece": 0.05, "Romania": 0.05, "Sweden": 0.05, "Poland": 0.05, "Portugal": 0.05, "Austria": 0.05, "Switzerland": 0.05},
    "Asia": {"China": 0.3, "India": 0.2, "Japan": 0.15, "South Korea": 0.1, "Indonesia": 0.1, "Thailand": 0.1, "Vietnam": 0.05},
    "Africa": {"Nigeria": 0.2, "South Africa": 0.2, "Egypt": 0.2, "Kenya": 0.1, "Ethiopia": 0.1, "Ghana": 0.1, "Morocco": 0.1},
    "South America": {"Brazil": 0.4, "Argentina": 0.2, "Colombia": 0.15, "Chile": 0.05, "Peru": 0.1, "Venezuela": 0.05, "Ecuador": 0.05}
}


clients["Age"] = np.random.choice(range(18,70), size=N_CLIENTS, p=None)
clients["Age_range"] = pd.cut(clients["Age"], bins=[17,25,35,50,100], labels=["18-25","26-35","36-50","51+"])
clients["Gender"] = np.random.choice(["M","F","Other"], size=N_CLIENTS, p=[0.48,0.48,0.04])
clients["Continent"] = np.random.choice(list(continents.keys()), size=N_CLIENTS, p=list(continents.values()))
clients["Referral_source"] = np.random.choice(["Online Ad", "Friend/Family", "Search Engine", "Social Media", "Other"], size=N_CLIENTS, p=[0.3,0.25,0.2,0.15,0.1])
clients["Credit_card"] = np.random.choice(["Visa", "MasterCard", "Amex", "Discover"], size=N_CLIENTS, p=[0.4,0.35,0.15,0.1])
def sample_nationality(continent):
    nations = list(continent_to_nationalities[continent].keys())
    probs = list(continent_to_nationalities[continent].values())
    return np.random.choice(nations, p=probs)

clients["Nationality"] = clients["Continent"].apply(sample_nationality)

clients["Travel_freq"] = np.random.poisson(1.8, N_CLIENTS) + 1
clients["Patience"] = np.random.rand(N_CLIENTS)
clients["Budget"] = np.random.rand(N_CLIENTS)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def sample_month():
    return random.choice(MONTHS)

def generate_dates(transaction_month):
    start = transaction_month + pd.DateOffset(days=random.randint(30,180))
    duration = random.randint(3,14)
    end = start + timedelta(days=duration)
    return start, end




# -----------------------------
# TRANSACTIONS
# -----------------------------
records = []

for i in range(N_TRANSACTIONS):
    client = clients.sample(1).iloc[0]
    client_id = client.Client_ID if random.random() > 0.1 else np.nan

    t_month = sample_month()
    t_index = (t_month.year - 2021)*12 + t_month.month

    # destination trend
    dest_probs = []
    for _, row in destinations.iterrows():
        pop = row.Popularity
        if row.Region == "Europe":
            pop *= max(0.5, 1 - t_index/120)
        if row.Region == "Asia":
            pop *= min(1.5, 1 + t_index/120)
        dest_probs.append(pop)
    dest_probs = np.array(dest_probs)/sum(dest_probs)
    dest = destinations.sample(1, weights=dest_probs).iloc[0]

    start, end = generate_dates(t_month)
    duration = (end - start).days

    travelers = np.random.choice([1,2,3,4,5,6,7,8], p=[0.2,0.25,0.15,0.1,0.1,0.1,0.05,0.05])

    # costs
    transport = np.random.normal(500 + 300*(1-dest.Popularity), 100) * travelers
    accom_type = np.random.choice(["Budget","Standard","Luxury"], p=[0.3,0.5,0.2])
    accom_base = {"Budget":50,"Standard":120,"Luxury":300}[accom_type]
    accom_cost = accom_base * duration * travelers * (1 + dest.Popularity)



    insurance = min(0.03*(transport+accom_cost)*(1 + client.Age/100)+ np.random.normal(0,20),100)

    # agency hours (boost for older clients)
    age_hours_base = client.Age/35
    age_hours_factor = 1.5 if client.Age >= 50 else 1.0
    hours = (
        5
        + (1-dest.Popularity)**1.2*10
        + age_hours_base * age_hours_factor
        + (travelers*0.5)**2
        + np.random.normal(0,1)
    )
    #on-call hours as a separate variable
    # 1/5 of total hours, with more variability for less popular destinations
    # higher for older clients and larger groups and last-minute bookings
    on_call_hours = hours * np.random.uniform(0.15, 0.25) * (1 + (1-dest.Popularity)*0.5)**0.9 * (1 + age_hours_base*0.5) * (1 + travelers*0.1) * (1 + max(0,60 - (start - t_month).days)/60)

    # agency fee (significantly boosted)
    if client.Age < 35:
        age_mult = 2.5
    elif client.Age < 50:
        age_mult = 2.0
    else:
        age_mult = 1.8

    pop_disc = (1 - dest.Popularity*0.4)
    time_decay = max(0.6, 1 - t_index/180)

    fee = 700 * age_mult * pop_disc * time_decay + np.random.normal(0,30)

    # introduce noise
    if random.random() < 0.05:
        dest_name = dest.Destination.replace(",", random.choice([" (", "; "]))
    else:
        dest_name = dest.Destination
    def denoise_dest(dest_name):
        return dest_name.replace(" (", ",").replace("; ", ",")

    def sample_hour_of_day():
        return random.choice(["Morning", "Afternoon", "Evening"])
    
    def sample_client_rank(travel_freq):
        def correct_client_rank(travel_freq):
            if travel_freq > 5:
                return random.choice(["VIP", "vip", "V.I.P."])
            elif travel_freq > 2:
                return random.choice(["Frequent", "frequent", "Frequent Traveler"])
            else:
                return "na"
        if travel_freq > 5:
            return correct_client_rank(travel_freq) if random.random() > 0.2 else correct_client_rank(3)
        elif travel_freq > 2:
            return correct_client_rank(travel_freq) if random.random() > 0.2 else correct_client_rank(6) if random.random() > 0.5 else correct_client_rank(1)
        else:
            return correct_client_rank(travel_freq) if random.random() > 0.1 else correct_client_rank(3) if random.random() > 0.5 else correct_client_rank(6)

    def sample_tour_cost(dest_popularity, accom_type):
        accom_boost = {"Budget": 0.8, "Standard": 1.0, "Luxury": 1.3}[accom_type]
        base = 100 * 1.1**(1 + (1-dest_popularity)*0.5)*accom_boost
        return base + np.random.normal(0,20)
    records.append([
        i+1,
        t_month.strftime("%Y-%m"),
        dest_name,
        start.strftime("%Y-%m-%d") if random.random()>0.1 else start.strftime("%m/%d/%Y"),
        end.strftime("%Y-%m-%d"),
        travelers if random.random()>0.05 else np.nan,
        client_id if random.random() > 0.01 else np.nan,
        client.Age_range if random.random()>0.03 else np.nan,
        client.Gender,
        client.Referral_source if random.random()>0.1 else np.nan,
        client.Credit_card if random.random()>0.1 else np.nan,
        client.Nationality,
        client.Age if random.random()>0.1 else np.nan,
        sample_client_rank(client.Travel_freq) if random.random()>0.05 else "na",
        sample_hour_of_day() if random.random()>0.05 else np.nan,
        accom_type if random.random()>0.05 else np.nan,
        round(transport,2) if random.random()>0.03 else np.nan,
        round(accom_cost,2) if random.random()>0.03 else np.nan,
        round(sample_tour_cost(dest.Popularity, accom_type),2) if random.random()>0.03 else np.nan,
        round(insurance,2) if random.random()>0.03 else np.nan,
        round(fee,2) if random.random()>0.03 else np.nan,
        round(hours,2) if random.random()>0.03 else np.nan,
        round(on_call_hours,2) if random.random()>0.3 else np.nan,
        np.random.poisson(0.5) if random.random() > 0.2 else np.nan, #number of associates involved
        np.random.poisson(0.3) if random.random() > 0.3 else np.nan #number of service failures (e.g., booking errors, miscommunications)
    ])

columns = [
    "Trip_ID","TransactionMonth","Destination","Start_date","End_date",
    "Number_of_travelers","Client_ID","Client_age_range","Client_gender","Referral_source","Client_credit_card",
    "Client_nationality", "Client_age","Client_rank","Time_of_first_call","Accommodation_type","Transportation_cost",
    "Accommodation_cost","Tours_cost","Insurance_cost","Agency_fee","Agency_hours","On_call_hours","Associates_involved","Internal_service_failures"
]

transactions = pd.DataFrame(records, columns=columns)

# -----------------------------
# REVIEWS (PROMPT GENERATION)
# -----------------------------
review_sample = transactions.sample(N_REVIEWS)
reviews = []

for _, row in review_sample.iterrows():
    # get start date and transaction month for timing signal
    start_date = None
    transaction_month = None
    try:
        start_date = pd.to_datetime(row.Start_date, errors='coerce')
        transaction_month = pd.to_datetime(row.TransactionMonth + "-01", errors='coerce')
    except:
        pass
    # Numeric review score (1-10) starting at 6 with condition-based random effects
    review_score = 6.0
    if row.Client_age_range == "51+":
        review_score -= 0.5
    if any(x in str(row.Destination) for x in ["(", ";"]):
        review_score += 0.3
    if row.Number_of_travelers > 5:
        review_score -= 0.4
    if pd.notnull(start_date) and pd.notnull(transaction_month) and (start_date - transaction_month).days < 60:
        review_score -= 0.6
    
    if pd.notna(row.Client_ID):
        freq = clients.loc[clients.Client_ID == row.Client_ID, "Travel_freq"]
        if not(freq.empty) and len(freq) > 0 and freq.values[0] > 2:
            review_score += 0.5
    

    # Add randomness while capping between 1 and 10
    review_score += np.random.normal(0, 1.0)
    review_score = max(1, min(10, round(review_score, 1)))

    system_prompt_parts = []
    user_prompt_parts = []

    # Base instruction
    review_length = random.choice([1,2,3,4])
    if review_score <= 5 and random.random() > 0.1:
        review_tone = "negative"
    elif review_score >= 8 and random.random() > 0.1:
        review_tone = "positive"
    else:
        review_tone = "neutral"
    system_prompt_parts.append(
        "You are a customer who recently booked a trip through a travel agency. "
        "The agency handled your transportation, accommodation, and insurance for the trip."
    )
    user_prompt_parts.append(
        f"Write a {review_length}-sentence customer review of a travel agency experience. "
        f"The trip was to {row.Destination} and started on {row.Start_date}. "
        "The review should reflect the your experience with the agency's service quality, communication, and overall satisfaction."
    )
    user_prompt_parts.append(f"The tone should feel {review_tone}.")

    # Client-related signals
    if row.Client_age_range == "51+" and random.random() < 0.4:
        system_prompt_parts.append(
            "You are middle-aged and tend to be less tolerant of excessive back-and-forth communication."
        )
    if row.Client_age_range == "18-25" and random.random() < 0.4:
        system_prompt_parts.append(
            "You are a younger traveler and are more price-sensitive, expecting good value for the cost."
        )

    # Destination sentiment
    if row.Destination != "Unknown" and destination_is_niche(denoise_dest(row.Destination)) and random.random() < 0.3:
        user_prompt_parts.append(
            "The destination is less popular and should be described as a 'hidden gem' or uniquely enjoyable."
        )

    # Group size signal
    if row.Number_of_travelers > 5 and random.random() < 0.4:
        user_prompt_parts.append(
            "The trip involved a large group, and there were frustrations around coordinating passports and traveler information."
        )

    # Timing signal (approximate: shorter lead time proxy)
    try:
        if start_date is not None and pd.notnull(start_date) and transaction_month is not None and pd.notnull(transaction_month):
            lead_time_days = (start_date - transaction_month).days
            if lead_time_days < 60:
                user_prompt_parts.append(
                    "The trip was booked close to the travel date, causing delays in communication."
                )
    except:
        pass

    # Frequent client signal
    if pd.notna(row.Client_ID):
        freq = clients.loc[clients.Client_ID == row.Client_ID, "Travel_freq"]
        if not(freq.empty) and len(freq) > 0 and freq.values[0] > 2:
            system_prompt_parts.append(
                "You are a repeat customer and generally have a positive tone."
            )

    # Cost-related signals (with some noise)
    if row.Agency_fee > 600 and random.random() < 0.3:
        user_prompt_parts.append(
            "The cost felt high for the value provided, contributing to a less satisfied experience."
        )
    elif row.Agency_fee < 300 and random.random() < 0.3:
        user_prompt_parts.append(
            "The cost was reasonable and contributed to a more positive experience."
        )
    # Randomly add signals related to food, quality of accomodation, comfort of transportation,
    # whether the beds were comfy, whether the weather was good, whether the destination was crowded,
    # to add variability and make the review more realistic and less formulaic
    if random.random() < 0.2:
        user_prompt_parts.append(
            random.choice([
                "The food recommendations provided by the agency were fantastic and enhanced the trip experience.",
                "The accommodation booked by the agency was subpar and detracted from the overall enjoyment of the trip.",
                "The transportation arrangements were comfortable and reliable, making the travel experience smooth.",
                "The beds at the accommodation were uncomfortable, leading to restless nights during the trip.",
                "The weather at the destination was unexpectedly bad, which impacted outdoor plans and overall enjoyment.",
                "The destination was more crowded than anticipated, which made it difficult to enjoy popular attractions."
            ])
        )
    # Random irrelevant complaints or praises to add variability
    # stuff the agency has no control over but that a customer might still mention in a review, to make it more realistic and less formulaic
    if random.random() < 0.15:
        user_prompt_parts.append(
            random.choice([
                "The agent's accent was hard to understand, which made communication frustrating.",
                "The tap water tasted weird at the accommodation, which was a minor but annoying issue.",
                "The Wi-Fi connection at the accommodation was unreliable, affecting productivity and entertainment.",
                "The check-in process was lengthy and inefficient, causing delays in settling into the accommodation.",
                "The local cuisine was delicious and a highlight of the trip, even though it was not arranged by the agency.",
                "The local tour guide recommended by the agency was knowledgeable and made the sightseeing experience much more enjoyable.",
                "The local tour guide recommended by the agency was unprofessional and detracted from the sightseeing experience.",
                "The locals were rude and unhelpful, which negatively impacted the overall experience of the trip.",
                "The local currency exchange rates were unfavorable during the trip, which was frustrating.",
                "The local currency exchange rates were favorable during the trip, which was a pleasant surprise."
            ])
        )
    for _ in range(2):
        if random.random() < 0.15:
            user_prompt_parts.append(
                random.choice([
                    "You've been really getting into non-fiction literature lately.",
                    "Your cat was lonely while you were away and has been extra affectionate since you returned.",
                    "Your boss has been a real pain at work.",
                    "Your neighbor Daniel is a real asshole, isn't he?",
                    "Your football team has been doing really well this season.",
                    "You can't seem to find a good show to watch on TV these days.",
                    "You've been trying to eat healthier but it's been a struggle.",
                ])
            )
    user_prompt_parts.append(
        "The tone and content should naturally reflect these details without explicitly listing them."
    )

    system_prompt = " ".join(system_prompt_parts)
    user_prompt = " ".join(user_prompt_parts)

    reviews.append([row.Trip_ID, system_prompt, user_prompt, review_score])

reviews_df = pd.DataFrame(reviews, columns=["Trip_ID", "System_prompt", "User_prompt", "Review_score"])

# -----------------------------
# SAVE FILES
# -----------------------------
transactions.to_csv("transactions.csv", index=False)
reviews_df.to_csv("review_prompts.csv", index=False)

print("Data generation complete.")
