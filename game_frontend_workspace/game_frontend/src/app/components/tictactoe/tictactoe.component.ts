import { Component, OnInit } from '@angular/core';
import { TictactoeService, GameState } from '../../services/tictactoe.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-tictactoe',
  templateUrl: './tictactoe.component.html',
  styleUrls: ['./tictactoe.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class TictactoeComponent implements OnInit {
  gameId: string | null = null;
  board: string[][] = [['', '', ''], ['', '', ''], ['', '', '']];
  status: 'in_progress' | 'win_X' | 'win_O' | 'draw' | null = null;
  nextPlayer: 'X' | 'O' | null = null;
  winner: string | null = null;
  loading = false;
  error: string | null = null;

  constructor(ttt: TictactoeService) {
    this.ttt = ttt;
  }

  private ttt: TictactoeService;

  ngOnInit(): void {
    this.newGame();
  }

  // PUBLIC_INTERFACE
  newGame() {
    this.loading = true;
    this.error = null;
    this.ttt.startGame().subscribe({
      next: (resp) => {
        this.syncState(resp);
        this.loading = false;
      },
      error: (e) => {
        this.loading = false;
        this.error = `Failed to start new game: ${e}`;
      }
    });
  }

  // PUBLIC_INTERFACE
  makeMove(row: number, col: number) {
    if (
      !this.gameId ||
      this.status !== 'in_progress' ||
      this.loading ||
      this.board[row][col]
    ) {
      return;
    }
    this.loading = true;
    this.error = null;
    this.ttt.makeMove(this.gameId, row, col).subscribe({
      next: (resp) => {
        this.syncState(resp);
        this.loading = false;
      },
      error: (e) => {
        this.loading = false;
        this.error = `Failed to make move: ${e}`;
      }
    });
  }

  getCellLabel(row: number, col: number): string {
    return this.board[row][col] || '';
  }

  get statusMessage(): string {
    if (this.status === 'win_X') return "Player X wins!";
    if (this.status === 'win_O') return "Player O wins!";
    if (this.status === 'draw') return "It's a draw!";
    if (this.status === 'in_progress') {
      return this.loading
        ? "Updating..."
        : (this.nextPlayer ? `Next turn: Player ${this.nextPlayer}` : "");
    }
    return '';
  }

  isBoardDisabled(): boolean {
    return this.loading || this.status !== 'in_progress';
  }

  private syncState(resp: GameState) {
    this.gameId = resp.game_id || this.gameId;
    this.board = resp.state?.map(row => row.slice()) ?? [['', '', ''], ['', '', ''], ['', '', '']];
    this.nextPlayer = resp.next_player;
    this.status = resp.status;
    this.winner = resp.winner ?? null;
  }
}
