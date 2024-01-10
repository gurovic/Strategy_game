use pyo3::prelude::*;

use libgame_core::{get_battle as get_battle_rust, get_raw_battle as get_raw_battle_rust};
use libgame_core::battle::{Battle as BattleRust, Player, PlayerMove as PlayerMoveRust};

use std::io::{Stdin, Stdout};


#[pyclass]
pub struct PlayerMove {
    pub player: Player,
    pub data: String
}

impl PlayerMove {
    fn from(player_move: PlayerMoveRust) -> PlayerMove {
        PlayerMove {
            player: player_move.player,
            data: player_move.data
        }
    }
}

#[pymethods]
impl PlayerMove {
    pub fn __str__(&self) -> String {
        format!("{{\"player\": {}, \"data\": \"{}\" }}", self.player, self.data)
    }
}


#[pyclass]
struct Battle {
    #[pyo3(get)]
    pub num_players: isize,

    battle: BattleRust<Stdin, Stdout>,
}

impl Battle {
    fn new(battle: BattleRust<Stdin, Stdout>) -> Battle {
        Battle {
            num_players: battle.num_players.clone(),
            battle,
        }
    }
}

#[pymethods]
impl Battle {
    pub fn send_to(&mut self, player: Player, data: &str) {
        self.battle.send_to(player, &data);
    }

    pub fn wait(&mut self) -> PyResult<Py<PlayerMove>> {
        let player_move = self.battle.wait();
        Ok(Python::with_gil(|py| Py::new(py, PlayerMove::from(player_move)).unwrap()))
    }

    pub fn wait_for(&mut self, player: Player) -> PyResult<Py<PlayerMove>> {
        let player_move = self.battle.wait_for(player);
        Ok(Python::with_gil(|py| Py::new(py, PlayerMove::from(player_move)).unwrap()))
    }

    pub fn set_points(&mut self, player: Player, count: isize) {
        self.battle.set_points(player, count);
    }

    pub fn add_points(&mut self, player: Player, count: isize) {
        self.battle.add_points(player, count);
    }

    pub fn end_due(&mut self, data: &str) {
        self.battle.end_due(data);
    }

    pub fn end(&mut self) {
        self.battle.end();
    }
}

#[pyfunction]
fn get_battle() -> PyResult<Py<Battle>> {
    let battle = get_battle_rust();
    Ok(Python::with_gil(|py| Py::new(py, Battle::new(battle)).unwrap()))
}


#[pymodule]
fn libgame(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_battle, m)?)?;
    Ok(())
}
