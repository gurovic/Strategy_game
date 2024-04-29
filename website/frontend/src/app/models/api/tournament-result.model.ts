export interface TournamentResult {
  tournament: {
    id: number;
    name: string;
  };
  playersInTournament: PlayerInTournament[];
}

export interface PlayerInTournament {
  player_id: number;
  tournament_id: number;
  place: number;
  number_of_points: number;
  file_solution: string;
  player_name: string;
}
