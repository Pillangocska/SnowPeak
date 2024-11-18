import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'status',
  standalone: true,
})
export class StatusPipe implements PipeTransform {
  transform(value?: string): string {
    switch (value) {
      case 'HALF_STEAM':
        return 'Fél gőz';
      case 'FULL_STEAM':
        return 'Teljes gőz';
      case 'STOPPED':
        return 'Áll';
      default:
        return '-';
    }
  }
}
