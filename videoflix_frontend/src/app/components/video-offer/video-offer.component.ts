import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-video-offer',
  standalone: true,
  imports: [NavBarComponent, RouterLink],
  templateUrl: './video-offer.component.html',
  styleUrl: './video-offer.component.scss',
})
export class VideoOfferComponent implements AfterViewInit {
  @ViewChild('backgroundVideo') backgroundVideo!: ElementRef<HTMLVideoElement>;

  /**
   * slowing down the motion of the background video
   */
  ngAfterViewInit(): void {
    if (this.backgroundVideo?.nativeElement) {
      this.backgroundVideo.nativeElement.playbackRate = 0.5;
    }
  }
}
