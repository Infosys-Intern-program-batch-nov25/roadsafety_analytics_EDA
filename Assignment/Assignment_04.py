import pandas as pd

# Load dataset
df = pd.read_csv("US_Accidents_March23.csv")

# Check dataset size
print(f"Total records: {len(df):,}")

# Randomly sample 1,000,000 rows
sample_df = df.sample(n=1_000_000, random_state=42)

# Save sampled dataset
sample_df.to_csv("US_Accidents_1M_sample.csv", index=False)

print("Sample saved as US_Accidents_1M_sample.csv")
