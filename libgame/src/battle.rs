use std::string::String;
use std::io::{self, Stdin, Stdout, Write};

use serde::{Deserialize, Serialize};

use indexmap::IndexMap;

type Player = isize;

pub trait Read {
    fn read_line(&mut self, buffer: &mut String) -> io::Result<usize>;
}


impl Read for Stdin {
    fn read_line(&mut self, buffer: &mut String) -> io::Result<usize> {
        Ok(buffer.len())
    }
}

#[derive(PartialEq, Debug, Serialize, Deserialize)]
struct PlayData {
    state: &'static str,
    player: Option<Player>,
    data: Option<&'static str>,
    points: Option<Vec<isize>>
}

#[derive(PartialEq, Debug, Serialize, Deserialize)]
pub struct PlayerMove {
    pub player: Player,
    pub data: String
}

#[derive(PartialEq, Debug)]
pub struct Battle<R: Read, W: Write> {
    pub num_players: isize,
    points: IndexMap<Player, isize>,

    stdin: R,
    stdout: W
}

impl<R: Read, T: Write> Battle<R, T> {
    pub fn new(num_players: isize) -> Battle<Stdin, Stdout> {
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

    pub fn send_to(&mut self, player: Player, data: &'static str) {
        let play_data = PlayData {
            state: "play",
            player: Some(player),
            data: Some(data),
            points: None,
        };
        let output = serde_json::to_string(&play_data).unwrap();
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

    pub fn set_points(&mut self, player: Player, count: isize) {
        self.points.insert(player, count);
    }

    pub fn add_points(&mut self, player: Player, count: isize) {
        let points = self.points.get(&player).unwrap_or(&0);
        self.points.insert(player, points + count);
    }

    fn end_battle(&mut self, data: Option<&'static str>) {
        self.points.sort_keys();
        let play_data = PlayData {
            state: "end",
            points: Some(self.points.values().cloned().collect::<Vec<isize>>()),
            player: None,
            data
        };
        let output = serde_json::to_string(&play_data).unwrap();
        write!(self.stdout, "{}", output).unwrap();
    }

    pub fn end_due(&mut self, data: &'static str) {
        self.end_battle(Some(data));
    }

    pub fn end(&mut self) {
        self.end_battle(None);
    }
}

#[cfg(test)]
mod tests;
