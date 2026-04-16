import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteService } from '../../core/services/route.service';

@Component({
  selector: 'app-import-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: 'import.page.html',
})
export class ImportPage {

  file = signal<File | null>(null);

  loading = signal(false);
  processing = signal(false);

  response = signal<any>(null);
  error = signal<string | null>(null);

  progress = signal(0);

  constructor(private routeService: RouteService) {}

  onFileSelected(event: any) {
    this.file.set(event.target.files[0]);
  }

  upload() {
    const file = this.file();
    if (!file) return;

    this.loading.set(true);
    this.processing.set(true);
    this.error.set(null);
    this.response.set(null);
    this.progress.set(10);

    const interval = setInterval(() => {
      const current = this.progress();
      if (current < 90) this.progress.set(current + 10);
    }, 200);

    this.routeService.importExcel(file).subscribe({
      next: (res) => {
        clearInterval(interval);

        this.progress.set(100);
        this.response.set(res);

        this.processing.set(false);
        this.loading.set(false);
      },

      error: (err) => {
        clearInterval(interval);

        this.error.set(
          err?.error?.message || 'Error importando archivo'
        );

        this.processing.set(false);
        this.loading.set(false);
      }
    });
  }
}