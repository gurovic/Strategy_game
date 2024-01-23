import { Component, OnInit } from '@angular/core';

export class Task {
  public name?: string;
  public contributors?: number;
  public link?: string;

}

@Component({
  selector: 'app-sandbox',
  templateUrl: './sandbox.component.html',
  styleUrls: ['./sandbox.component.scss']
})
export class SandboxComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
