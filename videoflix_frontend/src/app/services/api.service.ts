import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private URL = 'http://127.0.0.1:8000/';
  private httpClient = inject(HttpClient);

  constructor() {}

  getAuthHeaders(token: string): HttpHeaders {
    const header = new HttpHeaders({
      Authorization: `Token ` + token,
      'Content-Type': 'application/json',
    });
    return header;
  }

  getUnAuthHeaders(): HttpHeaders {
    const header = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return header;
  }

  getData(endpoint: string, token: string): Observable<any> {
    return this.httpClient.get(this.URL + endpoint, {
      observe: 'response',
      headers: this.getAuthHeaders(token),
    });
  }

  postData(
    endpoint: string,
    payload: any,
    header: HttpHeaders
  ): Observable<any> {
    return this.httpClient.post(this.URL + endpoint, JSON.stringify(payload), {
      headers: header,
    });
  }

  putData(endpoint: string, payload: any, token: string) {
    return this.httpClient.put(this.URL + endpoint, JSON.stringify(payload), {
      headers: this.getAuthHeaders(token),
    });
  }

  /**
   *
   * @param endpoint - API endpoint
   * @param token - authenticated user's token
   * @returns status code 204 or error
   */
  deleteData(endpoint: string, token: string): Observable<any> {
    return this.httpClient.delete(this.URL + endpoint, {
      headers: this.getAuthHeaders(token),
    });
  }

  patchData(endpoint: string, payload: any, token: string): Observable<any> {
    return this.httpClient.patch(this.URL + endpoint, JSON.stringify(payload), {
      headers: this.getAuthHeaders(token),
    });
  }

  isAuthenticated(): boolean {
    const token = sessionStorage.getItem('token');
    return !!token;
  }
}
