import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {SandboxTaskInterface} from "../../../../interface/sandbox_task";
import {SandboxTasksService} from "../../../../services/api/sandbox-tasks.service";

@Component({
  selector: 'app-task',
  templateUrl: './task-viewer.component.html',
  styleUrls: ['./task-viewer.component.scss']
})
export class TaskViewerComponent implements OnInit {
  public task: SandboxTaskInterface = {};

  constructor(
      private router: Router,
      private route: ActivatedRoute,
      private sandbox_task_service: SandboxTasksService,
  ) { }

  ngOnInit(): void {
    this.task = this.get_task();
  }

  get_task():SandboxTaskInterface {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    return this.sandbox_task_service.get(id);
  }
}
