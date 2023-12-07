use super::*;

#[test]
fn get_battle_test() {
    assert_eq!(get_battle_from_cli(Cli::parse_from(["test", "5"])).num_players, 5);
}