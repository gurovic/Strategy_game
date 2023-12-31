pub mod battle;

use std::io::{Stdin, Stdout};
use battle::Battle;
use std::env;


pub fn get_raw_battle(num_players: isize) -> Battle<Stdin, Stdout> {
    Battle::<Stdin, Stdout>::new(num_players)
}

pub fn get_battle() -> Battle<Stdin, Stdout> {
    let num_players: isize = env::args().last().unwrap().parse().expect("Should provide num of players!");
    get_raw_battle(num_players)
}

#[cfg(test)]
mod tests;