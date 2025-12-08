# FEATURE ENGINEERING

# Extract date components from 'InspectionDate' for trend analysis
restaurant_violations_df_clean['Year'] = restaurant_violations_df_clean['InspectionDate'].dt.year
restaurant_violations_df_clean['Month'] = restaurant_violations_df_clean['InspectionDate'].dt.month
restaurant_violations_df_clean['MonthName'] = restaurant_violations_df_clean['InspectionDate'].dt.month_name()
restaurant_violations_df_clean['Quarter'] = restaurant_violations_df_clean['InspectionDate'].dt.quarter
restaurant_violations_df_clean['DayOfWeek'] = restaurant_violations_df_clean['InspectionDate'].dt.day_name()
restaurant_violations_df_clean['Season'] = restaurant_violations_df_clean['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter', # 12, 1, 2 is Winter
    3: 'Spring', 4: 'Spring', 5: 'Spring', # 3, 4, 5 is Spring
    6: 'Summer', 7: 'Summer', 8: 'Summer', # 6, 7, 8 is Summer
    9: 'Fall', 10: 'Fall', 11: 'Fall' # 9, 10, 11 is Fall
})

# Categorize violations based on the text
def categorize_violation(text):
    if pd.isna(text):
        return 'Unknown'

    text_lower = str(text).lower()

    # Temperature
    if any(word in text_lower for word in ['temperature', 'cold', 'hot', 'refrigerat', 'freez', 'thaw']):
        return 'Temperature Control'

    # Sanitation
    elif any(word in text_lower for word in ['sanitation', 'clean', 'dirty', 'wash', 'sanitiz']):
        return 'Sanitation'

    # Pest control
    elif any(word in text_lower for word in ['pest', 'rodent', 'insect', 'fly', 'roach', 'mouse', 'rat']):
        return 'Pest Control'

    # Employee hygiene
    elif any(word in text_lower for word in ['employee', 'hand', 'hygiene', 'glove', 'hair']):
        return 'Employee Hygiene'

    # Food storage
    elif any(word in text_lower for word in ['storage', 'shelf', 'container', 'label', 'date']):
        return 'Food Storage'

    # Food handling
    elif any(word in text_lower for word in ['cross-contaminat', 'raw', 'cooked', 'separate']):
        return 'Food Handling'

    # Facilities/Equipment
    elif any(word in text_lower for word in ['equipment', 'facility', 'floor', 'wall', 'ceiling', 'plumb']):
        return 'Facility/Equipment'

    else:
        return 'Other'

# Apply violation categorizing to dataframe
restaurant_violations_df_clean['ViolationCategory'] = restaurant_violations_df_clean['ViolationText'].apply(categorize_violation)

# Create total violations dataframe to calculate violation metrics per facility
violations_per_facility = restaurant_violations_df_clean.groupby('FacilityID').agg({
    'ObjectId': 'count',
    'InspectionDate': ['min', 'max']
}).reset_index()

# Rename columns
violations_per_facility.columns = ['FacilityID', 'TotalViolations', 'FirstInspection', 'LastInspection']


# Merge total violations with main dataframe
if 'TotalViolations' not in restaurant_violations_df_clean.columns:
    restaurant_violations_df_clean = restaurant_violations_df_clean.merge(
    violations_per_facility[['FacilityID', 'TotalViolations']],
    on='FacilityID',
    how='left')

# Create risk score based on number of violations and assigned intervals
restaurant_violations_df_clean['RiskLevel'] = pd.cut(restaurant_violations_df_clean['TotalViolations'],
                                bins=[0, 2, 5, 10, float('inf')],
                                labels=['Low', 'Medium', 'High', 'Critical'])

print("New Features Created:")
print(restaurant_violations_df_clean[['Year', 'Month', 'Season', 'ViolationCategory', 'TotalViolations', 'RiskLevel']].head())
