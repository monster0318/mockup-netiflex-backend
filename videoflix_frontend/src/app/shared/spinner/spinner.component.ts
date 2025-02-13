import { Component, OnInit } from '@angular/core';
import { NgxSpinnerModule, NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [NgxSpinnerModule],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.scss',
})
export class SpinnerComponent implements OnInit {
  constructor(private spinner: NgxSpinnerService) {}

  ngOnInit(): void {
    this.spinner.show();

    setTimeout(() => {
      this.spinner.hide();
    }, 5000);
  }

  // showSpinner() {
  //   this.spinner.show();

  //   setTimeout(() => {
  //     this.spinner.hide();
  //   }, 10000);
  // }
}
