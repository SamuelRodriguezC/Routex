import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { RouteService } from '../../../core/services/route.service';
import { StatusService } from '../../../core/services/status.service';
import { PriorityService } from '../../../core/services/priority.service';

@Component({
  standalone: true,
  selector: 'app-route-detail',
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './route-detail.html'
})
export class RouteDetail implements OnInit {

  form!: FormGroup;
  routeId!: number;

  statuses: any[] = [];
  priorities: any[] = [];

  loading = false;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private routeService: RouteService,
    private statusService: StatusService,
    private priorityService: PriorityService
  ) {}

  ngOnInit() {
    this.routeId = Number(this.route.snapshot.paramMap.get('id'));

    this.initForm();
    this.loadCatalogs();
    this.loadRoute();
  }

  initForm() {
    this.form = this.fb.group({
      origin: ['', Validators.required],
      destination: ['', Validators.required],
      distance_km: [0, [Validators.required, Validators.min(0.01)]],
      time_window_start: ['', Validators.required],
      time_window_end: ['', Validators.required],
      status: [null, Validators.required],
      priority: [null, Validators.required]
    });
  }

  // 👇 CARGA CENTRALIZADA
  loadCatalogs() {
    this.loadStatuses();
    this.loadPriorities();
  }

  loadStatuses() {
    this.statusService.getStatuses().subscribe({
      next: (data) => {
        this.statuses = data.map((s: any) => ({
          label: s.description,
          value: s.id
        }));
      }
    });
  }

  loadPriorities() {
    this.priorityService.getPriorities().subscribe({
      next: (data) => {
        this.priorities = data.map((p: any) => ({
          label: p.priority_name,
          value: p.id
        }));
      }
    });
  }

  loadRoute() {
    this.routeService.getRouteById(this.routeId).subscribe(route => {
      this.form.patchValue({
        origin: route.origin,
        destination: route.destination,
        distance_km: route.distance_km,
        time_window_start: route.time_window_start,
        time_window_end: route.time_window_end,
        
        //  IMPORTANTE: ahora trabajamos con IDs
        status: route.status,
        priority: route.priority
      });
    });
  }

  submit() {
    if (this.form.invalid) return;

    this.loading = true;

    this.routeService.updateRoute(this.routeId, this.form.value)
      .subscribe({
        next: () => {
          this.loading = false;
          this.router.navigate(['/routes']);
        },
        error: (err) => {
          this.loading = false;
          console.error('Error updating route', err);
        }
      });
  }
}