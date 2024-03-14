import { Injectable } from '@angular/core';

export interface Member {
  name: string;
  image_path: string;
  position: string;
}

@Injectable({
  providedIn: 'root'
})
export class OurTeamService {
  public members: Member[] = [
    {name: 'Vladimir Gurovic', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Team Lead' },
    {name: 'Boris Kiva', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'FullStack dev' },
    {name: 'Vladimir Shaklein', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Backend dev' },
    {name: 'Seraphim Lobanov', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'FullStack dev' },
    {name: 'Maria Bessolova', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Andrew user' },
    {name: 'Ilgizar Khazeev', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Thinker' },
    {name: 'Michel Countryside', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'GPT-user' },
    {name: 'Michel Lichmanov', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'still doing math' },
    {name: 'Dmitry Dubrov', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Postgres' },
    {name: 'Dmitry Palov', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'User' },
    {name: 'Alexandra Golubcova', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Thinker' },
  ]

  constructor() { }
}
