import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteService } from '../../../core/services/route.service';
import { Route } from '../../../core/models/route.model';
import { RouteFormComponent } from '../route-form/route-form';import { ButtonModule } from 'primeng/button';

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

  // 👇 controla el modal
  showModal = signal(false);

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

  openCreate() {
    this.showModal.set(true);
  }

  onSaved() {
    // Se ejecuta cuando el form emite saved
    this.loadRoutes();
  }
}