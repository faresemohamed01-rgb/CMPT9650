def clean_data():
  restaurant_violations_df_clean = restaurant_violations_df.copy()

  restaurant_violations_df_clean['ViolationText'] = restaurant_violations_df_clean['ViolationText'].fillna('Unknown')
  restaurant_violations_df_clean = restaurant_violations_df_clean.drop_duplicates()

  restaurant_violations_df_clean['InspectionDate'] = pd.to_datetime(restaurant_violations_df_clean['InspectionDate'])
  restaurant_violations_df_clean['Zip'] = restaurant_violations_df_clean['Zip'].astype(str).str[:5]  # Standardize zip codes

  restaurant_violations_df_clean['Year'] = restaurant_violations_df_clean['InspectionDate'].dt.year
  restaurant_violations_df_clean['Month'] = restaurant_violations_df_clean['InspectionDate'].dt.month
  restaurant_violations_df_clean['MonthName'] = restaurant_violations_df_clean['InspectionDate'].dt.month_name()
  restaurant_violations_df_clean['Quarter'] = restaurant_violations_df_clean['InspectionDate'].dt.quarter
  restaurant_violations_df_clean['DayOfWeek'] = restaurant_violations_df_clean['InspectionDate'].dt.day_name()
  restaurant_violations_df_clean['Season'] = restaurant_violations_df_clean['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
  })

return restaurant_violations_df_clean
