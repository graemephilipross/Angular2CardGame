/**
 * Created by Graeme on 4/5/2016.
 */

import {Injectable} from '@angular/core';

@Injectable()
export class SubscriberService {

    private _sub_id:number;

    setSubID(sub_id: number): void {
        this._sub_id = sub_id
    }

    getSubID(): number {
        return this._sub_id
    }
}