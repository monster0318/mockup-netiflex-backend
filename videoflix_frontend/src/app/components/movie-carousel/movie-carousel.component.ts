import { CommonModule } from '@angular/common';
import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import Glide from '@glidejs/glide';
import { VideoData } from '../../modules/interfaces';
@Component({
  selector: 'app-movie-carousel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './movie-carousel.component.html',
  styleUrl: './movie-carousel.component.scss',
})
export class MovieCarouselComponent {
  @Input() videos: VideoData[] = [];
  @ViewChild('glide') glideRef!: ElementRef;

  movies = [
    {
      title: 'Inception',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'The Dark Knight',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Interstellar',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Avengers: Endgame',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Parasite',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Joker',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Spider-Man: No Way Home',
      image: 'assets/video_img/video_1.svg',
    },
    {
      title: 'Dune',
      image: 'assets/video_img/video_1.svg',
    },
  ];

  ngAfterViewInit() {
    new Glide(this.glideRef.nativeElement, {
      type: 'carousel',
      perView: 6,
      gap: 20,
      autoplay: 3000,
      hoverpause: true,
      breakpoints: {
        1024: { perView: 3 },
        768: { perView: 2 },
        480: { perView: 1 },
      },
    }).mount();
  }
}
