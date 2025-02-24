import { CommonModule } from '@angular/common';
import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import Glide from '@glidejs/glide';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-movie-carousel',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './movie-carousel.component.html',
  styleUrl: './movie-carousel.component.scss',
})
export class MovieCarouselComponent {
  @Input({ required: true }) videos: any[] = []; //to be changed to normal type, only test
  @ViewChild('glide') glideRef!: ElementRef;

  // ngAfterViewInit() {
  //   new Glide(this.glideRef.nativeElement, {
  //     type: 'carousel',
  //     perView: 4,
  //     gap: 90,
  //     autoplay: 3000,
  //     focusAt: 'center',
  //     hoverpause: true,
  //     breakpoints: {
  //       1024: { perView: 3 },
  //       768: { perView: 2 },
  //       480: { perView: 1 },
  //     },
  //   }).mount();
  // }
}
