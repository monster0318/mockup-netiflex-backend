import { Routes } from '@angular/router';
import { ResetPasswordComponent } from './components/reset-password/reset-password.component';
import { LogInComponent } from './components/log-in/log-in.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { PrivacyPolicyComponent } from './shared/privacy-policy/privacy-policy.component';
import { LegalNoticeComponent } from './shared/legal-notice/legal-notice.component';
import { StartpageComponent } from './components/startpage/startpage.component';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { VideoOfferComponent } from './components/video-offer/video-offer.component';
import { VideoPlayerComponent } from './components/video-player/video-player.component';

export const routes: Routes = [
  {
    path: '',
    component: StartpageComponent,
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent,
  },
  {
    path: 'new-password',
    component: ForgotPasswordComponent,
  },
  {
    path: 'login',
    component: LogInComponent,
  },
  {
    path: 'signup',
    component: SignUpComponent,
  },
  {
    path: 'video-offer',
    component: VideoOfferComponent,
  },
  {
    path: 'video-player',
    component: VideoPlayerComponent,
  },
  {
    path: 'privacy-policy',
    component: PrivacyPolicyComponent,
  },
  {
    path: 'legal-notice',
    component: LegalNoticeComponent,
  },
];
