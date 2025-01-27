import { Component } from '@angular/core';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { FooterComponent } from '../../shared/footer/footer.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [WrapperComponent, NavBarComponent, FooterComponent, FormsModule],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss',
})
export class SignUpComponent {
  password!: string;
  confirmPassword!: string;
  icon: string = 'visibility.svg';
  type: string = 'password';
  icon_confirm: string = 'visibility.svg';
  type_confirm: string = 'password';

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
}
