import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { RxStompService } from '../../rx-stomp.service';
import { convertFromStringToBuffer } from '../../api/shared/functions/binary.function';

@Injectable({
  providedIn: 'root',
})
export class RabbitmqService {
  rxStompService = inject(RxStompService);

  baseExchangeUrl = '/exchange/topic_skilift/';

  watchSensorsByLiftId(liftId: string): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.${liftId}.logs.sensor.*`,
    );
  }

  watchTemperatureSensorsByLiftId(liftId: string): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.${liftId}.logs.sensor.temperature`,
    );
  }

  watchWindSensorsByLiftId(liftId: string): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.${liftId}.logs.sensor.wind`,
    );
  }

  watchPublicLiftsMessages(): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.*.logs.status_update`,
    );
  }

  watchPublicLiftsMessagesByLiftId(liftId: string): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.${liftId}.logs.status_update`,
    );
  }

  watchCommandsByLiftId(liftId: string): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.${liftId}.logs.command.*`,
    );
  }

  sendEmergencyStop(liftId: string, body: any): void {
    var binaryData = convertFromStringToBuffer(body);
    this.rxStompService.publish({
      destination: `/exchange/direct_emergency_stop/${liftId}`,
      binaryBody: binaryData,
      headers: {
        'content-type': 'application/octet-stream',
        'lift-id': liftId,
      },
    });
  }

  sendSuggestion(liftId: string, body: any): void {
    var binaryData = convertFromStringToBuffer(body);
    this.rxStompService.publish({
      destination: `/exchange/direct_suggestions/${liftId}`,
      binaryBody: binaryData,
      headers: {
        'content-type': 'application/octet-stream',
        'lift-id': liftId,
      },
    });
  }
}
