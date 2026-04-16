import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { getStatusBadgeClass } from '../../../shared/utils/helpers/route-status.helper';
import { formatDate } from '../../../shared/utils/helpers/date-format.helper';
import { RouteService } from '../../../core/services/route.service';
import { Route } from '../../../core/models/route.model';

import { RouteFormComponent } from '../route-form/route-form';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-routes',
  standalone: true,
  templateUrl: './routes-list.html',
  imports: [
    CommonModule,
    ButtonModule,
    RouteFormComponent
  ]
})
export class RoutesList implements OnInit {

  routes = signal<Route[]>([]);
  loading = signal(true);

  getStatusBadgeClass = getStatusBadgeClass;

  showModal = signal(false);
  formatDate = formatDate;

  constructor(
    private routeService: RouteService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadRoutes();
  }

  loadRoutes() {
    this.loading.set(true);

    this.routeService.getRoutes().subscribe({
      next: (data) => {
        this.routes.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('ERROR API:', err);
        this.loading.set(false);
      }
    });
  }

  openCreate() {
    this.showModal.set(true);
  }

  onSaved() {
    this.loadRoutes();
  }

  editRoute(id: number) {
    this.router.navigate(['/routes', id]);
  }
}