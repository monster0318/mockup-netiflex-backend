import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from '../../shared/footer/footer.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { RequestsService } from '../../services/requests.service';
import { CommonModule } from '@angular/common';
import { GuestCredentials } from '../../modules/config';

@Component({
  selector: 'app-log-in',
  standalone: true,
  imports: [
    FormsModule,
    FooterComponent,
    NavBarComponent,
    CommonModule,
    WrapperComponent,
    RouterLink,
  ],
  templateUrl: './log-in.component.html',
  styleUrl: './log-in.component.scss',
})
export class LogInComponent implements OnInit {
  password!: string;
  email!: string;
  rememberMe: boolean = false;
  icon: string = 'visibility.svg';
  type: string = 'password';
  errorMessage: string | null = null;
  errorType: string | null = null;

  private apiService = inject(ApiService);
  private requestsService = inject(RequestsService);
  constructor(private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.requestsService.errorMessage$.subscribe((message) => {
      this.errorMessage = message['message'][0];
      this.errorType = message['type'][0];
    });
  }
  /**
   * show entered password
   */
  showPassword() {
    if (this.password && this.type === 'password') {
      this.type = 'text';
      this.icon = 'visibility_off.svg';
    } else if (this.password && this.type === 'text') {
      this.type = 'password';
      this.icon = 'visibility.svg';
    }
  }

  onLogin() {
    this.requestsService.postData(
      'login/',
      { email: this.email, password: this.password },
      this.apiService.getUnAuthHeaders(),
      () => {
        this.requestsService.goToPage('/video-offer');
      }
    );
  }
  onGuestLogin() {
    const guest = new GuestCredentials();

    this.requestsService.postData(
      'login/',
      {
        email: guest.GUEST_CREDENTIALS['email'],
        username: guest.GUEST_CREDENTIALS['username'],
      },
      this.apiService.getUnAuthHeaders(),
      () => {
        this.requestsService.goToPage('/video-offer');
      }
    );
  }
}
