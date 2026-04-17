import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { ExecutionLog } from '../models/execution-log.model';

export interface RouteLogsResponse {
  route_id: number;
  route: string;
  total_logs: number;
  logs: ExecutionLog[];
}

@Injectable({ providedIn: 'root' })
export class ExecutionLogService {

  private api = `${environment.apiUrl}/routes`;

  constructor(private http: HttpClient) {}

  //  GET logs by route
  getLogsByRoute(routeId: number): Observable<RouteLogsResponse> {
    return this.http.get<RouteLogsResponse>(
      `${this.api}/${routeId}/logs/`
    );
  }
}