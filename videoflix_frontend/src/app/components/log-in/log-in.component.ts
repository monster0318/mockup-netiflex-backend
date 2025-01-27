import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FooterComponent } from '../../shared/footer/footer.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-log-in',
  standalone: true,
  imports: [
    FormsModule,
    FooterComponent,
    NavBarComponent,
    WrapperComponent,
    RouterLink,
  ],
  templateUrl: './log-in.component.html',
  styleUrl: './log-in.component.scss',
})
export class LogInComponent {
  password!: string;
  icon: string = 'visibility.svg';
  type: string = 'password';

  showPassword() {
    if (this.password && this.type === 'password') {
      this.type = 'text';
      this.icon = 'visibility_off.svg';
    } else if (this.password && this.type === 'text') {
      this.type = 'password';
      this.icon = 'visibility.svg';
    }
  }
}
