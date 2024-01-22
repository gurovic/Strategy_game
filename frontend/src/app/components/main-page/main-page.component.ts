import {Component, AfterViewInit, HostListener } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements AfterViewInit {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  ngAfterViewInit(): void {
    let vertical_01_lines = document.getElementsByClassName('vertical-line')!;
    for (let i = 0; i < vertical_01_lines.length; i++) {
      // @ts-ignore
      vertical_01_lines[i].innerText=this.generate_01_text_line();
    }
    console.log(1);

    addEventListener("scroll", (event)=>{
      console.log(1);
      for (let i = 0; i < vertical_01_lines.length; i++) {
        let element = vertical_01_lines[i];
        let y = window.scrollY;
        console.log(y);
        // @ts-ignore
        element.style.top = `${y*2}px`
      }
    })
  }



  getRandomInt(max:number): number {
    return Math.floor(Math.random() * max);
  }

  generate_01_text_line() {
    let result = "";
    for (let i = 0; i < 200; i++) {
      if (this.getRandomInt(2) == 0) result+="0";
      else result+="1";
    }
    // this.cdr.detectChanges();
    return result;
  }
}
