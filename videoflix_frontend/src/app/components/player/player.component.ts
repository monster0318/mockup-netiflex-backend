import {
  Component,
  ElementRef,
  ViewChild,
  OnDestroy,
  AfterViewInit,
  ViewEncapsulation,
  Input,
} from '@angular/core';
import videojs from 'video.js';
import '@videojs/http-streaming';
import HlsQualitySelector from 'videojs-hls-quality-selector';
import 'videojs-hls-quality-selector';
import 'video.js/dist/video-js.css';

@Component({
  selector: 'app-player',
  standalone: true,
  imports: [],
  templateUrl: './player.component.html',
  styleUrl: './player.component.scss',
  encapsulation: ViewEncapsulation.None,
})
export class PlayerComponent implements OnDestroy {
  @ViewChild('target', { static: true }) target!: ElementRef;

  // See options: https://videojs.com/guides/options
  @Input() options!: any;

  player: any;

  constructor(private elementRef: ElementRef) {}

  // Instantiate a Video.js player OnInit
  ngOnInit() {
    this.player = videojs(
      this.target.nativeElement,
      {
        fluid: true,
        autoplay: false,
        responsive: true,
        aspectRatio: '16:9',
        width: 920,
        playbackRates: [0.5, 1, 1.5, 2],
        controls: true,
        sources: [
          {
            src: 'assets/videos/master.m3u8',
            type: 'application/x-mpegURL',
          },
        ],
      },
      () => {
        console.log('Player is ready!');
        console.log('Registered plugins:', Object.keys(videojs.getPlugins()));

        // Initialize the quality selector plugin if available
        if (this.player.hlsQualitySelector) {
          this.player.hlsQualitySelector({
            displayCurrentQuality: true,
          });
        } else {
          console.error('hlsQualitySelector plugin not found');
        }
      }
    );
  }
  // Dispose the player OnDestroy
  ngOnDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  }
}
