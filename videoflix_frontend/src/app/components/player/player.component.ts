import { CommonModule } from "@angular/common";
import { Component, ElementRef, ViewChild, OnDestroy, ViewEncapsulation, Input } from "@angular/core";
import Plyr from "plyr";
import { Video } from "../../modules/interfaces";
import { RequestsService } from "../../services/requests.service";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-player",
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: "./player.component.html",
  styleUrl: "./player.component.scss",
  encapsulation: ViewEncapsulation.None,
})
export class PlayerComponent {
  vid: Video[] = [];
  plyrConfig: string = "";
  token: string | null = null;
  currentVideo: Video | null = null;
  recentVideos: Video[] = [];
  recommendedVideos: Video[] = [];
  private storageKey = "video-progress";
  @ViewChild("videoPlayer", { static: true })
  videoElement!: ElementRef<HTMLVideoElement>;

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.videos$.subscribe(videos => {
      this.vid = videos;
    });

    this.requestsService.recentVideos$.subscribe(videos => {
      this.recentVideos = videos;
    });

    this.requestsService.currentVideos$.subscribe(video => {
      this.currentVideo = video;
      console.log("Current video:", this.currentVideo);
    });
  }

  private player!: Plyr;

  ngAfterViewInit() {
    this.player = new Plyr(this.videoElement.nativeElement, {
      captions: { active: true },
      quality: {
        default: 720,
        options: [1080, 720, 480, 360, 240],
      },
    });

    (window as any).player = this.player;

    /**
     * Saave view state
     */
    this.player.on("timeupdate", () => {
      localStorage.setItem(this.storageKey, this.player.currentTime.toString());
    });

    /**
     * restore state
     */
    const lastTime = localStorage.getItem(this.storageKey);
    if (lastTime) {
      this.player.once("loadedmetadata", () => {
        this.player.currentTime = parseFloat(lastTime!);
      });
    }

    /**
     * clear after end video
     */
    this.player.on("ended", () => {
      localStorage.removeItem(this.storageKey);
    });
  }

  //   this.player.on('timeupdate', () => {
  //     localStorage.setItem('video-progress', this.player.currentTime);
  // });

  updateRecentVideo(id: number) {
    this.token = sessionStorage.getItem("token");
    if (this.token) {
      this.requestsService.getData(`api/videos/${id}`, this.token, data => {
        this.requestsService.emitCurrentVideos(data);
      });
    }
  }
}
