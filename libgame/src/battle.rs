use std::string::String;
use std::io::{self, Stdin, Stdout, Write};

use serde_json::json;
use serde::{Deserialize, Serialize};

use indexmap::IndexMap;


type Player = i32;

pub trait Read {
    fn read_line(&mut self, buffer: &mut String) -> io::Result<usize>;
}


impl Read for Stdin {
    fn read_line(&mut self, buffer: &mut String) -> io::Result<usize> {
        Ok(buffer.len())
    }
}

#[derive(PartialEq, Debug, Serialize, Deserialize)]
pub struct PlayerMove {
    player: Player,
    data: String
}

#[derive(PartialEq, Debug)]
pub struct Battle<R: Read, W: Write> {
    pub num_players: i32,
    points: IndexMap<Player, i32>,

    stdin: R,
    stdout: W
}

impl<R: Read, T: Write> Battle<R, T> {
    pub fn new(num_players: i32) -> Battle<Stdin, Stdout> {
        let mut points = IndexMap::new();
        for player in 0..num_players {
            points.insert(player+1, 0);
        }

        Battle {
            num_players,
            points,

            stdin: io::stdin(),
            stdout: io::stdout(),
        }
    }

    pub fn send_to(&mut self, player: Player, data: &str) {
        let output = json!({"type": "state", "player": player, "data": data}).to_string();
        writeln!(self.stdout, "{}", output).unwrap();
    }

    pub fn wait(&mut self) -> PlayerMove {
        let mut input = String::new();
        self.stdin.read_line(&mut input).expect("Failed to parse input!");
        serde_json::from_str(&input).unwrap()
    }

    pub fn wait_for(&mut self, player: Player) -> PlayerMove {
        loop {
            let player_move = self.wait();
            if player_move.player == player {
                return player_move
            }
        }
    }

    pub fn set_points(&mut self, player: Player, count: i32) {
        self.points.insert(player, count);
    }

    pub fn add_points(&mut self, player: Player, count: i32) {
        let points = self.points.get(&player).unwrap_or(&0);
        self.points.insert(player, points + count);
    }

    pub fn end(&mut self) {
        self.points.sort_keys();
        let output = json!({"type": "end", "points": self.points.values().cloned().collect::<Vec<i32>>()}).to_string();
        write!(self.stdout, "{}", output).unwrap();
    }
}

#[cfg(test)]
mod tests;
