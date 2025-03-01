import { MenuLink, VideoData } from './interfaces';

export class NavLinks {
  links: MenuLink[] = [
    {
      icon: 'user.svg',
      text: 'username',
    },
  ];
}

export class VideoJsonData {
  videos: VideoData[] = [
    {
      title: 'The 5th Wave',
      duration: '02:30',
      poster: 'the_5th_wave_poster.jpg',
    },
  ];
}
