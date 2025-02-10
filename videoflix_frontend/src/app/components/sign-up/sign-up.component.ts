import { Component, inject } from '@angular/core';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { FooterComponent } from '../../shared/footer/footer.component';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { ActivatedRoute, Router } from '@angular/router';
import { RequestsService } from '../../services/requests.service';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [WrapperComponent, NavBarComponent, FooterComponent, FormsModule],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss',
})
export class SignUpComponent {
  email!: string;
  password!: string;
  confirmPassword!: string;
  icon: string = 'visibility.svg';
  type: string = 'password';
  icon_confirm: string = 'visibility.svg';
  type_confirm: string = 'password';

  private apiService = inject(ApiService);
  private requestsService = inject(RequestsService);
  constructor(private router: Router, private route: ActivatedRoute) {}

  /**
   * this function allow the user to toggle password view
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

  /**
   * this function allow the user to toggle confirm password view
   */
  showConfirmPassword() {
    if (this.confirmPassword && this.type_confirm === 'password') {
      this.type_confirm = 'text';
      this.icon_confirm = 'visibility_off.svg';
    } else if (this.confirmPassword && this.type_confirm === 'text') {
      this.type_confirm = 'password';
      this.icon_confirm = 'visibility.svg';
    }
  }

  signUp() {
    this.requestsService.postData(
      'register/',
      {
        email: this.email,
        password: this.password,
        confirm_password: this.confirmPassword,
      },
      this.apiService.getUnAuthHeaders(),
      () => {
        this.requestsService.goToPage('/login');
      }
    );
  }
}
