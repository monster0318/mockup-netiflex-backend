import { Routes } from "@angular/router";
import { ResetPasswordComponent } from "./components/reset-password/reset-password.component";
import { LogInComponent } from "./components/log-in/log-in.component";
import { SignUpComponent } from "./components/sign-up/sign-up.component";
import { PrivacyPolicyComponent } from "./shared/privacy-policy/privacy-policy.component";
import { LegalNoticeComponent } from "./shared/legal-notice/legal-notice.component";
import { StartpageComponent } from "./components/startpage/startpage.component";
import { ForgotPasswordComponent } from "./components/forgot-password/forgot-password.component";
import { VideoOfferComponent } from "./components/video-offer/video-offer.component";
import { VideoPlayerComponent } from "./components/video-player/video-player.component";
import { ActivateAccountComponent } from "./components/activate-account/activate-account.component";
import { authenticatorGuard } from "./guards/authenticator.guard";
import { PlayerComponent } from "./components/player/player.component";

export const routes: Routes = [
  {
    path: "",
    component: StartpageComponent,
    title: "Videoflix | Home",
  },
  {
    path: "reset-password/:uid/:token",
    component: ResetPasswordComponent,
    title: "Videoflix | Reset Password",
  },
  {
    path: "activate-account/:uid/:token",
    component: ActivateAccountComponent,
    title: "Videoflix | Activate Account",
  },
  {
    path: "new-password",
    component: ForgotPasswordComponent,
    title: "Videoflix | New Password",
  },
  {
    path: "login",
    component: LogInComponent,
    title: "Videoflix | Log In",
  },
  {
    path: "signup",
    component: SignUpComponent,
    title: "Videoflix | Sign Up",
  },
  {
    path: "video-offer",
    component: VideoOfferComponent,
    canActivate: [authenticatorGuard],
    title: "Videoflix | Videos",
  },
  {
    path: "video-player",
    component: VideoPlayerComponent,
    canActivate: [authenticatorGuard],
    title: "Videoflix | Player",
  },
  {
    path: "player",
    component: PlayerComponent,
    canActivate: [authenticatorGuard],
    title: "Videoflix | Player",
  },
  {
    path: "privacy-policy",
    component: PrivacyPolicyComponent,
    title: "Videoflix | Privacy Policy",
  },
  {
    path: "legal-notice",
    component: LegalNoticeComponent,
    title: "Videoflix | Legal Notice",
  },
  { path: "**", redirectTo: "login" },
];
