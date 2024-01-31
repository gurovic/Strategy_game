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
    {name: 'Vladimir Gurovic', image_path: 'assets/our_team_photos/boris.png', position: 'Team Lead' },
    {name: 'Boris Kiva', image_path: 'assets/our_team_photos/boris.png', position: 'FullStack dev' },
    {name: 'Vladimir Shaklein', image_path: 'assets/our_team_photos/boris.png', position: 'Backend dev' },
    {name: 'Seraphim Lobanov', image_path: 'assets/our_team_photos/boris.png', position: 'FullStack dev' },
    {name: 'Maria Bessolova', image_path: 'assets/our_team_photos/boris.png', position: 'Andrew user' },
    {name: 'Ilgizar Khazeev', image_path: 'assets/our_team_photos/boris.png', position: 'Thinker' },
    {name: 'Michel Countryside', image_path: 'assets/our_team_photos/boris.png', position: 'GPT-user' },
    {name: 'Michel Lichmanov', image_path: 'assets/our_team_photos/boris.png', position: 'still doing math' },
    {name: 'Dmitry Dubrov', image_path: 'assets/our_team_photos/boris.png', position: 'None' },
    {name: 'Dmitry Polov', image_path: 'assets/our_team_photos/boris.png', position: 'User haha' },
    {name: 'Alexandra Golubcova', image_path: 'assets/our_team_photos/boris.png', position: 'Thinker' },
  ]

  constructor() { }
}
