import pandas as pd

# List of years you're working with
years = range(2007, 2025)

# Loop through each year
for year in years:
    print(f"Processing year: {year}")
    
    # Load the division and non-division records for AL and NL
    nl_division_df = pd.read_csv(f'divisions_nl_{year}.csv')
    al_division_df = pd.read_csv(f'divisions_al_{year}.csv')
    
    nl_non_division_df = pd.read_csv(f'non_divisions_nl_{year}.csv')
    al_non_division_df = pd.read_csv(f'non_divisions_al_{year}.csv')
    
    # Add columns for the league (NL or AL)
    nl_division_df['League'] = 'NL'
    al_division_df['League'] = 'AL'
    nl_non_division_df['League'] = 'NL'
    al_non_division_df['League'] = 'AL'
    
    # Concatenate the division and non-division data for AL and NL
    all_division_df = pd.concat([nl_division_df, al_division_df], ignore_index=True)
    all_non_division_df = pd.concat([nl_non_division_df, al_non_division_df], ignore_index=True)
    
    # Save the division data to CSV with the required format (MLB_DIVISION_YEAR.csv)
    all_division_df.to_csv(f'MLB_DIVISION_{year}.csv', index=False)
    print(f"Successfully saved MLB_DIVISION_{year}.csv.")
    
    # Save the non-division data to CSV with the required format (MLB_NON_DIVISION_YEAR.csv)
    all_non_division_df.to_csv(f'MLB_NON_DIVISION_{year}.csv', index=False)
    print(f"Successfully saved MLB_NON_DIVISION_{year}.csv.")
