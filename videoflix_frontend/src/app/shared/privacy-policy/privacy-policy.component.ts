import { Component, OnInit } from '@angular/core';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import { ApiService } from '../../services/api.service';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-privacy-policy',
  standalone: true,
  imports: [NavBarComponent, RouterLink],
  templateUrl: './privacy-policy.component.html',
  styleUrl: './privacy-policy.component.scss',
})
export class PrivacyPolicyComponent implements OnInit {
  isAuthenticated: boolean = false;

  constructor(private apiService: ApiService) {}
  ngOnInit(): void {
    this.isAuthenticated = this.apiService.isAuthenticated();
  }
}
