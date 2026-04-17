import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { formatDate } from '../../../shared/utils/helpers/date-format.helper';
import { ExecutionLogService, RouteLogsResponse } from '../../../core/services/execution-log.service';
import { Location } from '@angular/common';


@Component({
  selector: 'app-route-logs',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './route-logs.html'
})
export class RouteLogs implements OnInit {

  routeId!: number;

  data = signal<RouteLogsResponse | null>(null);
  loading = signal(true);

  formatDate = formatDate;

  constructor(
    private route: ActivatedRoute,
    private logService: ExecutionLogService,
    private location: Location
  ) {}

  ngOnInit() {
    this.routeId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadLogs();
  }
  
  goBack() {
    this.location.back();
  }

  loadLogs() {
    this.loading.set(true);

    this.logService.getLogsByRoute(this.routeId).subscribe({
      next: (res) => {
        this.data.set(res);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('ERROR LOGS:', err);
        this.loading.set(false);
      }
    });
  }
}