import {AfterViewInit, Component, Input} from '@angular/core';
import {Router} from "@angular/router";
import {SandboxTaskInterface} from "../../../interface/sandbox_task";

@Component({
  selector: 'app-archive-task',
  templateUrl: './archive-task.component.html',
  styleUrls: ['./archive-task.component.scss']
})
export class ArchiveTaskComponent implements AfterViewInit {
  @Input()
  public task: SandboxTaskInterface = {};

  constructor(
      private router: Router,
  ) {
  }

  ngAfterViewInit(): void {
    //   setting random background for 'mini-card__item'
    let items = document.getElementsByClassName('mini-card__item')!;
    const backgrounds = [
      '#9a06d5', '#342ef8', '#e317a8', '#0ed738',
      '#07a6e0', '#0217fd', '#06d560', '#d506c4',
    ];
    const color = [
      0, 0, 1, 1,
      1, 0, 1, 0,
    ]
    for (let i = 0; i < items.length; i++) {
      let item = items[i];
      let index = Math.floor(Math.random() * backgrounds.length)
      let clr = (color[index] == 1 ? 'var(--background-ddark)' : 'var(--text-white)');
      // @ts-ignore
      item.style.background = backgrounds[index];
      // @ts-ignore
      item.style.color = clr;
    }
  }

  go(id: number) {
    this.router.navigate(['sandbox/task/'+id]);
  }

}
