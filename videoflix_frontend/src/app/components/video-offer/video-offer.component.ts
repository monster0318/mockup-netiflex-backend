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

@Component({
  selector: 'app-video-offer',
  standalone: true,
  imports: [NavBarComponent, RouterLink, SpinnerComponent],
  templateUrl: './video-offer.component.html',
  styleUrl: './video-offer.component.scss',
})
export class VideoOfferComponent implements AfterViewInit, OnInit {
  isLoading: boolean = false;

  @ViewChild('backgroundVideo') backgroundVideo!: ElementRef<HTMLVideoElement>;

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.isLoading$.subscribe((value) => {
      this.isLoading = value;
    });
  }

  /**
   * slowing down the motion of the background video
   */
  ngAfterViewInit(): void {
    if (this.backgroundVideo?.nativeElement) {
      this.backgroundVideo.nativeElement.playbackRate = 0.5;
    }
  }
}
