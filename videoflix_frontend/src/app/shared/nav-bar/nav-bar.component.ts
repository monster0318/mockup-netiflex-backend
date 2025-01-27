import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './nav-bar.component.html',
  styleUrl: './nav-bar.component.scss',
})
export class NavBarComponent {
  @Input({ required: true }) logo: string = '';
  @Input() logOut: string = '';
  @Input() btnText: string = 'Log in';
  @Input() login: boolean = false;

  getLogoImage() {
    return 'assets/img/' + this.logo;
  }
  getLogOutImage() {
    return 'assets/img/' + this.logOut;
  }
}
