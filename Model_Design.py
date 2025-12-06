def get_violation_category(text):
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

def apply_model():
  restaurant_violations_df_clean = clean_data()

  # Apply violation categorizing to dataframe
  restaurant_violations_df_clean['ViolationCategory'] = restaurant_violations_df_clean['ViolationText'].apply(get_violation_category)

  # Calculate violation metrics per facility
  violations_per_facility = restaurant_violations_df_clean.groupby('FacilityID').agg({
      'ObjectId': 'count',
      'InspectionDate': ['min', 'max']
   }).reset_index()
  violations_per_facility.columns = ['FacilityID', 'TotalViolations', 'FirstInspection', 'LastInspection']


  # Merge total violations with main dataframe
  if 'TotalViolations' not in restaurant_violations_df_clean.columns:
    restaurant_violations_df_clean = restaurant_violations_df_clean.merge(
    violations_per_facility[['FacilityID', 'TotalViolations']],
    on='FacilityID',
    how='left')

  # Create risk score based on number of violations
  restaurant_violations_df_clean['RiskLevel'] = pd.cut(restaurant_violations_df_clean['TotalViolations'],
                                bins=[0, 2, 5, 10, float('inf')],
                                labels=['Low', 'Medium', 'High', 'Critical'])
