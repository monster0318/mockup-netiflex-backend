import { CommonModule } from '@angular/common';
import Plyr from 'plyr';
import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { VideoCategoryComponent } from '../video-category/video-category.component';
import { VideoRecommendationComponent } from '../video-recommendation/video-recommendation.component';
import { Video } from '../../modules/interfaces';
import { RequestsService } from '../../services/requests.service';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [
    CommonModule,
    NavBarComponent,
    VideoCategoryComponent,
    VideoRecommendationComponent,
  ],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss',
})
export class VideoPlayerComponent implements AfterViewInit, OnInit {
  @ViewChild('videoPlayer', { static: true })
  videoElement!: ElementRef<HTMLVideoElement>;

  vid: Video[] = [];

  videos: any[] = [
    {
      title: 'Inception',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'The Dark Knight',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Interstellar',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Avengers: Endgame',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Parasite',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Joker',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Spider-Man: No Way Home',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
    {
      title: 'Dune',
      duration: '02:30',
      image: 'assets/videos/the_5th_wave_poster.jpg',
    },
  ];

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.videos$.subscribe((videos) => {
      this.vid = videos;
      console.log(this.vid);
    });
  }

  private player!: Plyr;

  ngAfterViewInit() {
    this.player = new Plyr(this.videoElement.nativeElement, {
      captions: { active: true },
    });

    (window as any).player = this.player;
  }
}
