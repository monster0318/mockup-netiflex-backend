import { AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild } from "@angular/core";
import { NavBarComponent } from "../../shared/nav-bar/nav-bar.component";
import { RouterLink } from "@angular/router";
import { RequestsService } from "../../services/requests.service";
import { SpinnerComponent } from "../../shared/spinner/spinner.component";
import { VideoCategoryComponent } from "../video-category/video-category.component";
import { Video } from "../../modules/interfaces";
import { CommonModule } from "@angular/common";

@Component({
  selector: "app-video-offer",
  standalone: true,
  imports: [NavBarComponent, RouterLink, SpinnerComponent, VideoCategoryComponent, CommonModule],
  templateUrl: "./video-offer.component.html",
  styleUrl: "./video-offer.component.scss",
})
export class VideoOfferComponent implements AfterViewInit, OnInit {
  isLoading: boolean = false;
  recentVideos: Video[] | [] = [];
  allVideos: Video[] | [] = [];
  rndVideo: Video | null = null;
  categorizedVideos:
    | { action: Video[]; horror: Video[]; drama: Video[]; documentary: Video[]; technic: Video[] }
    | { action: []; horror: []; drama: []; documentary: []; technic: [] } = { action: [], horror: [], drama: [], documentary: [], technic: [] };
  token: string | null = null;
  currentVideo: Video | null = null;
  intervalId: any;
  timeoutId: any;

  @ViewChild("backgroundVideo") backgroundVideo!: ElementRef<HTMLVideoElement>;

  constructor(private requestsService: RequestsService) {}

  ngOnInit(): void {
    this.requestsService.videos$.subscribe(videos => {
      this.allVideos = videos;
      console.log("All videos", this.allVideos);
      this.selectRandomVideo();
    });

    this.requestsService.isLoading$.subscribe(value => {
      this.isLoading = value;
    });

    this.requestsService.recentVideos$.subscribe(videos => {
      this.recentVideos = videos;
      console.log("recent Offer video:", this.recentVideos);
    });

    this.requestsService.currentVideos$.subscribe(video => {
      this.currentVideo = video;
      console.log("Current Offer video:", this.currentVideo);
    });

    this.requestsService.categorizedVideos$.subscribe(video => {
      this.categorizedVideos = video;
      console.log("categorized Offer video:", this.categorizedVideos);
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

  updateRecentVideo(id: number | undefined) {
    this.token = sessionStorage.getItem("token");
    if (this.token && this.rndVideo) {
      this.requestsService.getData(`api/videos/${id}`, this.token, data => {
        this.requestsService.emitCurrentVideos(data);
      });
    }
  }

  selectRandomVideo() {
    clearTimeout(this.timeoutId);
    const randomIndex = Math.floor(Math.random() * this.allVideos.length);
    this.rndVideo = this.allVideos[randomIndex];
    console.log("Random video", this.rndVideo);

    setTimeout(async () => {
      if (this.backgroundVideo && this.rndVideo?.video_file_hd1080) {
        const video = this.backgroundVideo.nativeElement;
        video.pause();
        video.src = this.rndVideo.video_file_hd1080;
        video.muted = true;
        video.load();

        try {
          await video.play();
        } catch (err) {
          console.error("Autoplay failed:", err);
        }

        video.onended = () => {
          this.selectRandomVideo();
        };

        const changeTime = Math.min(this.rndVideo.duration, 100) * 1000;
        this.timeoutId = setTimeout(() => {
          this.selectRandomVideo();
        }, changeTime);
      }
    }, 100);
  }
}
