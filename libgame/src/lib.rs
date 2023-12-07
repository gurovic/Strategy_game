mod battle;

use std::io::{Stdin, Stdout};
use battle::Battle;
use clap::Parser;



#[derive(Parser)]
pub struct Cli {
    players: i32
}

fn get_battle_from_cli(args: Cli) -> Battle<Stdin, Stdout> {
    Battle::<Stdin, Stdout>::new(args.players)
}

pub fn get_battle() -> Battle<Stdin, Stdout> {
    get_battle_from_cli(Cli::parse())
}

#[cfg(test)]
mod tests;