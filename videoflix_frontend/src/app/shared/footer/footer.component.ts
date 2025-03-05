import { Component, inject } from "@angular/core";
import { RouterLink } from "@angular/router";
import { RequestsService } from "../../services/requests.service";

@Component({
  selector: "app-footer",
  standalone: true,
  imports: [RouterLink],
  templateUrl: "./footer.component.html",
  styleUrl: "./footer.component.scss",
})
export class FooterComponent {
  private requestsService = inject(RequestsService);

  /**
   * Reset error state when user change route
   */
  resetError() {
    this.requestsService.resetErrorState();
  }
}
