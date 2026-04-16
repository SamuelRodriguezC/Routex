export class DateUtils {
  static toDateTimeLocal(value: string): string {
    if (!value) return '';

    const date = new Date(value);

    const offset = date.getTimezoneOffset();
    const localDate = new Date(date.getTime() - offset * 60000);

    return localDate.toISOString().slice(0, 16);
  }
}