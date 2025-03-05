import { Injectable } from "@angular/core";
import { Subject } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class AuthFormService {
  constructor() {}

  private resetSignUpFormSource = new Subject<void>();
  private resetLogInFormSource = new Subject<void>();

  resetSignUpForm$ = this.resetSignUpFormSource.asObservable();
  resetLogInForm$ = this.resetLogInFormSource.asObservable();

  resetSignUpForm() {
    this.resetSignUpFormSource.next();
  }

  resetLogInForm() {
    this.resetLogInFormSource.next();
  }
}
