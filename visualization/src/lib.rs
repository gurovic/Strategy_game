use std::cmp::max;
use std::cmp::min;

#[derive(Debug, Clone)]
pub struct Frame {
    pub width: usize,
    pub height: usize,
    pub data: Vec<Vec<(i32,i32,i32)>>,
}

impl Frame {
    pub fn new(width: usize, height: usize, color: (i32,i32,i32)) -> Frame {
        let mut image: Vec<Vec<(i32, i32, i32)>> = vec![vec![color; height]; width];
        Frame {
            width: width,
            height: height,
            data: image,
        }
    }

    pub fn draw_line(&mut self, start_x: i32, start_y: i32, end_x: i32, end_y: i32, color: (i32,i32,i32)) {
        if (start_x-end_x).abs()>(start_y-end_y).abs() {
            for x in start_x..end_x {
                let y = (((x-start_x) as f32)*((end_y-start_y) as f32)/((end_x-start_x) as f32)+start_y as f32).round() as i32;
                if x >=0 && x < self.width as i32 && y >= 0 && y < self.height as i32{
                    self.data[x as usize][y as usize] = color;
                }
            }
        } else {
            for y in start_y..end_y {
                let x = (((y-start_y) as f32)*((end_x-start_x) as f32)/((end_y-start_y) as f32)+start_x as f32).round() as i32;
                if x >=0 && x < self.width as i32 && y >= 0 && y < self.height as i32{
                    self.data[x as usize][y as usize] = color;
                }
            }
        }
    }

    pub fn draw_circle(&mut self, x: i32, y: i32, radius: i32, color: (i32,i32,i32), fill: bool) {
        if fill==true {
            for i in (x-radius)..(x+radius) {
                for j in (y-radius)..(y+radius) {
                    if i >=0 && i < self.width as i32 && j >= 0 && j < self.height as i32 && (i-radius)*(i-radius) + (j-radius)*(j-radius) <= radius*radius{
                        self.data[i as usize][j as usize] = color;
                    }
                }
            }
        } else {
            for angle in 0..360 {
                let x1 = ((radius as f32)*(((angle as f32)*std::f32::consts::PI/180.0).cos())).round() as i32;
                let y1 = ((radius as f32)*(((angle as f32)*std::f32::consts::PI/180.0).sin())).round() as i32;
                if x1 >=0 && x1 < self.width as i32 && y1 >= 0 && y1 < self.height as i32{
                    self.data[x1 as usize][y1 as usize] = color;
                }
            }
        }
    }

    pub fn draw_rectangle(&mut self, x1: i32, y1: i32, x2: i32, y2: i32,color: (i32,i32,i32), fill: bool) {
        if fill == true {
            for x in (max(0,min(x1,x2)))..(min(self.width as i32 -1,max(x1,x2))) {
                for y in (max(0,min(y1,y2)))..(min(self.height as i32 -1,max(y1,y2))) {
                    self.data[x as usize][y as usize] = color;
                }
            }
        } else {
            for x in (max(0,min(x1,x2)))..(min(self.width as i32 -1,max(x1,x2))) {
                self.data[x as usize][(max(0,min(y1,y2))) as usize] = color;
                self.data[x as usize][(min(self.height as i32 -1,max(y1,y2))) as usize] = color;
            }
            for y in (max(0,min(y1,y2)))..(min(self.height as i32 -1,max(y1,y2))) {
                self.data[(max(0,min(x1,x2))) as usize][y as usize] = color;
                self.data[(min(self.width as i32 -1,max(x1,x2))) as usize][y as usize] = color;
            }
        }
    }
}

pub fn get_frame(width: usize, height: usize, color: (i32,i32,i32)) -> Frame {
    let img = Frame::new(width, height, color);
    //println!("{}",img.width);
    img
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn frame_creation() {
        let frame: Frame = Frame::new(10,20,(255,255,255));
        assert_eq!(frame.height, 20);
        assert_eq!(frame.width, 10);
        assert_eq!(frame.data[0][0].0, 255);
    }

    #[test]
    fn check_line_creation() {
        let mut frame: Frame = Frame::new(5,5,(255,255,255));
        frame.draw_line(0, 0, 4, 4, (0,0,0));
        //println!("{:?}",frame.data);
    }

    #[test]
    fn check_circle_creation() {
        let mut frame: Frame = Frame::new(10,20,(255,255,255));
        frame.draw_circle(2, 2, 5, (255,0,255), false);
        frame.draw_circle(2, 2, 5, (255,0,255), true);
    }

    #[test]
    fn check_rectangle_creation() {
        let mut frame: Frame = Frame::new(10,20,(255,255,255));
        frame.draw_rectangle(2, 2, 5, 5, (255,0,255), false);
        frame.draw_rectangle(2, 2, 5, 5, (255,0,255), true);
    }
}

