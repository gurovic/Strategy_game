import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {SandboxTaskInterface} from "../../interface/sandbox_task";

const baseUrl = '/api/register/';

@Injectable({
    providedIn: 'root'
})
export class SandboxTasksService {
    public tasks_array: SandboxTaskInterface[] = [
        {
            id: 1,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
        {
            id: 2,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
        {
            id: 3,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
        {
            id: 4,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
        {
            id: 5,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
        {
            id: 6,
            name: "LOL Lovers",
            link: 'bruh',
            contributors: 2193,
            bg_path: 'assets/our_team_photos/boris.png',
            tags: ['strategy', '2players'],
        },
    ];

    constructor(private http: HttpClient) {
    }

    getAllFromApi(): Observable<SandboxTaskInterface[]> {
        return this.http.get<SandboxTaskInterface[]>(baseUrl);
    }

    getAll() {
        let local_storage_tasks_string = localStorage.getItem('sandbox-tasks')
        if (local_storage_tasks_string == null) {
            let tasks = this.tasks_array;
            // this.getAll().subscribe(
            //     response => {
            //         tasks = response;
            //     },
            //     error => {
            //         return {};
            //     }
            // );
            this.send_to_local_storage(tasks);
            return tasks;
        } else {
            return this.convert_from_string(local_storage_tasks_string);
        }
    }

    get(id: number): SandboxTaskInterface {
        let tasks: SandboxTaskInterface[] = this.getAll();

        for (const task of tasks)
            if (task.id == id)
                return task;
        return {};
    }

    convert_from_string(str: string): SandboxTaskInterface[] {
        let result: SandboxTaskInterface[] = [];

        let array = str.split('@');
        for (const i of array) {
            if (i=='') break;
            let a:string [] = i.split('#');
            let id = Number(a[0]);
            let name = a[1];
            let link = a[2];
            let contributors = Number(a[3]);
            let bg_path = a[4];
            let tags = a[5].split('$');
            tags.pop();

            result.push({
                id: id,
                name: name,
                link: link,
                contributors: contributors,
                bg_path: bg_path,
                tags: tags,
            })
            console.log(result);
        }

        return result;
    }

    send_to_local_storage(tasks: SandboxTaskInterface[]) {
        console.log(1);
        let res = "";
        for (const task of tasks) {
            res += String(task.id) + "#";
            res += task.name + "#";
            res += task.link + "#";
            res += String(task.contributors) + "#";
            res += task.bg_path + "#";
            for (const tag of task.tags!)
                res += tag + "$";
            res += "@";
        }
        localStorage.setItem('sandbox-tasks', res);
    }
}
