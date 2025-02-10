import { Component, OnInit } from '@angular/core';
import { NavBarComponent } from '../../shared/nav-bar/nav-bar.component';
import { FooterComponent } from '../../shared/footer/footer.component';
import { FormsModule } from '@angular/forms';
import { ModuleService } from '../../services/module.service';

@Component({
  selector: 'app-startpage',
  standalone: true,
  imports: [NavBarComponent, FooterComponent, FormsModule],
  templateUrl: './startpage.component.html',
  styleUrl: './startpage.component.scss',
})
export class StartpageComponent {
  email!: string;
  emailAddress!: string | null;
  constructor(private moduleService: ModuleService) {}

  sendEmail(emailAddress: string) {
    if (this.email) {
      this.moduleService.emitEmail(emailAddress);
    }
  }
}
