use std::fmt::Write;
use std::string::String;
use super::*;

struct TestWrite(Option<String>);

impl io::Write for TestWrite {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        if self.0.is_none() {
            self.0 = Some(unsafe { String::from_utf8_unchecked(Vec::from(buf))});
        }
        Ok(buf.len())
    }

    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

impl TestWrite {
    fn new() -> TestWrite {
        TestWrite(None)
    }

    fn assert(&self, string: &str) {
        assert_eq!(self.0.clone().unwrap(), string);
    }
}


struct TestRead(Vec<&'static str>);

impl Read for TestRead {
    fn read_line(&mut self, buf: &mut String) -> io::Result<usize> {
        buf.write_str(self.0.remove(0)).unwrap();
        Ok(buf.len())
    }
}

#[test]
fn battle_new() {
    assert_eq!(Battle::<Stdin, Stdout>::new(3).points, IndexMap::from([(1, 0), (2, 0), (3, 0)]));
}

#[test]
fn battle_send_to() {
    let mut buffer = TestWrite::new();
    let mut battle = Battle {num_players: 3, points: IndexMap::from([(1, 2), (2, 4), (3, 6)]), stdin: io::stdin(), stdout: &mut buffer};
    battle.send_to(2, "test");

    buffer.assert("{\"data\":\"test\",\"player\":2,\"type\":\"state\"}");
}

#[test]
fn battle_wait() {
    let buffer = TestRead(vec!["{\"player\":2, \"data\":\"test\"}"]);

    let mut battle = Battle {num_players: 3, points: IndexMap::from([(1, 2), (2, 4), (3, 6)]), stdin: buffer, stdout: io::stdout()};
    assert_eq!(battle.wait(), PlayerMove { player: 2, data: String::from("test") });
}

#[test]
fn battle_wait_for() {
    let buffer = TestRead(vec!["{\"player\":2, \"data\":\"test\"}", "{\"player\":3, \"data\":\"test\"}"]);
    let mut battle = Battle {num_players: 3, points: IndexMap::from([(1, 2), (2, 4), (3, 6)]), stdin: buffer, stdout: io::stdout()};

    assert_eq!(battle.wait_for(3), PlayerMove { player: 3, data: String::from("test") });
}

#[test]
fn battle_set_points() {
    let mut battle = Battle::<Stdin, Stdout>::new(3);
    battle.set_points(2, 10);

    assert_eq!(*battle.points.get(&2).unwrap(), 10);
}

#[test]
fn battle_add_points() {
    let mut battle = Battle::<Stdin, Stdout>::new(3);
    battle.add_points(2, 2);
    battle.add_points(2, 3);

    assert_eq!(*battle.points.get(&2).unwrap(), 5);
}

#[test]
fn battle_add_points_remove() {
    let mut battle = Battle::<Stdin, Stdout>::new(3);
    battle.add_points(2, 10);
    battle.add_points(2, -4);

    assert_eq!(*battle.points.get(&2).unwrap(), 6);
}

#[test]
fn battle_end() {
    let mut buffer = TestWrite::new();

    let mut battle = Battle {num_players: 3, points: IndexMap::from([(1, 2), (2, 4), (3, 6)]), stdin: io::stdin(), stdout: &mut buffer};
    battle.end();

    buffer.assert("{\"points\":[2,4,6],\"type\":\"end\"}");
}