TRAVEL AGENCY SYNTHETIC DATA GENERATION PLAN

---

## STEP 0: GLOBAL PARAMETERS

* Number of transactions: 10,000
* Number of reviews: 1,000
* Time range: 2021-01 to 2025-12 (60 months)
* Agency hourly cost: $30

---

## STEP 1: DEFINE DESTINATIONS

Create a destination table with fields:

* Destination_name
* Region (Europe, Asia, Americas, Africa, Oceania)
* Popularity_score (0–1)
* Peak_months (list of months)

Rules:

* Europe destinations start with higher popularity but decline over time
* Asia destinations increase in popularity over time
* Less popular destinations have:

  * Lower popularity_score
  * Higher agency hours
  * Higher review ratings

---

## STEP 2: GENERATE CLIENT BASE

Generate ~4,000–6,000 unique clients.

Fields:

* Client_ID
* Age (sample from skewed distribution favoring younger clients)
* Age_range:

  * 18–25
  * 26–35
  * 36–50
  * 51+
* Gender (M/F/Other with realistic proportions)
* Nationality (grouped by continent)

Latent variables:

* Travel_frequency (Poisson distribution, mean ~1.8)
* Patience_level (0–1)
* Budget_sensitivity (0–1)

Rules:

* Younger clients:

  * Higher budget sensitivity
  * Lower patience
* Older clients:

  * Lower patience for communication delays
  * Higher expected agency hours

---

## STEP 3: GENERATE TRANSACTIONS

For each of 10,000 transactions:

3.1 Assign Client

* Sample client (with probability weighted by Travel_frequency)
* Some transactions (~10%) have no Client_ID (NaN)

3.2 Assign Transaction Month

* Sample month with bias toward:

  * 3 months before peak travel months

3.3 Assign Destination

* Probability depends on:

  * Popularity_score
  * Time trend (Europe ↓, Asia ↑)

3.4 Generate Travel Dates

* Start_date:

  * Typically 1–6 months after TransactionMonth
* End_date:

  * Duration sampled (3–14 days)

3.5 Number of Travelers

* Sample:

  * 1 (solo): 30%
  * 2–3: 40%
  * 4–6: 20%
  * 7+: 10%

---

## STEP 4: COST GENERATION

4.1 Transportation Cost

* Base = function(distance + region)
* Multiply by number_of_travelers
* Add noise

4.2 Accommodation Cost

* Depends on:

  * Destination popularity
  * Accommodation type
  * Duration
* Higher for popular locations

4.3 Accommodation Type

* Budget / Standard / Luxury
* Correlates with:

  * Client age
  * Budget sensitivity

4.4 Insurance Cost

* Small % of total cost (2–5%)
* Slightly higher for older clients

---

## STEP 5: AGENCY HOURS GENERATION

Base hours = function of:

* Destination popularity:

  * Lower popularity → higher hours
* Number_of_travelers
* Client age

Formula:
Agency_hours =
base_hours

* (1 - popularity_score)*X
* age_factor
* traveler_factor
* noise

Rules:

* Older clients → more hours
* Less popular destinations → more hours

---

## STEP 6: AGENCY FEE GENERATION

Agency_fee depends on:

* Client age (younger → higher fees)
* Destination popularity (popular → lower fees)
* Time trend (fees decrease over time)

Formula:
Agency_fee =
base_margin

* age_multiplier
* popularity_discount
* time_decay

- noise

Rules:

* Younger clients pay more
* Popular destinations pay less
* Fees shrink over time

---

## STEP 7: PROFITABILITY CONTROL

Profit =
Agency_fee - (Agency_hours * 30)

Adjust:

* Increase hours slightly over time
* Decrease fees over time

Ensure:

* Average profit declines over time

---

## STEP 8: DATA QUALITY ISSUES

Introduce noise:

* Missing values (3–7%) in:

  * Client_ID
  * Accommodation_type
* Date format inconsistencies:

  * yyyy-mm-dd
  * mm/dd/yyyy
* Destination formatting variations:

  * "City, Country"
  * "City (Country)"
  * "City; Country"
* Typos (~2–3%)

---

## STEP 9: GENERATE REVIEWS (1,000)

Sample 1,000 transactions.

Fields:

* Trip_ID
* Rating (1–5)
* Review_text

---

## STEP 10: REVIEW RATING GENERATION

Rating influenced by:

* Client frequency:

  * Repeat clients → higher ratings
* Destination popularity:

  * Less popular → higher ratings
* Client age:

  * Older → lower ratings
* Booking timing:

  * Close to peak → lower ratings

---

## STEP 11: REVIEW TEXT GENERATION

Use templated text with embedded signals:

Include references to:

1. Communication:

   * "too much back and forth"
   * "slow responses"

2. Timing:

   * "last-minute planning issues"

3. Group size:

   * "difficult coordinating documents/passports"

4. Destination sentiment:

   * "hidden gem", "less crowded", "amazing experience"

Rules:

* Older clients:

  * Mention communication frustration

* Less popular destinations:

  * Strong positive tone

* Close-to-peak bookings:

  * Mention delays

* Large groups:

  * Mention logistics difficulty

Ensure:

* Each review text independently signals the pattern

---

## STEP 12: FINAL OUTPUT STRUCTURE

Transactions columns:

* Trip_ID
* TransactionMonth
* Destination
* Start_date
* End_date
* Number_of_travelers
* Client_ID
* Client_age_range
* Client_gender
* Client_nationality
* Accommodation_type
* Transportation_cost
* Accommodation_cost
* Insurance_cost
* Agency_fee
* Agency_hours

Reviews columns:

* Trip_ID
* Rating
* Review_text

---

## END OF PLAN
