# Travel Agency Synthetic Data Generation

This repository contains scripts for generating synthetic datasets for a travel agency capstone project. The code creates plausible transaction and review data with embedded insights for analysis and modeling.

## Data Generation Strategies

The synthetic data generation employs several strategies to create realistic datasets:

- **Destination Modeling**: Destinations are categorized by region (Europe, Asia, Americas, Africa) with popularity scores and peak travel months. European destinations decline in popularity over time, while Asian destinations increase, reflecting real-world trends.

- **Client Demographics**: Clients are generated with age distributions favoring younger travelers, gender proportions, and nationalities grouped by continent. Latent variables like travel frequency, patience level, and budget sensitivity influence behavior.

- **Transaction Dynamics**: Transactions incorporate temporal biases (e.g., booking 3 months before peak seasons), destination popularity trends, and realistic travel durations (3-14 days). Traveler group sizes follow common patterns.

- **Cost Structures**: Transportation and accommodation costs vary by distance, region, popularity, and accommodation type (budget/standard/luxury). Insurance costs are proportional to total expenses.

- **Agency Operations**: Agency hours and fees depend on destination popularity, client age, and time trends. Profitability is controlled to ensure realistic margins.

- **Review Generation**: Reviews are generated using transformer models with prompts that incorporate transaction details, creating varied sentiment and content.

These strategies ensure the data contains useful insights like seasonal trends, demographic correlations, profitability analysis, and customer sentiment patterns.

## Running the Scripts

Follow these steps in order to generate the complete synthetic dataset:

1. **Download Original Data**:
   ```bash
   python download.py
   ```
   This downloads a real travel dataset from Kaggle for reference.

2. **Explore and Clean Original Data**:
   ```bash
   python basicexploration.py
   ```
   Performs initial exploration and cleaning of the downloaded data, creating a cleaned version.

3. **Generate Synthetic Transactions**:
   ```bash
   python datageneration.py
   ```
   Creates 10,000 synthetic transactions with clients, destinations, costs, and agency metrics.

4. **Generate Review Prompts**:
   ```bash
   python promptgeneration.py
   ```
   Uses transformer models to generate review prompts based on transaction data. Requires a Hugging Face API key set as `HUGGINGFACE_KEY` environment variable.

5. **Clean Generated Reviews**:
   ```bash
   python review_cleaning.py
   ```
   Processes and cleans the generated reviews, adding variations and removing artifacts.

6. **Validate Patterns**:
   ```bash
   python patternvalidation.py
   ```
   Analyzes the generated data for expected patterns and creates visualizations in the `vizzes/` directory.

## Final Results

The scripts produce several key files:

- `transactions.csv`: 10,000 synthetic transactions with fields like client info, destination, dates, costs, agency hours/fees, and profitability.
- `generated_reviews.csv`: Synthetic customer reviews linked to transactions.
- `cleaned_reviews.csv`: Processed and cleaned review data.
- `vizzes/`: Directory containing validation plots and analysis visualizations.

The datasets are designed to support various analyses including customer segmentation, seasonal trend analysis, profitability modeling, and sentiment analysis.

## Usage for Capstone Projects

This code serves as inspiration for creating synthetic datasets when real data is unavailable for capstone or mock projects. The modular approach allows adaptation to different domains by modifying the generation parameters and rules. Focus on embedding realistic correlations and trends to create datasets that yield meaningful insights during analysis.