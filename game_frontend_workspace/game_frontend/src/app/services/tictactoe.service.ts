import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

// PUBLIC_INTERFACE
export interface GameState {
  game_id: string;
  state: string[][];
  next_player: 'X' | 'O' | null;
  status: 'in_progress' | 'win_X' | 'win_O' | 'draw';
  winner?: 'X' | 'O' | null;
}

// PUBLIC_INTERFACE
@Injectable({
  providedIn: 'root'
})
export class TictactoeService {
  private apiBase = '/api/games';

  constructor(private http: HttpClient) {}

  // PUBLIC_INTERFACE
  startGame(): Observable<GameState> {
    return this.http.post<GameState>(this.apiBase, {})
      .pipe(catchError(this.handleError));
  }

  // PUBLIC_INTERFACE
  makeMove(gameId: string, row: number, col: number): Observable<GameState> {
    return this.http.post<GameState>(`${this.apiBase}/${gameId}/moves`, { row, col })
      .pipe(catchError(this.handleError));
  }

  // PUBLIC_INTERFACE
  getGame(gameId: string): Observable<GameState> {
    return this.http.get<GameState>(`${this.apiBase}/${gameId}`)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    let msg = 'An unknown error occurred.';
    if (error.error instanceof ErrorEvent) {
      msg = error.error.message;
    } else if (error.error && error.error.detail) {
      msg = error.error.detail;
    } else if (typeof error.error === 'string') {
      msg = error.error;
    }
    return throwError(() => msg);
  }
}
