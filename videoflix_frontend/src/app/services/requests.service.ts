import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RequestsService {
  private isLoadingSubject = new BehaviorSubject<boolean>(true);
  isLoading$ = this.isLoadingSubject.asObservable();

  private isErrorSubject = new BehaviorSubject<boolean>(false);
  isError$ = this.isErrorSubject.asObservable();

  private errorMessageSubject = new BehaviorSubject<{
    error_type: string[] | null[];
    error_message: string[] | null[];
  }>({ error_type: [null], error_message: [null] });

  errorMessage$ = this.errorMessageSubject.asObservable();

  constructor(private router: Router, private route: ActivatedRoute) {}

  handleLoading(bool: boolean) {
    this.isLoadingSubject.next(bool);
  }

  handleError(bool: boolean) {
    this.isErrorSubject.next(bool);
  }

  handleErrorMessage(message: any) {
    this.errorMessageSubject.next(message);
  }
}
