export interface GameModel {
    id?: number;
    name?: string;
    number_of_players?: string;
    ideal_solution?: any;
    play?: any;
    compiled_play?: any;
    win_points?: number;
    lose_points?: number;
    visualizer?: any;
    rules?: string;
}