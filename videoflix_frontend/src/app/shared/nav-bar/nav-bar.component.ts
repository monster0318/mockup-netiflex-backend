import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nav-bar.component.html',
  styleUrl: './nav-bar.component.scss',
})
export class NavBarComponent implements OnInit {
  @Input({ required: true }) logo: string = '';
  @Input() logOut: string = '';
  @Input() btnText: string = 'Log in';
  @Input() isAuthenticated: boolean = false;
  @Input() is_watching: boolean = false;
  @Input() login: boolean = false;

  constructor(private router: Router, private apiService: ApiService) {}
  ngOnInit(): void {
    this.isAuthenticated = this.apiService.isAuthenticated();
  }

  getLogoImage() {
    return 'assets/img/' + this.logo;
  }
  getLogOutImage() {
    return 'assets/img/' + this.logOut;
  }

  onReturnToStartPage() {
    if (this.isAuthenticated) {
      this.router.navigateByUrl('/video-offer');
    } else {
      this.router.navigateByUrl('/login');
    }
  }

  logUserInOrOut() {
    if (this.btnText === 'Log out') {
      sessionStorage.removeItem('token');
      this.router.navigateByUrl('');
    } else if (this.btnText === 'Log in') {
      this.router.navigateByUrl('/login');
    }
  }
}
