import { Component, OnInit } from '@angular/core';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-legal-notice',
  standalone: true,
  imports: [NavBarComponent, RouterLink, DatePipe],
  templateUrl: './legal-notice.component.html',
  styleUrl: './legal-notice.component.scss',
})
export class LegalNoticeComponent implements OnInit {
  todayDate: Date = new Date();
  isAuthenticated: boolean = false;

  constructor(private apiService: ApiService) {}
  ngOnInit(): void {
    this.isAuthenticated = this.apiService.isAuthenticated();
  }
}
