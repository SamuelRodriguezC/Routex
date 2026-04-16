import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Route } from '../models/route.model';
import { tap } from 'rxjs';
import { ImportResult } from '../interfaces/ImportResult';

@Injectable({ providedIn: 'root' })
export class StatusService {

  private api = `${environment.apiUrl}/statuses/`;

  constructor(private http: HttpClient) {}

 
  getStatuses() {
    return this.http.get<any[]>(this.api);
}
}


