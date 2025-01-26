import { Component } from '@angular/core';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from '../../shared/footer/footer.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [WrapperComponent, FormsModule, FooterComponent, NavBarComponent],
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.scss',
})
export class ResetPasswordComponent {
  password!: string;
  confirmPassword!: string;
  icon: string = 'visibility.svg';
  type: string = 'password';
  icon_confirm: string = 'visibility.svg';
  type_confirm: string = 'password';

  showPassword() {
    if (this.password && this.type === 'password') {
      this.type = 'text';
      this.icon = 'visibility_off.svg';
    } else if (this.password && this.type === 'text') {
      this.type = 'password';
      this.icon = 'visibility.svg';
    }
  }
  showConfirmPassword() {
    if (this.confirmPassword && this.type_confirm === 'password') {
      this.type_confirm = 'text';
      this.icon_confirm = 'visibility_off.svg';
    } else if (this.confirmPassword && this.type_confirm === 'text') {
      this.type_confirm = 'password';
      this.icon_confirm = 'visibility.svg';
    }
  }
}
