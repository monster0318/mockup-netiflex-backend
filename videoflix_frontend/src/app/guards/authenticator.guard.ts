import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { ApiService } from '../services/api.service';

export const authenticatorGuard: CanActivateFn = (route, state) => {
  const apiService = inject(ApiService);
  const router = inject(Router);

  if (apiService.isAuthenticated()) {
    return true;
  } else {
    router.navigate(['/login'], {
      queryParams: { returnUrl: state.url },
    });
    return false;
  }
};
