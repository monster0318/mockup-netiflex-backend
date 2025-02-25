import { CommonModule } from '@angular/common';
import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import Glide from '@glidejs/glide';
import { RouterLink } from '@angular/router';
import { RequestsService } from '../../services/requests.service';
import { Video } from '../../modules/interfaces';
@Component({
  selector: 'app-movie-carousel',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './movie-carousel.component.html',
  styleUrl: './movie-carousel.component.scss',
})
export class MovieCarouselComponent implements OnInit {
  @Input({ required: true }) videos: any[] = []; //to be changed to normal type, only test
  @ViewChild('glide') glideRef!: ElementRef;
  token: string | null = null;
  currentVideo: Video | null = null;

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.currentVideos$.subscribe((video) => {
      this.currentVideo = video;
    });
  }

  ngAfterViewInit() {
    new Glide(this.glideRef.nativeElement, {
      type: 'carousel',
      perView: 4,
      gap: 120,
      // autoplay: 3000,
      focusAt: 'center',
      hoverpause: true,
      breakpoints: {
        1315: { perView: 3 },
        768: { perView: 2 },
        480: { perView: 1.5 },
      },
    }).mount();
  }

  updateRecentVideo() {
    console.log('HALLLO');

    // this.token = sessionStorage.getItem('token');
    // if (this.token) {
    //   this.requestsService.getData(`api/videos/`, this.token, (data) => {
    //     this.requestsService.emitCurrentVideos(data);
    //   });
    //   console.log('Current Offers video:', this.currentVideo);
    // }
  }
}
