import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { RequestsService } from '../../services/requests.service';

@Component({
  selector: 'app-activate-account',
  standalone: true,
  imports: [],
  templateUrl: './activate-account.component.html',
  styleUrl: './activate-account.component.scss',
})
export class ActivateAccountComponent implements OnInit {
  uid: string | null = null;
  token: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private requestsService: RequestsService
  ) {}

  ngOnInit(): void {
    this.uid = this.route.snapshot.paramMap.get('uid');
    this.token = this.route.snapshot.paramMap.get('token');
  }

  onNewPassword() {
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
