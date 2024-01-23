import {Component, AfterViewInit, HostListener } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements AfterViewInit {
  public svg_filenames = [
    'assets/logos_for_main_page/csharp.svg',
    'assets/logos_for_main_page/c++.svg',
    'assets/logos_for_main_page/c.svg',
    'assets/logos_for_main_page/go.svg',
    'assets/logos_for_main_page/java.svg',
    'assets/logos_for_main_page/js.svg',
    'assets/logos_for_main_page/kotlin.svg',
    'assets/logos_for_main_page/python.svg',
    'assets/logos_for_main_page/rust.svg',
    'assets/logos_for_main_page/ts.svg',
  ]

  constructor(
    public router: Router,
    private route: ActivatedRoute,
  ) { }

  ngAfterViewInit(): void {
    let vertical_01_lines = document.getElementsByClassName('vertical-line')!;
    for (let i = 0; i < vertical_01_lines.length; i++) {
      let line_content = this.generate_01_text_line();
      console.log(line_content);
      // @ts-ignore
      vertical_01_lines[i].innerText = line_content;
    }

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

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        let class_name = 'show';
        console.log(entry);
        if (entry.isIntersecting)
          entry.target.classList.add(class_name);
        else
          entry.target.classList.remove(class_name);
      });
    });
    const cards_observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        let class_name = 'little-card__show';
        console.log(entry);
        if (entry.isIntersecting)
          entry.target.classList.add(class_name);
        else
          entry.target.classList.remove(class_name);
      });
    });

    const hiddenElements = document.querySelectorAll('.hidden');
    const hiddenCards = document.querySelectorAll('.little-card__hide');
    hiddenElements.forEach((el) => observer.observe(el));
    hiddenCards.forEach((el) => cards_observer.observe(el));
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
