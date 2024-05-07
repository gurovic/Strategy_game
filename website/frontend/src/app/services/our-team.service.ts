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
    {name: 'Владимир Гуровиц', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Team lead' },
    {name: 'Борис Кива', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Fustack dev' },
    {name: 'Владимир Шаклеин', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Project lead' },
    {name: 'Лобанос Серафим', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Backend dev' },
    {name: 'Бессолова Мария', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Shaklein user' },
    {name: 'Хазеев Ильгизар', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Smartphone Vivo' },
    {name: 'Загороднюк Михаил', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'GPT-user' },
    {name: 'Личманов Михаил', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'math is done' },
    {name: 'Дубров Дмитрий', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'BD lead' },
    {name: 'Палов Дмитрий', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'User' },
    {name: 'Голубцова Александра', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Thinker' },
    {name: 'Адаменко Мирослав', image_path: '/static/angular/assets/our_team_photos/boris.png', position: 'Thinker' },
  ]

  constructor() { }
}
