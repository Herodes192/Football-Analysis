-- Gil Vicente Tactical Intelligence Platform - Database Schema

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    api_team_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    logo VARCHAR(500),
    country VARCHAR(100),
    founded INTEGER,
    venue_name VARCHAR(255),
    venue_capacity INTEGER,
    is_gil_vicente INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_teams_api_id ON teams(api_team_id);
CREATE INDEX idx_teams_gil_vicente ON teams(is_gil_vicente);

-- Matches table
CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    api_fixture_id INTEGER UNIQUE NOT NULL,
    home_team_id INTEGER NOT NULL REFERENCES teams(id),
    away_team_id INTEGER NOT NULL REFERENCES teams(id),
    match_date TIMESTAMP NOT NULL,
    venue VARCHAR(255),
    referee VARCHAR(255),
    status VARCHAR(50),
    home_score INTEGER,
    away_score INTEGER,
    home_possession FLOAT,
    away_possession FLOAT,
    home_shots INTEGER,
    away_shots INTEGER,
    home_shots_on_target INTEGER,
    away_shots_on_target INTEGER,
    home_xg FLOAT,
    away_xg FLOAT,
    home_formation VARCHAR(20),
    away_formation VARCHAR(20),
    tactical_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_matches_fixture_id ON matches(api_fixture_id);
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_home_team ON matches(home_team_id);
CREATE INDEX idx_matches_away_team ON matches(away_team_id);

-- Tactical Profiles table
CREATE TABLE IF NOT EXISTS tactical_profiles (
    id SERIAL PRIMARY KEY,
    team_id INTEGER NOT NULL REFERENCES teams(id),
    primary_formation VARCHAR(20),
    secondary_formation VARCHAR(20),
    formation_frequency JSONB,
    possession_style FLOAT,
    build_up_speed FLOAT,
    defensive_line_height FLOAT,
    pressing_intensity FLOAT,
    width_of_attack FLOAT,
    key_strengths JSONB,
    key_weaknesses JSONB,
    home_performance_avg FLOAT,
    away_performance_avg FLOAT,
    attacking_patterns JSONB,
    defensive_patterns JSONB,
    matches_analyzed INTEGER DEFAULT 0,
    last_analysis_date TIMESTAMP,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tactical_profiles_team ON tactical_profiles(team_id);

-- Update triggers for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_matches_updated_at BEFORE UPDATE ON matches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tactical_profiles_updated_at BEFORE UPDATE ON tactical_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert Gil Vicente as default team
INSERT INTO teams (api_team_id, name, country, is_gil_vicente)
VALUES (228, 'Gil Vicente', 'Portugal', 1)
ON CONFLICT (api_team_id) DO NOTHING;
