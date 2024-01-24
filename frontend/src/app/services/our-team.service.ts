import { Injectable } from '@angular/core';

export interface Member {
  name: string;
  image_path: string;

}

@Injectable({
  providedIn: 'root'
})
export class OurTeamService {
  public members: Member[] = [
    {name: 'Vladimir Gurovic', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Boris Kiva', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Vladimir Shaklein', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Seraphim Lobanov', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Michel Countryside', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Michel Lichmanov', image_path: 'assets/our_team_photos/boris.png' },
    {name: 'Maria Bessolova', image_path: 'assets/our_team_photos/boris.png' },
  ]

  constructor() { }
}
