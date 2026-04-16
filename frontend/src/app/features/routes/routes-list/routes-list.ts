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

  showModal = signal(false);

  selectedRoute = signal<Route | null>(null);

  getStatusBadgeClass = getStatusBadgeClass;
  formatDate = formatDate;

  constructor(private routeService: RouteService) {}

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

  // 🆕 CREAR
  openCreate() {
    this.selectedRoute.set(null);
    this.showModal.set(true);
  }

  // ✏️ EDITAR (AQUÍ ESTÁ EL CAMBIO IMPORTANTE)
  editRoute(route: Route) {
    this.selectedRoute.set(route);
    this.showModal.set(true);
  }

  onSaved() {
    this.loadRoutes();
  }
}