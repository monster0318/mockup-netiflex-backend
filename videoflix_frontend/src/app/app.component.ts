import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MovieCarouselComponent } from './components/movie-carousel/movie-carousel.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MovieCarouselComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'videoflix_frontend';
}
