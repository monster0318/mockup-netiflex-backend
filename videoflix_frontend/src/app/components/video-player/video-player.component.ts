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
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [
    CommonModule,
    NavBarComponent,
    VideoCategoryComponent,
    VideoRecommendationComponent,
    RouterLink,
  ],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss',
})
export class VideoPlayerComponent implements AfterViewInit, OnInit {
  @ViewChild('videoPlayer', { static: true })
  videoElement!: ElementRef<HTMLVideoElement>;
  token: string | null = null;
  currentVideo: Video | null = null;
  recentVideos: Video[] = [];
  recommendedVideos: Video[] = [];
  private storageKey = 'video-progress';

  vid: Video[] = [];
  plyrConfig: string = '';

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
    });

    this.requestsService.recentVideos$.subscribe((videos) => {
      this.recentVideos = videos;
    });

    this.requestsService.currentVideos$.subscribe((video) => {
      this.currentVideo = video;
      console.log('Current video:', this.currentVideo);
    });
  }

  private player!: Plyr;

  ngAfterViewInit() {
    this.player = new Plyr(this.videoElement.nativeElement, {
      captions: { active: true },
      quality: {
        default: 720,
        options: [1080, 720, 480, 360, 240],
      },
    });

    (window as any).player = this.player;

    /**
     * Saave view state
     */
    this.player.on('timeupdate', () => {
      localStorage.setItem(this.storageKey, this.player.currentTime.toString());
    });

    /**
     * restore state
     */
    const lastTime = localStorage.getItem(this.storageKey);
    if (lastTime) {
      this.player.once('loadedmetadata', () => {
        this.player.currentTime = parseFloat(lastTime!);
      });
    }

    /**
     * clear after end video
     */
    this.player.on('ended', () => {
      localStorage.removeItem(this.storageKey);
    });
  }

  //   this.player.on('timeupdate', () => {
  //     localStorage.setItem('video-progress', this.player.currentTime);
  // });

  updateRecentVideo(id: number) {
    this.token = sessionStorage.getItem('token');
    if (this.token) {
      this.requestsService.getData(`api/videos/${id}`, this.token, (data) => {
        this.requestsService.emitCurrentVideos(data);
      });
    }
  }

  // nextVideos() {
  //   this.token = sessionStorage.getItem('token');
  //   if (this.token) {
  //     this.requestsService.getData(
  //       `api/videos/${this.currentVideo?.id}`,
  //       this.token,
  //       (data) => {
  //         this.recommendedVideos;
  //       }
  //     );
  //   }
  // }
}
