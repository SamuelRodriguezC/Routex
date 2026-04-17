import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

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

  // 🔥 NUEVO: selección múltiple
  selectedRouteIds = signal<number[]>([]);

  // UI helpers
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

  // =========================
  // SELECCIÓN DE CHECKBOX
  // =========================
  toggleSelection(routeId: number, event: any) {
    const checked = event.target.checked;

    const current = this.selectedRouteIds();

    if (checked) {
      this.selectedRouteIds.set([...current, routeId]);
    } else {
      this.selectedRouteIds.set(current.filter(id => id !== routeId));
    }
  }

  // =========================
  // EJECUTAR MASIVO 🔥 NUEVO
  // =========================
  executeSelectedRoutes() {
    const ids = this.selectedRouteIds();

    if (ids.length === 0) {
      alert('Selecciona al menos una ruta');
      return;
    }

    this.routeService.executeRoutes(ids).subscribe({
      next: (res) => {
        console.log('EJECUCIÓN:', res);
        this.loadRoutes();
        this.selectedRouteIds.set([]);
      },
      error: (err) => {
        console.error('ERROR EJECUCIÓN:', err);
      }
    });
  }

  // =========================
  // CREAR
  // =========================
  openCreate() {
    this.selectedRoute.set(null);
    this.showModal.set(true);
  }

  // =========================
  // EDITAR
  // =========================
  editRoute(route: Route) {
    this.selectedRoute.set(route);
    this.showModal.set(true);
  }

  onSaved() {
    this.loadRoutes();
  }
}