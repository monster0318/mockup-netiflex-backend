import { Component, inject, OnInit } from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { FooterComponent } from '../../shared/footer/footer.component';
import { FormsModule } from '@angular/forms';
import { ModuleService } from '../../services/module.service';
import { RequestsService } from '../../services/requests.service';
import { NgxSpinnerModule, NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-startpage',
  standalone: true,
  imports: [NavBarComponent, FooterComponent, FormsModule, NgxSpinnerModule],
  templateUrl: './startpage.component.html',
  styleUrl: './startpage.component.scss',
})
export class StartpageComponent {
  email!: string;
  emailAddress!: string | null;
  isSpinnerShowed: boolean = true;
  private requestsService = inject(RequestsService);
  constructor(
    private moduleService: ModuleService,
    private spinner: NgxSpinnerService
  ) {}

  ngOnInit(): void {
    this.spinner.show();
    setTimeout(() => {
      this.spinner.hide();
      this.isSpinnerShowed = false;
    }, 5000);
  }

  sendEmail(emailAddress: string) {
    if (this.email) {
      this.moduleService.emitEmail(emailAddress);
      this.requestsService.goToPage('/signup');
    }
  }
}
