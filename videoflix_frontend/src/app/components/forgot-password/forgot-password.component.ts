import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from '../../shared/footer/footer.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [FormsModule, FooterComponent, NavBarComponent, WrapperComponent],
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.scss',
})
export class ForgotPasswordComponent {
  email!: string;
}
