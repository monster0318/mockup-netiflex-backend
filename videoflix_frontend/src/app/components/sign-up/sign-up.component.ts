import { Component, inject, OnInit } from "@angular/core";
import { WrapperComponent } from "../../shared/wrapper/wrapper.component";
import { NavBarComponent } from "../../shared/nav-bar/nav-bar.component";
import { FooterComponent } from "../../shared/footer/footer.component";
import { FormGroup, FormsModule } from "@angular/forms";
import { ApiService } from "../../services/api.service";
import { RequestsService } from "../../services/requests.service";
import { ModuleService } from "../../services/module.service";
import { ToastrService } from "ngx-toastr";
import { AuthFormService } from "../../services/auth-form.service";

@Component({
  selector: "app-sign-up",
  standalone: true,
  imports: [WrapperComponent, NavBarComponent, FooterComponent, FormsModule],
  templateUrl: "./sign-up.component.html",
  styleUrl: "./sign-up.component.scss",
})
export class SignUpComponent implements OnInit {
  email: string | null = null;
  password: string | null = null;
  confirmPassword: string | null = null;
  icon: string = "visibility.svg";
  type: string = "password";
  icon_confirm: string = "visibility.svg";
  type_confirm: string = "password";
  emailAddress: string | null = null;
  errorMessage: string | null = null;
  errorType: string | null = null;
  signUpForm!: FormGroup;

  private apiService = inject(ApiService);
  private requestsService = inject(RequestsService);
  constructor(private authFormService: AuthFormService, private toastr: ToastrService, private moduleService: ModuleService) {}

  ngOnInit(): void {
    this.moduleService.email$.subscribe(email => {
      this.email = email;
    });

    this.requestsService.errorMessage$.subscribe(message => {
      this.errorMessage = message["message"][0];
      this.errorType = message["type"][0];
    });

    this.authFormService.resetSignUpForm$.subscribe(() => {
      this.signUpForm.reset();
    });
  }

  /**
   * success message when form submitted
   */
  successToast() {
    this.toastr.success("You signed up successfully, Please check your email to activate your account!");
  }

  /**
   * error message when form not submitted
   */
  errorToast() {
    this.toastr.error("Op an error occurs, Try again!");
  }

  /**
   * this function allow the user to toggle password view
   */
  showPassword() {
    if (this.password && this.type === "password") {
      this.type = "text";
      this.icon = "visibility_off.svg";
    } else if (this.password && this.type === "text") {
      this.type = "password";
      this.icon = "visibility.svg";
    }
  }

  /**
   * this function allow the user to toggle confirm password view
   */
  showConfirmPassword() {
    if (this.confirmPassword && this.type_confirm === "password") {
      this.type_confirm = "text";
      this.icon_confirm = "visibility_off.svg";
    } else if (this.confirmPassword && this.type_confirm === "text") {
      this.type_confirm = "password";
      this.icon_confirm = "visibility.svg";
    }
  }

  resetForm() {
    this.email = "";
    this.password = "";
    this.confirmPassword = "";
  }

  signUp() {
    this.requestsService
      .postData(
        "register/",
        {
          email: this.email,
          password: this.password,
          confirm_password: this.confirmPassword,
        },
        this.apiService.getUnAuthHeaders(),
        () => {
          this.requestsService.goToPage("/login");
          this.successToast();
        }
      )
      .then(() => {
        this.requestsService.errorMessage$.subscribe(error => {
          if (!error.message) {
            this.resetForm();
          }
        });
      });
  }
}
