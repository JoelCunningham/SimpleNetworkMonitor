import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnerAddCard } from './owner-add-card';

describe('AddOwnerCard', () => {
  let component: OwnerAddCard;
  let fixture: ComponentFixture<OwnerAddCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerAddCard],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnerAddCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
