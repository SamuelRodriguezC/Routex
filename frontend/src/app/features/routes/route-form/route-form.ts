import {
  Component,
  EventEmitter,
  Input,
  Output,
  signal,
  OnChanges,
  SimpleChanges
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { DatePickerModule } from 'primeng/datepicker';
import { SelectModule } from 'primeng/select';

import { RouteService } from '../../../core/services/route.service';
import { PriorityService } from '../../../core/services/priority.service';
import { StatusService } from '../../../core/services/status.service';

import { Route } from '../../../core/models/route.model';

@Component({
  selector: 'app-route-form',
  standalone: true,
  templateUrl: './route-form.html',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ButtonModule,
    DialogModule,
    InputTextModule,
    InputNumberModule,
    DatePickerModule,
    SelectModule
  ]
})
export class RouteFormComponent implements OnChanges {

  @Input() visible = false;
  @Output() visibleChange = new EventEmitter<boolean>();
  @Output() saved = new EventEmitter<void>();

  @Input() routeToEdit: Route | null = null;
  @Input() mode: 'create' | 'edit' = 'create';

  submitting = signal(false);
  errorMessage = signal<string | null>(null);

  priorityOptions = signal<any[]>([]);
  statusOptions = signal<any[]>([]);

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private routeService: RouteService,
    private priorityService: PriorityService,
    private statusService: StatusService
  ) {

    this.form = this.fb.group({
      origin: ['', Validators.required],
      destination: ['', Validators.required],
      distance_km: [null, [Validators.required, Validators.min(0.01)]],
      priority: [null, Validators.required],
      time_window_start: [null, Validators.required],
      time_window_end: [null, Validators.required],
      status: [null, Validators.required]
    }, { validators: this.timeWindowValidator });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['visible'] && this.visible) {
      this.loadPriorities();
      this.loadStatuses();

      if (this.routeToEdit) {
        this.mode = 'edit';
        this.fillForm();
      } else {
        this.mode = 'create';
        this.form.reset();
      }
    }
  }

  fillForm() {
    this.form.patchValue({
      origin: this.routeToEdit?.origin,
      destination: this.routeToEdit?.destination,
      distance_km: this.routeToEdit?.distance_km,
      priority: this.routeToEdit?.priority,
      status: this.routeToEdit?.status,
      time_window_start: new Date(this.routeToEdit?.time_window_start as any),
      time_window_end: new Date(this.routeToEdit?.time_window_end as any),
    });
  }

  loadPriorities() {
    this.priorityService.getPriorities().subscribe({
      next: (data) => {
        this.priorityOptions.set(
          data.map(p => ({
            label: p.priority_name,
            value: p.id
          }))
        );
      }
    });
  }

  loadStatuses() {
    this.statusService.getStatuses().subscribe({
      next: (data) => {
        this.statusOptions.set(
          data.map(s => ({
            label: s.description,
            value: s.id
          }))
        );
      }
    });
  }

  timeWindowValidator(group: FormGroup) {
    const start = group.get('time_window_start')?.value;
    const end = group.get('time_window_end')?.value;

    if (start && end && start >= end) {
      return { invalidWindow: true };
    }
    return null;
  }

  close() {
    this.visibleChange.emit(false);
    this.form.reset();
    this.routeToEdit = null;
    this.mode = 'create';
    this.errorMessage.set(null);
  }

  submit() {

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.errorMessage.set(null);

    const payload: Route = {
      ...this.form.value,
      time_window_start: this.form.value.time_window_start.toISOString(),
      time_window_end: this.form.value.time_window_end.toISOString(),
    };

    const request =
      this.mode === 'edit' && this.routeToEdit
        ? this.routeService.updateRoute(this.routeToEdit.id, payload)
        : this.routeService.createRoute(payload);

    request.subscribe({
      next: () => {
        this.submitting.set(false);
        this.saved.emit();
        this.close();
      },
      error: (err) => {
        this.submitting.set(false);

        if (err.error?.non_field_errors) {
          this.errorMessage.set(err.error.non_field_errors[0]);
          this.form.setErrors({ duplicate: true });
        } else {
          this.errorMessage.set(
            this.mode === 'edit'
              ? 'Error al actualizar la ruta'
              : 'Error al crear la ruta'
          );
        }
      }
    });
  }
}