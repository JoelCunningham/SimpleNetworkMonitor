import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOwnerCard } from './add-owner-card';

describe('AddOwnerCard', () => {
  let component: AddOwnerCard;
  let fixture: ComponentFixture<AddOwnerCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddOwnerCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddOwnerCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
