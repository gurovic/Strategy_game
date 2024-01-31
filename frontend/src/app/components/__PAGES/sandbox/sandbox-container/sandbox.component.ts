import {Component, OnInit} from '@angular/core';
import {SandboxTaskInterface} from "../../../../interface/sandbox_task";
import {SandboxTasksService} from "../../../../services/api/sandbox-tasks.service";

@Component({
    selector: 'app-sandbox',
    templateUrl: './sandbox.component.html',
    styleUrls: ['./sandbox.component.scss']
})
export class SandboxComponent implements OnInit {
    public tasks_array:SandboxTaskInterface[] = [];

    constructor(
        private sandbox_tasks_service: SandboxTasksService,
    ) {
    }

    ngOnInit(): void {
        this.tasks_array = this.sandbox_tasks_service.getAll();
    }


}
