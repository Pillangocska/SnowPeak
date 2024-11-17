import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { RxStompService } from '../../rx-stomp.service';

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

  watchPublicLiftsMessages(): Observable<any> {
    return this.rxStompService.watch(
      `${this.baseExchangeUrl}skilift.*.logs.status_update`,
    );
  }
}
