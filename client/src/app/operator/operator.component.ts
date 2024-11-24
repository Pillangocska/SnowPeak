import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
  inject,
} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { KeycloakService } from 'keycloak-angular';
import { PrivateLiftResponseModel } from '../api/models';
import { LiftControllerService, LogControllerService } from '../api/services';
import { RxStompService } from '../rx-stomp.service';
import { FormsModule } from '@angular/forms';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTableModule } from '@angular/material/table';
import { EmergencyStopDialogComponent } from '../shared/components/emergency-stop-dialog/emergency-stop-dialog.component';
import { Subscription } from 'rxjs';
import { RabbitmqService } from '../shared/services/rabbitmq.service';
import { StatusPipe } from '../api/shared/pipe/status.pipe';
import { InternalKeycloakService } from '../shared/services/internal-keycloak.service';
import { PublicComponent } from '../public/public.component';

@Component({
  selector: 'app-operator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatChipsModule,
    MatDividerModule,
    MatCardModule,
    MatDialogModule,
    StatusPipe,
    PublicComponent,
    MatTooltipModule,
    MatTableModule,
  ],
  templateUrl: './operator.component.html',
  styleUrl: './operator.component.scss',
})
export class OperatorComponent implements OnInit {
  @ViewChild('temperatureLogContainer')
  private temperatureLogContainer!: ElementRef;
  @ViewChild('windLogContainer') private windLogContainer!: ElementRef;
  @ViewChild('commandContainer') private commandContainer!: ElementRef;

  keycloakService = inject(KeycloakService);
  internalKeycloakService = inject(InternalKeycloakService);
  rabbitMqService = inject(RabbitmqService);
  rxStompService = inject(RxStompService);
  logService = inject(LogControllerService);
  liftService = inject(LiftControllerService);
  cdr = inject(ChangeDetectorRef);
  dialog = inject(MatDialog);

  liftTemperatureSensorSubscription?: Subscription;
  liftWindSensorSubscription?: Subscription;
  liftStatusSubscription?: Subscription;
  liftCommandSubscription?: Subscription;

  sensorDisplayedColumns: string[] = ['timestamp', 'location', 'value'];
  commandDisplayedColumns: string[] = [
    'timestamp',
    'type',
    'user',
    'outcome',
    'args',
  ];
  temperatureDataSource: any[] = [];
  windDataSource: any[] = [];
  commandDataSource: any[] = [];

  lifts?: Array<PrivateLiftResponseModel & { liftName: string }>;
  selectedLiftId?: string;

  operatorId?: string;

  liftStatus?: 'FULL_STEAM' | 'HALF_STEAM' | 'STOPPED';

  message?: string;

  ngOnInit(): void {
    this.operatorId = this.internalKeycloakService.getUserId();
    this.liftService
      .getPrivateLiftsByOperatorId({
        operatorId: this.operatorId ?? '',
      })
      .subscribe(
        (lifts) =>
          (this.lifts = lifts.map((lift, idx) => ({
            liftName: `Lift ${idx + 1}`,
            ...lift,
          }))),
      );
  }

  private watchSelectedLiftTemperatureSensors(): void {
    this.liftTemperatureSensorSubscription?.unsubscribe();
    this.liftTemperatureSensorSubscription = undefined;

    if (this.selectedLiftId) {
      this.liftTemperatureSensorSubscription = this.rabbitMqService
        .watchTemperatureSensorsByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          this.temperatureDataSource = [
            ...this.temperatureDataSource,
            JSON.parse(message.body),
          ];
          setTimeout(() => {
            this.scrollToBottom(
              false,
              this.temperatureLogContainer.nativeElement,
            );
          });
        });
    } else {
      this.temperatureDataSource = [];
    }
  }

  private watchSelectedLiftWindSensors(): void {
    this.liftWindSensorSubscription?.unsubscribe();
    this.liftWindSensorSubscription = undefined;

    if (this.selectedLiftId) {
      this.liftWindSensorSubscription = this.rabbitMqService
        .watchWindSensorsByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          this.windDataSource = [
            ...this.windDataSource,
            JSON.parse(message.body),
          ];
          setTimeout(() => {
            this.scrollToBottom(false, this.windLogContainer.nativeElement);
          });
        });
    } else {
      this.windDataSource = [];
    }
  }

  private watchSelectedLiftStatus(): void {
    this.liftStatusSubscription?.unsubscribe();
    this.liftStatusSubscription = undefined;

    if (this.selectedLiftId) {
      this.liftStatusSubscription = this.rabbitMqService
        .watchPublicLiftsMessagesByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          this.liftStatus = JSON.parse(message?.body)?.skiLiftState;
        });
    } else {
      this.liftStatus = undefined;
    }
  }

  private watchSelectedLiftCommands(): void {
    this.liftCommandSubscription?.unsubscribe();
    this.liftCommandSubscription = undefined;

    if (this.selectedLiftId) {
      this.liftCommandSubscription = this.rabbitMqService
        .watchCommandsByLiftId(this.selectedLiftId)
        .subscribe((command: any) => {
          this.commandDataSource = [
            ...this.commandDataSource,
            JSON.parse(command.body),
          ];
          setTimeout(() => {
            this.scrollToBottom(false, this.commandContainer.nativeElement);
          });
        });
    } else {
      this.commandDataSource = [];
    }
  }

  scrollToBottom(force: boolean = false, element: any): void {
    const isAtBottom =
      element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

    if (force || isAtBottom) {
      element.scrollTop = element.scrollHeight;
    }
  }

  goToLift(liftId: string) {
    this.selectedLiftId = this.selectedLiftId === liftId ? undefined : liftId;
    this.temperatureDataSource = [];
    this.windDataSource = [];
    this.commandDataSource = [];
    this.liftStatus = undefined;

    this.watchSelectedLiftTemperatureSensors();
    this.watchSelectedLiftWindSensors();
    this.watchSelectedLiftStatus();
    this.watchSelectedLiftCommands();
  }

  sendMessage() {
    let body: any = {};
    body.messageKind = 'suggestion';
    body.severity = 'INFO';
    body.message = this.message;
    body.user = this.operatorId;
    body.timestamp = new Date().toISOString().slice(0, -1);
    this.rabbitMqService.sendSuggestion(this.selectedLiftId ?? '', body);
    this.message = undefined;
  }

  emergencyStop() {
    const dialogRef = this.dialog.open(EmergencyStopDialogComponent);

    dialogRef.afterClosed().subscribe((result) => {
      if (result && this.selectedLiftId) {
        result.user = this.operatorId;
        result.timestamp = new Date().toISOString().slice(0, -1);
        this.rabbitMqService.sendEmergencyStop(this.selectedLiftId, result);
      }
    });
  }

  login(): void {
    this.keycloakService.login();
  }

  logout(): void {
    this.keycloakService.logout();
  }
}
