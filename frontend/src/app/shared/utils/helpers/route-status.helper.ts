export const STATUS_COLOR_MAP: Record<string, string> = {
  READY: 'badge-success',
  PENDING: 'badge-warning',
  FAILED: 'badge-error',
  EXECUTED: 'badge-info',
};

export function getStatusBadgeClass(status?: string): string {
  if (!status) return 'badge-ghost';
  return STATUS_COLOR_MAP[status] ?? 'badge-neutral';
}