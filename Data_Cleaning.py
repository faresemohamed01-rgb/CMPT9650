# Create a copy for cleaning
restaurant_violations_df_clean = restaurant_violations_df.copy()

# Handle missing values
print("\nMissing values before cleaning:")
print(restaurant_violations_df_clean.isnull().sum())

# Fill ViolationText nulls with 'Unknown'
restaurant_violations_df_clean['ViolationText'] = restaurant_violations_df_clean['ViolationText'].fillna('Unknown')

print("\nMissing values after cleaning:")
print(restaurant_violations_df_clean.isnull().sum())

# Data type conversions
restaurant_violations_df_clean['InspectionDate'] = pd.to_datetime(restaurant_violations_df_clean['InspectionDate'])
restaurant_violations_df_clean['Zip'] = restaurant_violations_df_clean['Zip'].astype(str).str[:5]  # Standardize zip codes
restaurant_violations_df_clean['FacilityName'] = restaurant_violations_df_clean['FacilityName'].apply(
    lambda x: "Dunkin Donuts" if isinstance(x, str) and "dunkin" in x.lower() else x.title()
)

# Remove any duplicates
print(f"\nDuplicates found: {restaurant_violations_df_clean.duplicated().sum()}")
restaurant_violations_df_clean = restaurant_violations_df_clean.drop_duplicates()

# Data validation
print(f"\nDate range: {restaurant_violations_df_clean['InspectionDate'].min()} to {restaurant_violations_df_clean['InspectionDate'].max()}")
print(f"Unique facilities: {restaurant_violations_df_clean['FacilityID'].nunique()}")
print(f"Unique cities: {restaurant_violations_df_clean['City'].nunique()}")
