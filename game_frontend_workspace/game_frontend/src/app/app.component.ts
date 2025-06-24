import { Component } from '@angular/core';
import { TictactoeComponent } from './components/tictactoe/tictactoe.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TictactoeComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'angular';
}
