import { Component, Input } from '@angular/core';
import { MovieCarouselComponent } from '../movie-carousel/movie-carousel.component';
import { Video } from '../../modules/interfaces';

@Component({
  selector: 'app-video-category',
  standalone: true,
  imports: [MovieCarouselComponent],
  templateUrl: './video-category.component.html',
  styleUrl: './video-category.component.scss',
})
export class VideoCategoryComponent {
  @Input({ required: true }) videos: Video[] = [];
  @Input({ required: true }) categoryTitle: string | null = null;
}
