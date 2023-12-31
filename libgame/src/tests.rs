use super::*;

#[test]
fn get_battle_test() {
    assert_eq!(get_raw_battle(5).num_players, 5);
}