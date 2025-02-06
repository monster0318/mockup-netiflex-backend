import { CommonModule } from '@angular/common';
import Plyr from 'plyr';
import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [CommonModule, NavBarComponent],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss',
})
export class VideoPlayerComponent implements AfterViewInit {
  @ViewChild('videoPlayer', { static: true })
  videoElement!: ElementRef<HTMLVideoElement>;

  private player!: Plyr;

  ngAfterViewInit() {
    this.player = new Plyr(this.videoElement.nativeElement, {
      captions: { active: true },
    });

    (window as any).player = this.player;
  }
}
