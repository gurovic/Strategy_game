import {Component, OnInit} from '@angular/core';

export class ArchiveTask {
  public name?: string;
  public contributors?: number;
  public link?: string;
  public bg_path?: string;
  public tags?: string[];
}

@Component({
  selector: 'app-sandbox',
  templateUrl: './sandbox.component.html',
  styleUrls: ['./sandbox.component.scss']
})
export class SandboxComponent implements OnInit {
  public tasks_array: ArchiveTask[] = [
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: '/assets/background_svgs/task_backgrounds/img.png',
      tags: ['strategy', '2players'],
    },
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: '/assets/background_svgs/task_backgrounds/img.png',
      tags: ['strategy', '2players'],
    },
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: 'assets/background_svgs/task_backgrounds/img_2.png',
      tags: ['strategy', '2players'],
    },
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: 'assets/background_svgs/task_backgrounds/img_3.png',
      tags: ['strategy', '2players'],
    },
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: 'assets/background_svgs/task_backgrounds/img_4.png',
      tags: ['strategy', '2players'],
    },
    {
      name: "LOL Lovers",
      link: 'bruh',
      contributors: 2193,
      bg_path: 'assets/background_svgs/task_backgrounds/img_5.png',
      tags: ['strategy', '2players'],
    },
  ];

  constructor() {
  }

  ngOnInit(): void {
  }


}
