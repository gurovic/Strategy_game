use pyo3::prelude::*;

use visualization_rust::{Frame as Frame_rust};
use visualization_rust::get_frame as get_frame_rust;

#[pyclass]
struct Frame {
    frame: Frame_rust,
}

impl Frame {
    fn new(frame: Frame_rust) -> Frame {
        Frame {
            frame,
        }
    }
}

#[pymethods]
impl Frame {
    #[getter]
    pub fn data(&self) -> PyResult<Vec<Vec<(i32,i32,i32)>>> {
        Ok(self.frame.data.clone())
    }

    pub fn draw(&mut self, x: i32, y: i32, color: (i32, i32, i32)) {
        self.frame.draw(x, y, color);
    }
    
    pub fn draw_line(&mut self, start_x: i32, start_y: i32, end_x: i32, end_y: i32, color: (i32,i32,i32)) {
        self.frame.draw_line(start_x, start_y, end_x, end_y, color);
    }

    pub fn draw_circle(&mut self, x: i32, y: i32, radius: i32, color: (i32,i32,i32), fill: bool) {
        self.frame.draw_circle(x, y, radius, color, fill);
    }

    pub fn draw_rectangle(&mut self, x1: i32, y1: i32, x2: i32, y2: i32,color: (i32,i32,i32), fill: bool) {
        self.frame.draw_rectangle(x1, y1, x2, y2, color, fill);
    }

}

#[pyfunction]
fn get_frame(width: usize, height: usize, color: (i32,i32,i32)) -> PyResult<Py<Frame>> {
    let frame = get_frame_rust(width,height,color);
    Ok(Python::with_gil(|py| Py::new(py, Frame::new(frame)).unwrap()))
}

#[pymodule]
fn visualization(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_frame, m)?)?;
    m.add_class::<Frame>()?;
    Ok(())
}
