import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { RequestsService } from '../../services/requests.service';
import { FooterComponent } from '../../shared/footer/footer.component';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { WrapperComponent } from '../../shared/wrapper/wrapper.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-activate-account',
  standalone: true,
  imports: [FooterComponent, NavBarComponent, WrapperComponent, CommonModule],
  templateUrl: './activate-account.component.html',
  styleUrl: './activate-account.component.scss',
})
export class ActivateAccountComponent implements OnInit {
  uid: string | null = null;
  token: string | null = null;
  errorMessage: string | null = null;
  errorType: string | null = null;
  responseMessage: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private requestsService: RequestsService
  ) {}

  ngOnInit(): void {
    this.uid = this.route.snapshot.paramMap.get('uid');
    this.token = this.route.snapshot.paramMap.get('token');

    this.requestsService.errorMessage$.subscribe((message) => {
      this.errorMessage = message['message'][0];
      this.errorType = message['type'][0];
    });

    this.requestsService.response$.subscribe((response) => {
      this.responseMessage = response['message'];
    });
  }

  onActivateAccount() {
    this.requestsService.resetResponse();
    this.requestsService.postData(
      'activate-account/',
      {
        uid: this.uid,
        token: this.token,
      },
      this.apiService.getUnAuthHeaders(),
      () => {
        console.log('Account activated!👌');
      }
    );
  }
}
