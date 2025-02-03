import { CommonModule } from '@angular/common';
import Plyr from 'plyr';
import Hls from 'hls.js';
import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [CommonModule],
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

    // Expose the player instance to the global window
    (window as any).player = this.player;
  }

  ////////////////////////////////////////////////////////////////////////////

  // @ViewChild('videoPlayer', { static: true })
  // videoElement!: ElementRef<HTMLVideoElement>;

  // private player!: Plyr;
  // private videoSrc = 'assets/videos/nature_480p.m3u8';

  // ngAfterViewInit() {
  //   const video = this.videoElement.nativeElement;

  //   // Initialize Plyr
  //   this.player = new Plyr(this.videoElement.nativeElement, {
  //     captions: { active: true, update: true },
  //     settings: ['captions', 'quality', 'speed'],
  //   });

  //   if (video.canPlayType('application/vnd.apple.mpegurl')) {
  //     video.src = this.videoSrc;
  //   } else if (Hls.isSupported()) {
  //     // Use hls.js to play .m3u8 video
  //     const hls = new Hls();
  //     hls.loadSource(this.videoSrc);
  //     hls.attachMedia(video);
  //   }
  // }
}
