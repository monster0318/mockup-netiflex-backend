import { CommonModule } from "@angular/common";
import { Component, Input } from "@angular/core";

@Component({
  selector: "app-video-recommendation",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./video-recommendation.component.html",
  styleUrl: "./video-recommendation.component.scss",
})
export class VideoRecommendationComponent {
  @Input({ required: true }) recommendedVideos: any[] = [];
}
