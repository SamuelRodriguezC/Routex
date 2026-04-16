import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Route } from '../models/route.model';
import { tap } from 'rxjs';
import { ImportResult } from '../interfaces/ImportResult';

@Injectable({ providedIn: 'root' })
export class RouteService {

  private api = `${environment.apiUrl}/routes/`;

  constructor(private http: HttpClient) {}

  getRoutes() {
    return this.http.get<Route[]>(this.api).pipe(
      tap(res => console.log('API RESPONSE:', res))
    );
  }

  createRoute(route: Route) {
    return this.http.post<Route>(this.api, route);
  }

  importExcel(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<ImportResult>(
      `${this.api}import/`,
      formData
    );
  }

  executeRoutes(routeIds: number[]) {
    return this.http.post(`${this.api}execute`, {
      routes: routeIds
    });
  }
}


