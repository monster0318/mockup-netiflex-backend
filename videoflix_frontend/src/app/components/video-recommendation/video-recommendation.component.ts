import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-video-recommendation',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video-recommendation.component.html',
  styleUrl: './video-recommendation.component.scss',
})
export class VideoRecommendationComponent {
  @Input({ required: true }) recommendedVideos: any[] = [];

  // recommendedVideos: any[] = [
  //   {
  //     title: 'Interstellar',
  //     duration: '02:30',
  //     image: 'assets/videos/the_5th_wave_poster.jpg',
  //   },
  //   {
  //     title: 'Avengers: Endgame',
  //     duration: '02:30',
  //     image: 'assets/videos/the_5th_wave_poster.jpg',
  //   },
  //   {
  //     title: 'Dune',
  //     duration: '02:30',
  //     image: 'assets/videos/the_5th_wave_poster.jpg',
  //   },
  // ];
}
