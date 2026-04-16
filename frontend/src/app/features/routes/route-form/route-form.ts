import { Component, EventEmitter, Input, Output, signal, OnChanges, SimpleChanges } from '@angular/core';
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

  submitting = signal(false);
  errorMessage = signal<string | null>(null);

  priorityOptions = signal<any[]>([]);
  statusOptions = signal<any[]>([]);

  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private routeService: RouteService,
    private priorityService: PriorityService,
    private statusService: StatusService
  ) {

    this.form = this.fb.group({
      origin: ['', [Validators.required]],
      destination: ['', [Validators.required]],
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
    }
  }

  loadPriorities() {
    this.priorityService.getPriorities().subscribe({
      next: (data) => {

        const mapped = data.map(p => ({
          label: p.priority_name,
          value: p.id
        }));

        this.priorityOptions.set(mapped);
      }
    });
  }

  loadStatuses() {
    this.statusService.getStatuses().subscribe({
      next: (data) => {

        const mapped = data.map(s => ({
          label: s.description,
          value: s.id
        }));

        this.statusOptions.set(mapped);
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

    this.routeService.createRoute(payload).subscribe({
      next: () => {
        this.submitting.set(false);
        this.saved.emit();
        this.close();
      },
      error: (err) => {
        this.submitting.set(false);
          console.log('ERROR COMPLETO:', err);
          console.log('ERROR BODY:', err.error);;

        if (err.error?.non_field_errors) {
          this.errorMessage.set(err.error.non_field_errors[0]);
          this.form.setErrors({ duplicate: true });
        } else {
          this.errorMessage.set('Error al crear la ruta');
        }
      }
    });
  }
  // submit() {
  //   console.log('🚀 FORMULARIO ENVIADO, VALIDANDO...');
  //   if (this.form.invalid) {
  //     this.form.markAllAsTouched();
  //     return;
  //   }

  //   this.errorMessage.set(null);

  //   const payload: Route = {
  //     ...this.form.value,
  //     time_window_start: this.form.value.time_window_start.toISOString(),
  //     time_window_end: this.form.value.time_window_end.toISOString(),
  //   };

  //   console.log('📦 PAYLOAD QUE SE ENVIARÍA:');
  //   console.log(payload);

  //   console.log('📦 JSON FORMATEADO:');
  //   console.log(JSON.stringify(payload, null, 2));

  //   // 🚫 No enviamos nada al backend aún
  // }
}