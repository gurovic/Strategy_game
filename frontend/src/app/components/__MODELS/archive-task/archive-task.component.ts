import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-archive-task',
  templateUrl: './archive-task.component.html',
  styleUrls: ['./archive-task.component.scss']
})
export class ArchiveTaskComponent implements OnInit {
  @Input()
  public task_name?:string;
  @Input()
  public link?:string;

  constructor() { }

  ngOnInit(): void {
  }

}
