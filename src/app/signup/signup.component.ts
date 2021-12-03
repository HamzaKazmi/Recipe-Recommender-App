import { Component, OnInit } from '@angular/core';
import { AuthService} from '../auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  email: string;
  password: string;

  constructor(public authService: AuthService) {}

  ngOnInit() {
  }

  signup(email, password) {
    this.email = email;
    this.password = password;
    this.authService.signup(this.email, this.password);
    this.email = this.password = '';
  }


}
