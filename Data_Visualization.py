# Plot violation distribution by category
plt.figure(figsize=(12, 6))
violation_counts = restaurant_violations_df_clean['ViolationCategory'].value_counts()
ax = violation_counts.plot(kind='bar', color='steelblue')
plt.title('Distribution of Violation Types', fontsize=16, fontweight='bold')
plt.xlabel('Violation Category', fontsize=12)
plt.ylabel('Number of Violations', fontsize=12)
plt.xticks(rotation=45, ha='right')
for violation, violation_count in enumerate(violation_counts):
    ax.text(violation, violation_count + 50, str(violation_count), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Plot top 10 cities with the most violations
plt.figure(figsize=(12, 6))
city_violations = restaurant_violations_df_clean['City'].value_counts().head(10)
city_violations.plot(kind='barh', color='coral')
plt.title('Top 10 Cities by Violation Count', fontsize=16, fontweight='bold')
plt.xlabel('Number of Violations', fontsize=12)
plt.ylabel('City', fontsize=12)
plt.tight_layout()
plt.show()

# Plot seasonal trends
plt.figure(figsize=(12, 6))
# Group by season, and then count individual violations
seasonal_violations = restaurant_violations_df_clean.groupby('Season')['ObjectId'].count().reindex(['Spring', 'Summer', 'Fall', 'Winter'])
seasonal_violations.plot(kind='bar', color=['green', 'orange', 'brown', 'blue'])
plt.title('Violations by Season', fontsize=16, fontweight='bold')
plt.xlabel('Season', fontsize=12)
plt.ylabel('Number of Violations', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Repeat offenders
plt.figure(figsize=(12, 6))
# Group by facility name, and then count individual violations
top_offenders = restaurant_violations_df_clean.groupby('FacilityName')['ObjectId'].count().sort_values(ascending=False).head(15)
top_offenders.plot(kind='barh', color='crimson')
plt.title('Top 15 Facilities by Violation Count', fontsize=16, fontweight='bold')
plt.xlabel('Number of Violations', fontsize=12)
plt.ylabel('Facility Name', fontsize=12)
plt.tight_layout()
plt.show()

# Plot time trend analysis
# Group by year and month so that each point is a month within the year
monthly_trend = restaurant_violations_df_clean.groupby(['Year', 'Month'])['ObjectId'].count().reset_index()
monthly_trend['Date'] = pd.to_datetime(monthly_trend[['Year', 'Month']].assign(day=1))
plt.figure(figsize=(14, 6))
plt.plot(monthly_trend['Date'], monthly_trend['ObjectId'], marker='o', linewidth=2, color='darkblue')
plt.title('Violation Trends Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Violations', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Plot violation category by season
plt.figure(figsize=(12, 8))
season_category = pd.crosstab(restaurant_violations_df_clean['Season'], restaurant_violations_df_clean['ViolationCategory'])
sns.heatmap(season_category, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Count'})
plt.title('Violation Categories by Season', fontsize=16, fontweight='bold')
plt.xlabel('Violation Category', fontsize=12)
plt.ylabel('Season', fontsize=12)
plt.tight_layout()
plt.show()


# Calculate key statistic for insights
critical_risk_facilities = len(violations_per_facility[violations_per_facility['TotalViolations'] > 10])

print(f"The number of Critical Risk Faciltiies is {critical_risk_facilities:,}")
print(f"Critical Risk Facilities account for {critical_risk_facilities/(restaurant_violations_df_clean['FacilityID'].nunique()):.0%} of total facilities")
