import { CommonModule } from "@angular/common";
import { Component, inject, Input, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { ApiService } from "../../services/api.service";
import { RequestsService } from "../../services/requests.service";

@Component({
  selector: "app-nav-bar",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./nav-bar.component.html",
  styleUrl: "./nav-bar.component.scss",
})
export class NavBarComponent implements OnInit {
  @Input({ required: true }) logo: string = "";
  @Input() logOut: string = "";
  @Input() btnText: string = "Log in";
  @Input() isAuthenticated: boolean = false;
  @Input() is_watching: boolean = false;
  @Input() login: boolean = false;
  @Input() isPlayerNav: boolean = false;
  token: string | null = null;

  private requestsService = inject(RequestsService);
  constructor(private router: Router, private apiService: ApiService) {}
  ngOnInit(): void {
    this.isAuthenticated = this.apiService.isAuthenticated();
  }

  /**
   * Get the icon or image path
   * @returns (url : string) - src path of the icon
   */
  getImagePath(imageName: string) {
    return "assets/img/" + imageName;
  }

  /**
   * Action when user click on the videoflix logo
   * User stayed in video view when logged in or go to log in
   */
  onReturnToStartPage() {
    if (this.isAuthenticated) {
      this.router.navigateByUrl("/video-offer");
    } else {
      this.router.navigateByUrl("/login");
    }
    this.requestsService.resetErrorState();
  }

  /**
   * Log the guest user out and redirect to login page
   */
  logUserInOrOut() {
    if (this.btnText === "Log out") {
      this.removeGuestAccountOnLogout();
    }
    this.requestsService.resetErrorState();
    this.router.navigateByUrl("/login");
  }

  /**
   * Remove guest account on logout
   */
  removeGuestAccountOnLogout() {
    this.token = sessionStorage.getItem("token");
    if (this.token) {
      this.apiService.deleteData("logout/", this.token).subscribe({
        next: response => {
          console.log(response ? response : "Guest User logged out");
        },
        complete: () => {
          sessionStorage.removeItem("token");
        },
      });
    }
  }
}
