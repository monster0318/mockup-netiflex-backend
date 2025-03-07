import { Component, inject, OnInit } from "@angular/core";
import { NavigationEnd, Router, RouterOutlet } from "@angular/router";
import { RequestsService } from "./services/requests.service";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: "./app.component.html",
  styleUrl: "./app.component.scss",
})
export class AppComponent implements OnInit {
  title = "videoflix_frontend";
  token: string | null = null;
  private router = inject(Router);

  constructor(private requestsService: RequestsService) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        window.scrollTo({ top: 0, behavior: "smooth" }); // Smooth scrolling
      }
    });
  }

  ngOnInit(): void {
    this.token = sessionStorage.getItem("token");
    if (this.token) {
      this.requestsService.getData("api/videos", this.token, data => this.requestsService.emitVideos(data));
      this.requestsService.getData("api/videos/categorized_videos/", this.token, data => this.requestsService.emitCategorizedVideos(data));
      this.requestsService.getData("api/videos/recent_videos", this.token, data => this.requestsService.emitRecentVideos(data));
    }
  }
}
