import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnerCard } from './owner-card';

describe('OwnerCard', () => {
  let component: OwnerCard;
  let fixture: ComponentFixture<OwnerCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OwnerCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
