import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { RouterLink } from '@angular/router';
import { RequestsService } from '../../services/requests.service';
import { SpinnerComponent } from '../../shared/spinner/spinner.component';
import { VideoCategoryComponent } from '../video-category/video-category.component';
import { Video } from '../../modules/interfaces';

@Component({
  selector: 'app-video-offer',
  standalone: true,
  imports: [
    NavBarComponent,
    RouterLink,
    SpinnerComponent,
    VideoCategoryComponent,
  ],
  templateUrl: './video-offer.component.html',
  styleUrl: './video-offer.component.scss',
})
export class VideoOfferComponent implements AfterViewInit, OnInit {
  isLoading: boolean = false;
  recentVideos: Video[] | [] = [];
  token: string | null = null;
  currentVideo: Video | null = null;

  @ViewChild('backgroundVideo') backgroundVideo!: ElementRef<HTMLVideoElement>;

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.isLoading$.subscribe((value) => {
      this.isLoading = value;
    });
    this.requestsService.recentVideos$.subscribe((videos) => {
      this.recentVideos = videos;
    });

    this.requestsService.currentVideos$.subscribe((video) => {
      this.currentVideo = video;
      console.log('Current Offer video:', this.currentVideo);
    });
  }

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

  /**
   * slowing down the motion of the background video
   */
  ngAfterViewInit(): void {
    if (this.backgroundVideo?.nativeElement) {
      this.backgroundVideo.nativeElement.playbackRate = 0.5;
    }
  }

  updateRecentVideo() {
    this.token = sessionStorage.getItem('token');
    if (this.token) {
      this.requestsService.getData(`api/videos/49`, this.token, (data) => {
        this.requestsService.emitCurrentVideos(data);
      });
      console.log('Current Offers video:', this.currentVideo);
    }
  }
}
