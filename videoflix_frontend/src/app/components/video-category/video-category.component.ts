import { Component, Input } from '@angular/core';
import { MovieCarouselComponent } from '../movie-carousel/movie-carousel.component';

@Component({
  selector: 'app-video-category',
  standalone: true,
  imports: [MovieCarouselComponent],
  templateUrl: './video-category.component.html',
  styleUrl: './video-category.component.scss',
})
export class VideoCategoryComponent {
  @Input({ required: true }) videos: any[] = []; //to be changed to normal type, only test
  @Input({ required: true }) categoryTitle: string | null = null;
}
