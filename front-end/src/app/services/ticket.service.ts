import { HttpClient } from '@angular/common/http';
import { Injectable, Service, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { TicketResposta } from '../models/tickets.model';

@Injectable({
    providedIn: 'root',
})
export class TicketService {
    private http = inject(HttpClient)
    private baseUrl = `http.://localhost:8000/tickets`
    listar(): Observable<TicketResposta[]>{
        return this.http.get<TicketResposta[]>(this.baseUrl);
    }
}
