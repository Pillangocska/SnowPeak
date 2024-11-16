import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-emergency-stop-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  templateUrl: './emergency-stop-dialog.component.html',
  styleUrl: './emergency-stop-dialog.component.scss',
})
export class EmergencyStopDialogComponent {}
