import { Component, signal } from '@angular/core';
import { CommonModule, JsonPipe } from '@angular/common';
import { RouteService } from '../../core/services/route.service';

@Component({
  selector: 'app-import-page',
  standalone: true,
  imports: [CommonModule, JsonPipe],
  templateUrl: 'import.page.html',
})
export class ImportPage {

  file = signal<File | null>(null);
  loading = signal(false);
  response = signal<any>(null);
  error = signal<string | null>(null);

  constructor(private routeService: RouteService) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.file.set(file);
  }

  upload() {
    if (!this.file()) return;

    this.loading.set(true);
    this.error.set(null);

    this.routeService.importExcel(this.file()!)
      .subscribe({
        next: (res) => {
          this.response.set(res);
          this.loading.set(false);
        },
        error: (err) => {
          this.error.set(err.error?.message || 'Error importando archivo');
          this.loading.set(false);
        }
      });
  }
}