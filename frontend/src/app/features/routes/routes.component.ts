import { Component, OnInit, signal } from '@angular/core';
import { RouteService } from './../../core/services/route.service';
import { Route } from '../../core/models/route.model';

@Component({
  selector: 'app-routes',
  standalone: true,
  templateUrl: './routes.component.html'
})
export class RoutesComponent implements OnInit {

  routes = signal<Route[]>([]);
  loading = signal(true);

  constructor(private routeService: RouteService) {}

  ngOnInit() {
    this.loadRoutes();
  }

  loadRoutes() {
    this.loading.set(true);

    this.routeService.getRoutes().subscribe({
      next: (data) => {
        console.log('ROUTES FRONT:', data);
        this.routes.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('ERROR API:', err);
        this.loading.set(false);
      }
    });
  }
}