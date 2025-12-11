import pandas as pd

# Define division mappings for 2007-2009
divisions_2007_2009 = {
    'AL East': ['BAL', 'NYY', 'BOS', 'TB', 'TOR'],
    'AL Central': ['CLE', 'KC', 'CWS', 'MIN', 'DET'],
    'AL West': ['OAK', 'TEX', 'SEA', 'LAA' ]
}

# Function to select the division dictionary for 2007-2009
def get_division_dict(year):
    if 2007 <= year <= 2009:
        return divisions_2007_2009
    else:
        return None

# Loop through each season (2007 to 2009)
for year in range(2007, 2010):
    print(f"\nProcessing season: {year}")
    
    # Load the CSV for the current year, skipping the first two rows
    df = pd.read_csv(f'al_standings_{year}.csv', skiprows=2)

    # Extract team names (the first column after skipping the first two rows)
    teams = df['TEAMS'].tolist()

    # Initialize records for each year
    division_wins = {team: 0 for team in teams}
    division_losses = {team: 0 for team in teams}
    non_division_wins = {team: 0 for team in teams}
    non_division_losses = {team: 0 for team in teams}
    
    # Get the appropriate division mapping for this season
    divisions = get_division_dict(year)
    
    # Map teams to their divisions
    team_to_division = {team: div for div, teams in divisions.items() for team in teams}
    
    # Loop through each team's matchups
    for i, team in enumerate(teams):
        total_games = 0  # Initialize total games for each team
        for j, opponent in enumerate(teams):
            if i == j:  # Skip self-matchups
                continue

            # Extract record (e.g., "10-5")
            record = df.iloc[i, j + 1]

            if '--' in record:
                continue

            if record != '--':  # Skip invalid records
                wins, losses = map(int, record.split('-'))
                total_games += wins + losses  # Add to total games

                # Check if opponent is in the same division
                if team_to_division[team] == team_to_division[opponent]:
                    division_wins[team] += wins
                    division_losses[team] += losses
                else:
                    non_division_wins[team] += wins
                    non_division_losses[team] += losses

        # Add "vs AL" games to non-division totals
        al_record = df.iloc[i, -1]  # Access "vs AL" column
        if al_record != '--':
            al_wins, al_losses = map(int, al_record.split('-'))
            total_games += al_wins + al_losses  # Add to total games
            non_division_wins[team] += al_wins
            non_division_losses[team] += al_losses

        # Print total games processed for each team
        print(f"Total games processed for {team}: {total_games}")

        # Ensure the total games equals 162
        if total_games != 162:
            print(f"Warning: Total games for {team} is {total_games}, expected 162!")

    # Compile division and non-division records for this season
    division_records = pd.DataFrame({
        'Team': teams,
        'Division Wins': [division_wins[team] for team in teams],
        'Division Losses': [division_losses[team] for team in teams]
    })

    non_division_records = pd.DataFrame({
        'Team': teams,
        'Non-Division Wins': [non_division_wins[team] for team in teams],
        'Non-Division Losses': [non_division_losses[team] for team in teams]
    })

    # Save to separate CSVs for each year
    division_records.to_csv(f'divisions_al_{year}.csv', index=False)
    non_division_records.to_csv(f'non_divisions_al_{year}.csv', index=False)

    print(f"\nDivision and non-division records for {year} saved to CSV.")
